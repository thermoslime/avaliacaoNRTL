# -*- coding: utf-8 -*-
'''
Python com as funções utilizadas para os cálculos
'''

from dash import dash_table
# é preciso para lidar com excel: import openpyxl
import pandas as pd

# Biblioteca para plotar gráficos
import matplotlib.pyplot as plt
import plotly.graph_objects as go
# Biblioteca para dados
import numpy as np

# Para processar a tabelas
import base64
import io



def separar_tielines(df, fase="I"):

  if fase == "I":
    x1 = df['C1-I']
    x2 = df['C2-I']
    x3 = df['C3-I']

  elif fase == "II":
    x1 = df['C1-II']
    x2 = df['C2-II']
    x3 = df['C3-II']

  frac = []

  for i in df.index:
    composicao = [float(x1[i]), float(x2[i]), float(x3[i])]

    frac.append(composicao)

  return np.array(frac)


# Para pegar o conteudo de um arquivo
def df_tielines(conteudo, filename):
  '''
  Função para a leitura do dataframe retornado pelo site, na base 64. Retorna uma tupla com o dataframe, e 2 arrays

  Parâmetros
    ----------
    conteudo : base 64
        conteúdo do arquivo, codificada na base 64

    filename: str
        nome do arquivo, com a extenção dele


    Retorna
    -------
    df : Objeto Pandas
        Data frame com as tie-lines
  '''

  conteudo_type, conteudo_string = conteudo.split(',')

  # decodifica o conteudo que está na Base 64. São dados Binários (tipo bytes)
  decoded = base64.b64decode(conteudo_string)

  try:
    # se o arquivo for csv
    if 'csv' in filename:
      # Usamos o "io.StringIO" para que o pandas consiga manipular o conteúdo
      df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), decimal=",")

    # se o arquivo for um excel
    elif 'xlsx' in filename:
      df = pd.read_excel(io.BytesIO(decoded))

    # Removendo as linhas vazias
    df_limpo = df.dropna()

    tie_1 = separar_tielines(df_limpo, "I")
    tie_2 = separar_tielines(df_limpo, "II")

    return (df_limpo, tie_1, tie_2)

  except Exception as e:
    print(f"Erro gerado, dica? {e}")
    mensagem = 'Ocorreu um erro no carregamento dos dados do arquivo'
    return mensagem


def tabela_eixo_tielines(tupla_tieline):
  '''
  Função usada para mostrar a tabela com as informações dos cálculos da Tie-line


  Parâmetros
    ----------
    tupla_tieline: (listax1, listaX2, listaDeltaG)


    Retorna
    -------
    um objeto DBC tabela
  '''

  if tupla_tieline != None:
    n_casas = 4

    x1_extrato = []
    x2_extrato = []
    delta_G_extrato = []

    x1_rafinado = []
    x2_rafinado = []
    delta_G_rafinado = []

    tie_line = []

    # Percorrendo x1
    for x_1 in tupla_tieline[0]:
      x1_extrato.append(round(x_1[0], n_casas))
      x1_rafinado.append(round(x_1[1], n_casas))

    # Percorrendo x2
    for x_2 in tupla_tieline[1]:
      x2_extrato.append(round(x_2[0], n_casas))
      x2_rafinado.append(round(x_2[1], n_casas))

    # Percorrendo deltaG
    for deltaG in tupla_tieline[2]:
      delta_G_extrato.append(round(deltaG[0], n_casas))
      delta_G_rafinado.append(round(deltaG[1], n_casas))

    # Fazendo o indice
    for indice in  range(len(tupla_tieline[0])):
      texto = f'Tie-line #{indice + 1}'
      tie_line.append(texto)

    df = pd.DataFrame({
      'ordem' : tie_line,
      'x1_I' : x1_extrato,
      'x2_I' : x2_extrato,
      'DeltaG_I' : delta_G_extrato,
      'x1_II': x1_rafinado,
      'x2_II': x2_rafinado,
      'DeltaG_II': delta_G_rafinado,
    })

    tabela = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])

    return tabela

  else:
    return ''


def Modelo_NRTL(x, alpha, tau, mostrar = False, componentes = 2):
    """
    Calcula os coeficientes de atividade pelo modelo NRTL, recebendo a composição (binário por default)
    retorna 2 coeficientes de atividade.


    Parâmetros
    ----------
    x : ndarray(n_compnentes, 1)
        Fração molar de cada componente em equilibrio na fase (estimativa)

    alpha : ndarray(n_compnentes, n_compnentes)
        Array dos parâmetros de não aleatoriedade do modelo NRTL.

    tau : ndarray(n_compnentes, n_compnentes)
        Parâmetro de interação binária. É uma matriz

    mostrar : Booleano
        Se True, mostra os prints dos resultados

    componentes : Inteiro = 2
      Número de componentes na mistura


    Retorna
    -------
    gamma : ndarray(n_compnentes,)
        Coeficiente de Atividade de cada componente


    Exemplo
    -------
    Alpha = [
      [0,   A12],
      [A21, 0]
    ]

    tau = [
      [0,     Tau12],
      [Tau21, 0]
    ]

    t = 200

    x = [x1, x2]
    """


    #Faz o cálculo direto com a matriz. G é uma matriz com Gii = Gjj = 1
    G = np.exp(-alpha * tau)

    # Array de zeros com o mesmo formato de X
    gamma = np.zeros_like(x)


    # Soma
    termo_2 = 0

    # i é o indice com dois componentes. [1, 2, 3]
    for i in range(componentes):

      # np.sum faz a soma de todos os elementos de um array
      # tau[:,i] -> da matrix tau, ele pega a coluna i
      # tau[:,i] * G[:,i] - > retorna o produto das colunas
      # x -> Não recebe indice, pois é um vetor e não matriz

      # Numerador do primeiro termo
      tau_G_x = np.sum(tau[:,i] * G[:,i] * x )

      # Denominador do primeiro termo
      G_x = np.sum(G[:,i] * x)

      # Primeiro termo. Correto
      termo_1 =  tau_G_x / G_x

      #print(f"O termo 1 deu: {termo_1}")
      #print("Para o termo 2\n")

      # Reinicia a contagem para o próximo loop do componente i
      termo_2 = 0

      # Faz um segundo loop, com j = 1,2,3
      for j in range(componentes):

        # Cálculo do termo entre parênteses
        parenteses = tau[i,j] - ( np.sum(x * tau[:,j] * G[:,j]) / np.sum(G[:,j] * x) )

        # Adiciona o valor para o segundo termo do composto i
        termo_2 += ( x[j] * G[i,j] / np.sum (G[:,j]*x) )  * parenteses


      # Array com o coeficiente de atividade de cada componente
      gamma[i] = termo_1 + termo_2

    # Mostrando os valores
    if mostrar:

      print(f"O valor de -Alfa é: \n {-alpha}")

      print(f"\n O valor de tau (= A + B/T) é : \n {tau}")

      print(f"\nG (=exp [-alpha* Tau]) igual a: \n {G}")

      print(f"\n coef igual a: \n{np.exp(gamma)}")


    # Retorna o coeficiente de atividade
    return np.exp(gamma)



def FracaoMolar(ComposicaoMassica, MassaMolar):
  '''
  Função para transformar fração Mássica em molar

  Parâmetros
  -------------
  ComposicaoMassica (3, n):
  Matriz com todos os pontos experimentais, contendo a composição Mássica
  das duas fases

  MassaMolar (3,):
  Array que contem a massa molar dos três componentes, em ordem

  Retorna
  ------------
  Matriz com os valores em molar no formato (3,n)


  Obs
  -----------
  É usado para converter os dados fornecidos pelos experimentos de ELL em molar
  de forma a usar o modelo NRTL
  '''

  # Lista com as frações molares
  fracao_molar = []

  for massa in ComposicaoMassica:

    mols = massa / MassaMolar

    # Divide cada Mol pelo total, para obter a fração
    frac_molar = mols/ np.sum(mols)

    # Adicionamos na lista de fração molar
    fracao_molar.append(frac_molar)


  # Converte a lista em array
  return np.array(fracao_molar)


def DeltaG_Mistura_par_binario(xy, alfaij, tauij, par = '1-2', mostrar = False):
  """
  Calcula a energia livre de gibbs da mistura para um dado par binário


  Parâmetros
  ----------
  xy : ndarray(2, n)
      Fração molar dos pares trabalhados

  alfa : ndarray(n_compnentes, n_compnentes)
      Array dos parâmetros de não aleatoriedade do modelo NRTL.

  tau: ndarray(n_compnentes, n_compnentes)
      Parâmetro de interação binária. É uma matriz 3x3

  par: int
      Parâmetro que indica o par trabalhado, aceita '1-2', '1-3', e '2-3'

  mostrar : Booleano
      Se True, mostra os prints dos resultados

  n_componentes : Inteiro = 2
      Número de componentes na mistura

  Retorna
  -------
  deltaG : float
      Energia livre de Gibbs da mistura
  """
  if par == '1-2':
    alfa = np.array([
      [0, alfaij[0][1]],
      [alfaij[1][0], 0]
])
    tau =  np.array([
      [0, tauij[0][1]],
      [tauij[1][0], 0]
    ])

  elif par == '1-3':
    alfa = np.array([
      [0, alfaij[0][2]],
      [alfaij[2][0], 0]
    ])

    tau = np.array([
      [0, tauij[0][2]],
      [tauij[2][0], 0]
    ])

  elif par == '2-3':
    alfa = np.array([
      [0, alfaij[1][2]],
      [alfaij[2][1], 0]
])
    tau =  np.array([
      [0, tauij[1][2]],
      [tauij[2][1], 0]
    ])

  else:
    alfa = tau = None

  deltaG_par = []

  for x in xy:
    # Calculamos os coeficientes de atividade
    gamma = Modelo_NRTL(x, alfa, tau, mostrar = mostrar, componentes =  2)

    # Termo da energia de gibbs calculada com o modelo de gE
    termo_1 = 0
    # Termo da energia de gibbs ideal
    termo_2 = 0

    # Indice dos componentes. Primeiro e Segundo
    for i in range(2):

      # Caso a composição seja zero
      if  x[i] == 0:
        # Não temos contribuição para a energia, pois é nula o produto
        termo_1 += 0
        termo_2 += 0

      # Caso a composição seja maior que zero
      else:
        # Calculamos os termos
        termo_1 += x[i] * np.log(gamma[i])
        termo_2 += x[i] * np.log(x[i])

    # Obtemos a energia de gibbs
    deltaG = termo_1 + termo_2

    # Atualizamos a lista
    deltaG_par.append(deltaG)

  # Transformamos a lista em array
  deltaG_par = np.array(deltaG_par)

  # Retornamos a variável
  return deltaG_par


def DeltaG_Mistura(x, alfa, tau, mostrar = False, n_componentes = 3):
  """
  Calcula a energia livre de gibbs da mistura para até 3 componentes


  Parâmetros
  ----------
  x : ndarray(3, n)
      Fração molar dos pares trabalhados

  alfa : ndarray(n_compnentes, n_compnentes)
      Array dos parâmetros de não aleatoriedade do modelo NRTL.

  tau: ndarray(n_compnentes, n_compnentes)
      Parâmetro de interação binária. É uma matriz 3x3

  mostrar : Booleano
      Se True, mostra os prints dos resultados

  n_componentes : Inteiro = 3
      Número de componentes na mistura

  Retorna
  -------
  deltaG : float
      Energia livre de Gibbs da mistura
  """


  # Calculamos os coeficientes de atividade (3 valores)
  gamma = Modelo_NRTL(x, alfa, tau, mostrar = mostrar, componentes=  n_componentes )

  # Termo da energia de gibbs calculada com o modelo de gE
  termo_1 = 0
  # Termo da energia de gibbs ideal
  termo_2 = 0

  # Indice dos componentes. Primeiro, Segundo e terceiro
  for i in range(n_componentes):
    # Caso a composição seja zero
    if  x[i] == 0:
      # Não temos contribuição para a energia, pois é nula o produto
      termo_1 += 0
      termo_2 += 0

    # Caso a composição seja maior que zero
    else:
      # Calculamos os termos
      termo_1 += x[i] * np.log(gamma[i])
      termo_2 += x[i] * np.log(x[i])

    # Obtemos a energia de gibbs

  deltaG = termo_1 + termo_2

  return deltaG



def Fronteira_Tauij(Tauij, titulo = "Fronteira de solubilidade para modelo NRTL"):
  """
  Função  que retorna o gráfico da fronteira Título do gráfico

  """

  # Pontos originais dos parâmetros
  eixo_valores_tauij = (Tauij[0][1], Tauij[0][2], Tauij[1][2])  # Tau_ij
  eixo_valores_tauji = (Tauij[1][0], Tauij[2][0], Tauij[2][1])  # Tau_ji

  # Eixo onde ficará os novos valores
  eixo_tauji_limites = []  # Tau_ji

  # Inicializa o eixo, inicia em -10 e vai até 20.
  eixo_tauij_fronteira = np.linspace(-10, 20, 100)  # Tau_ij

  # Percorre cada valor que será utilizado. Tau_ij
  for tau_ij in eixo_tauij_fronteira:

    if tau_ij <= -3:
      tau_ji = -1.833 * tau_ij + 1.423

    elif tau_ij > -3 and tau_ij <= 7:
      tau_ji = -4.191e-3 * pow(tau_ij, 3) + 9.089e-2 * pow(tau_ij, 2) - 1.206 * tau_ij + 2.481

    else:
      tau_ji = -0.545 * tau_ij + 0.7758

      # Valor da fronteira
      # print(f"Para tau_ij = {tau_ij}, o valor deu {tau_ji}")

    eixo_tauji_limites.append(tau_ji)

  eixo_tauji_limites = np.array(eixo_tauji_limites)

  # Obtenção dos máximos e mínimos, para as regiões
  minimo = np.ones_like(eixo_tauji_limites) * np.min(eixo_tauji_limites)
  maximo = np.ones_like(eixo_tauji_limites) * np.max(eixo_tauji_limites)

  ############## Criação do Gráfico ##############

  # Criando a figura
  fig = go.Figure()

  # Adicionando os pontos
  fig.add_scatter(
    x = eixo_valores_tauij,
    y = eixo_valores_tauji,
    mode = 'markers',
    marker = dict(color='green', size=10),
    name = 'Experimental',
    showlegend = True  # Não mostrar na legenda
  )

  # Adicionando a curva central, fronteira
  fig.add_trace(go.Scatter(
    x = eixo_tauij_fronteira,
    y = eixo_tauji_limites,
    line = dict(color='black'),  # Cor da linha
    name = 'Fronteira',
    showlegend = True  # Não mostrar na legenda
  ))

  # Preenchendo a área entre as curvas. Área Inferior
  fig.add_trace(go.Scatter(
    x = np.concatenate([eixo_tauij_fronteira, eixo_tauij_fronteira[::-1]]),
    # X para as duas curvas (x, x em ordem reversa)
    y = np.concatenate([eixo_tauji_limites, minimo[::-1]]),
    # Y da curva superior seguido da curva inferior em ordem reversa
    fill = 'toself',  # Preencher a área entre as curvas
    fillcolor = 'rgba(0, 100, 255, 0.5)',  # Cor do preenchimento (azul com transparência)
    line = dict(color='rgba(255, 255, 255, 0)'),  # Linha invisível
    name = 'Região Homogênea',
    showlegend = True  # Não mostrar na legenda
  ))

  # Preenchendo a área entre as curvas. Área Superior
  fig.add_trace(go.Scatter(
    x = np.concatenate([eixo_tauij_fronteira, eixo_tauij_fronteira[::-1]]),
    # X para as duas curvas (x, x em ordem reversa)
    y = np.concatenate([maximo, eixo_tauji_limites[::-1]]),
    # Y da curva superior seguido da curva inferior em ordem reversa
    fill = 'toself',  # Preencher a área entre as curvas
    fillcolor = 'rgba(255, 0, 0, 0.5)',  # Cor do preenchimento (azul com transparência)
    line = dict(color='rgba(255, 255, 255, 0)'),  # Linha invisível
    name = 'Região Heterogênea',
    showlegend = True  # Não mostrar na legenda
  ))

  # Adicionando o título e configurando os eixos
  fig.update_layout(
    plot_bgcolor = 'white',
    title = {
      'text': f"{titulo}",
      'y': 0.9,  # Posição horizontal (0=esquerda, 1=direita)
      'x': 0.5,  # Posição vertical (0=embaixo, 1=em cima)
      'xanchor': 'center',
      'yanchor': 'top',
      'font': {'size': 20, 'family': 'Arial', 'color': 'black', 'weight': 'bold'}
    },

    xaxis = {
      'title': "Tau ij",
      'tickformat': '.0f'},

    yaxis = {
      'title': "Tau ji",
      'tickformat': '.0f'},

    font = {
      'family': 'Arial',
      'size': 18,
      'color': 'black'},
  )

  # Mostrando o gráfico
  return fig


def Grafico_Par_Binario(EixoX, EixoG, Titulo, Nome_Par = "Nenhum",
                        cor = "black", legenda = False, eixos = ("X1", "GM / RT")):
  """
  Função que retorna o gráfico da Energia de Gibbs do par binário


  Parâmetros
  -------------
  EixoX: narray (n,):
      Valores para a composição do componente 1

  EixoG: narray (n,):
      Valores para a energia livre de gibbs da mistura

  Titulo: str:
      Título do gráfico

  Nome_Par: str = "Par Binário":
      Nome do par binário

  cor: str = "black":
      Cor do gráfico

  legenda: Booleano = False:
      Se True, mostra a legenda do gráfico

  eixos: tuple = ("X1", "GM / RT"):
      Título dos eixos do gráfico

  Retorna
  -------------
  Gráfico da Energia de Gibbs do par binário
  """

  fig = go.Figure()

  # para linhas com marcas precisamos: 'lines + markers'
  if Nome_Par != "Nenhum":
    fig.add_trace(go.Scatter(x=EixoX, y=EixoG, mode='lines', name= Nome_Par))

    fig.update_layout(legend=dict(
      x=0.8,  # Posição horizontal (0=esquerda, 1=direita)
      y=0.1,  # Posição vertical (0=embaixo, 1=em cima)
      bgcolor='rgba(255, 255, 255, 0.5)',  # Fundo da legenda vermelho, verde, azul e transparência
      bordercolor='black',  # Cor da borda
      borderwidth=2  # Largura da borda
    ), showlegend=True)

  else:
    fig.add_trace(go.Scatter(x=EixoX, y=EixoG, mode='lines'))

  fig.update_layout(
    width=800, height=600, plot_bgcolor='white',
    title={
      'text': f"{Titulo}",
      'y': 0.9,  # Posição horizontal (0=esquerda, 1=direita)
      'x': 0.5,  # Posição vertical (0=embaixo, 1=em cima)
      'xanchor': 'center',
      'yanchor': 'top',
      'font': {'size': 20, 'family': 'Arial', 'color': 'black', 'weight': 'bold'}
    },

    xaxis={
      'title': f"{eixos[0]}",
      'range': [0, 1],
      'tickformat': '.1f'},

    yaxis={
      'title': f"{eixos[1]}",
      'tickformat': '.1f'},

    font={
      'family': 'Arial',
      'size': 18,
      'color': 'black'},

    colorway=[f"{cor}"]
  )

  fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray', showline=True, linecolor='black')
  fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray', showline=True, linecolor='black')


  return fig


def Malha_Superficie(alfa, tau, n_pontos = 100):
  """
  Função que retorna a malha da Superfície para o gráfico de superfície do
  par binário

  Parâmetros
  -------------
  T: float:
      Temperatura (K)

  alfa_binario: narray (3, 3):
      Parâmetro de não aleatoriedade

  tau_binario: narray (3, 3):
      Parâmetro de interação binária

  n_pontos: int:
      Quantidade de pontos na malha

  Retorna
  -------------
  (X1, X2, deltaG_ij)
  Tupla com os eixos da malha do gráfico de superfície
  """

  # Quantidade de pontos na nossa malha. Indo de 1 até 0
  limites = np.linspace(1, 0, n_pontos)

  # Malha das composições X1 e X2
  X1,X2 = np.meshgrid(limites, 1-limites)

  ########### Preparando o vetor da Energia de Gibbs ##############

  # Armazenas todos os valores da energia de gibbs
  deltaG_ij = []

  # Percorrendo os arrays
  for i in range(len(X1)):

    # Armazena os valores de delta G, em cada iteração de i
    deltaG_i = []

    # Olhando os valores
    for j in range(len(X1[i])):
      valor_x1 = X1[i][j]
      valor_x2 = X2[i][j]

      # Soma das composições
      soma = valor_x1 + valor_x2

      # Para composições que não possuem sentido, Não é atribuído um valor para G
      if soma > 1:
        delta_G = np.nan

      # Naqueles que fazem sentido, calculamos o valor de delta G
      else:
        # Valor do componente 3
        valor_x3 = 1 - valor_x1 - valor_x2

        # Composição de X1, X2 e X3
        x = [valor_x1, valor_x2, valor_x3]

        # Calculamos a energia de gibbs da mistura
        delta_G = DeltaG_Mistura(x, alfa, tau, mostrar = False, n_componentes = 3)

      # Final loop j
      deltaG_i.append(delta_G)

    # Final do loop i, adicionamos os valores na lista final
    deltaG_ij.append(deltaG_i)

  # Transforma em um array a lista
  deltaG_ij = np.array(deltaG_ij)

  # Retorna os eixos da malha do gráfico
  return (X1, X2, deltaG_ij)



def Eixo_Tie_lines(alfa, tau, comp_extrato, comp_rafinado):
  """
  Função que retorna os eixos para o gráfico 3d das tie-lines experimentais

  Parâmetros
  -------------
  T: float:
      Temperatura (K)

  alfa_binario: narray (3, 3):
      Parâmetro de não aleatoriedade

  tau_binario: narray (3, 3):
      Parâmetro de interação binária

  comp_extrato: narray (3, n):
      Composição da Tie-line na fase de extrato

  comp_rafinado: narray (3, n):
      Composição da Tie-line na fase de rafinado

  n_pontos: int:
      Quantidade de pontos na malha

  Retorna
  -------------
  (x1, x2, deltaG) -- x1[2, n], x2[2, n], deltaG[2, n]
  Tupla com os eixos do graficos 3d
  """

  ########### Preparando o vetor da Energia de Gibbs ##############

  # Eixos das composições do tipo [x1_extrato, x1_rafinado]
  eixo_x_1 = []
  # Eixos das composições do tipo [x2_extrato, x2_rafinado]
  eixo_x_2 = []
  # Armazenas todos os valores da energia de gibbs do tipo [energia_extrato, energia_rafinado]
  eixo_delta_G = []

  # Percorrendo cada uma das tie-lines
  for i in range(len(comp_extrato)):

    # Composições da tie-line "i", do tipo [x1, x2, x3]
    x_extrato = comp_extrato[i]
    x_rafinado = comp_rafinado[i]

    # Cálculo da energia de gibbs da composição dada
    delta_G_extrato = DeltaG_Mistura(x_extrato, alfa, tau, mostrar = False, n_componentes = 3)
    delta_G_rafinado = DeltaG_Mistura(x_rafinado, alfa, tau, mostrar = False, n_componentes = 3)

    # Atualização dos eixos
    eixo_x_1.append([x_extrato[0], x_rafinado[0]])
    eixo_x_2.append([x_extrato[1], x_rafinado[1]])
    eixo_delta_G.append([delta_G_extrato, delta_G_rafinado])


  # Transforma as listas em array
  eixo_x_1 = np.array(eixo_x_1)
  eixo_x_2 = np.array(eixo_x_2)
  eixo_delta_G = np.array(eixo_delta_G)

  # Retornamos os dados
  return (eixo_x_1, eixo_x_2, eixo_delta_G)



def Grafico_Superficie(x1, x2, deltaG, titulo, limitesG = "Nenhum", tamanho_fig = (1000, 600),
                       tupla_tie_line = None, transparencia = 0.9):

  """
  Função que retorna o gráfico da Energia de Gibbs do par binário

  Parâmetros
  -------------
  x1: narray (n,n):
      Malha do eixo X1

  x2: narray (n,n):
      Malha do eixo X2

  deltaG: narray (n,n):
      Malha da Energia de Gibbs

  titulo: str:
      Título do gráfico

  limitesG: tuple = (-0.6, 0.2):
      Limites do eixo Z (Energia de Gibbs) do gráfico

  tamanho_fig: tuple = (15,15):
       Largura, altura da imagem, em polegadas.

  tupla_tie_line: tuple = (x1, x2, deltaG):
      Tupla com os eixos das tie-lines experimentais

  transparencia: float = 0.7:
      Transparência do gráfico de superfície

  Retorna
  -------------
  Gráfico de superfície da Energia de Gibbs do par binário
  """

  # Se algum valor foi passado para as tie-lines
  if tupla_tie_line != None:
    x1_tieline, x2_tieline, deltaG_tieline = tupla_tie_line

    cores = ['red', 'blue', 'green', 'purple', 'orange', 'yellow', 'black', 'brown', 'cyan', 'pink']

    data = []

    data_s = go.Surface(
      x = x1,
      y = x2,
      z = deltaG,
      colorscale = 'jet',
      opacity = transparencia,
      showscale = False)

    # Adicionamos a data da superficie
    data.append(data_s)

    for i in range( len(x1_tieline) ):
      data_p = go.Scatter3d(
        x = x1_tieline[i],
        y = x2_tieline[i],
        z = deltaG_tieline[i],
        marker = dict(
          size = 5,
          color = cores[i],
          opacity = 1),
        name = f"Tie-line #{i + 1}",
        line = dict(color = cores[i], width = 5),
        showlegend = True
      )

      data.append(data_p)

  # Caso não tenhamos Tie-lines
  else:
    data =  go.Surface(
        x = x1,
        y = x2,
        z = deltaG,
        colorscale = 'jet',
        opacity = transparencia,
        showscale = False)

  # Criação da Figura
  fig = go.Figure(data = data)


  # Superfície 3d TENHAM sido passado limites
  if limitesG != "Nenhum" and limitesG != None:

    fig.update_layout(
      width = tamanho_fig[0], height = tamanho_fig[1],

      margin = dict(r=20, l=10, b=10, t=10),

      paper_bgcolor = "#FFFAFA",

      legend = dict(font = dict(size=15)),

      title = {
        'text': f"{titulo}",
        'y': 0.9,  # Posição horizontal (0=esquerda, 1=direita)
        'x': 0.5,  # Posição vertical (0=embaixo, 1=em cima)
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'size': 20, 'family': 'Arial', 'color': 'black', 'weight': 'bold'}
      },

      # Titulo dos eixos

      scene={
        'xaxis_title': 'X1',
        'yaxis_title': 'X2',
        'zaxis_title': 'GM/RT',

        'xaxis': {
          'nticks': 10,
          'range': [0, 1],
          'backgroundcolor': 'rgb(200, 200, 230)',
          'gridcolor': "white"},

        'yaxis': {
          'nticks': 10,
          'range': [0, 1],
          'backgroundcolor': 'rgb(230, 200,230)',
          'gridcolor': "white"},

        'zaxis': {
          'nticks': 10,
          'range': [limitesG[0], limitesG[1]],
          'backgroundcolor': 'rgb(230, 230,200)',
          'gridcolor': "white"}
      },

      # Visão inicial
      scene_camera_eye=dict(x=2, y=2, z=1),

      font={
        'family': 'Arial',
        'size': 12,
        'color': 'black'},

    )

  # Caso NÃO TENHAM sido passado os limites
  else:
    fig.update_layout(
      width = tamanho_fig[0], height = tamanho_fig[1],

      margin = dict(r=20, l=10, b=10, t=10),

      paper_bgcolor = "#FFFAFA",

      legend = dict(font=dict(size=15)),

      title = {
        'text': f"{titulo}",
        'y': 0.9,  # Posição horizontal (0=esquerda, 1=direita)
        'x': 0.5,  # Posição vertical (0=embaixo, 1=em cima)
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'size': 20, 'family': 'Arial', 'color': 'black', 'weight': 'bold'}
      },

      # Titulo dos eixos

      scene={
        'xaxis_title': 'X1',
        'yaxis_title': 'X2',
        'zaxis_title': 'GM/RT',

        'xaxis': {
          'nticks': 10,
          'range': [0, 1],
          'backgroundcolor': 'rgb(200, 200, 230)',
          'gridcolor': "white"},

        'yaxis': {
          'nticks': 10,
          'range': [0, 1],
          'backgroundcolor': 'rgb(230, 200,230)',
          'gridcolor': "white"},

        'zaxis': {
          'nticks': 10,
          'backgroundcolor': 'rgb(230, 230,200)',
          'gridcolor': "white"}
      },

      # Visão inicial
      scene_camera_eye=dict(x=2, y=2, z=1),

      font={
        'family': 'Arial',
        'size': 12,
        'color': 'black'},
    )

  return fig
