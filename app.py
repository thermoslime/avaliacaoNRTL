# Importando as bibliotecas
from dash import Dash, html, dcc, State, no_update
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash

# Usado na manipulação de matrizes
import numpy as np

# Usada para fazer download do csv
import pandas as pd

# Usada em alguns Callbacks
from dash.exceptions import PreventUpdate

# Importando as funções para os gráficos
from oficial.NRTL import Malha_Superficie, Grafico_Superficie, DeltaG_Mistura_par_binario, Grafico_Par_Binario, Fronteira_Tauij, df_tielines, Eixo_Tie_lines, tabela_eixo_tielines

# Importando os dados relativos ao caso 1
from oficial.Set_dados_Exemplo import caso_1_inconsistente, caso_1_consistente, frac_molar_1_extrato, frac_molar_1_rafinado

# Importando os dados relativos ao caso 2
from oficial.Set_dados_Exemplo import caso_2_inconsistente, caso_2_consistente, fracao_molar_caso_2_extrato, fracao_molar_caso_2_rafinado

########### VARIÁVEIS ####################
colors = {
    'fundo': '#FFFFFF',
    'texto': '#140903',
    'destaque': '#FF6961',
    'botao': '#0F00FF',
}

# Constante dos gases ideais
R = 8.314 #J/molK



# Preparando os eixos das composições para os gráficos 2d
eixo_x = np.linspace(0, 1, 200)

# Preparando a lista com as composição x1 e x2. [[x1, x2], [x1, x2], ...]
eixo_xy = []

# Para cada composição x1, calculamos um x2 e adicionamos na lista "eixo_xy"
for i in eixo_x:
  eixo_xy.append([i, 1-i])

# Transformamos a lista em um array
eixo_xy = np.array(eixo_xy)



# Gráfico vazio, usado para quando não termos nenhum dado
grafico_vazio =  {'data': [], 'layout': {
    'xaxis': {'title': 'Eixo X'},
    'yaxis': {'title': 'Eixo Y'},
    'title': 'Clique no botão para gerar o gráfico'
}}


############################################

# Inicializando o aplicativo
app = Dash(__name__, external_stylesheets= [dbc.themes.BOOTSTRAP], suppress_callback_exceptions = True, use_pages=True)
server = app.server

############ principal ################

# Layout principal
app.layout = dbc.Container([

    html.Div(style = {'backgroundColor': colors['fundo']}, children =
    [

    # Linha do título
    dbc.Row([
        
        # Titulo
        html.H2(
            children = 'Análise de dados de sistemas térnários ELL',
            style={
                'textAlign': 'center',
                'color': colors['texto']
                  }
            ),
        
        # Subtitulo
        html.H3(children='Baseada na Interface ALGMCal_TieLinesLL, de A. Marcilla et al.', style={
            'textAlign': 'center',
            'color': colors['texto']
             }),

        html.Hr(),
        html.Br()
    ]),

    # Linha de Links
    dbc.Row([
        dbc.Container( children = [

            dcc.Link(f"Inicial", id = "Link_inicial",href = "/", className = "btn btn-success m-2 fs-5"),
            # Tooltip apresenta uma dica em relação a pagina
            dbc.Tooltip(
                "Página Inicial, apresentando o aplicativo e a teoria !", 
                target="Link_inicial"
                        ),


            dcc.Link(f"Registro de dados", id = "Link_dados" , href = "/pages/tela_dados",  className = "btn btn-success m-2 fs-5"),

            dbc.Tooltip(
                "Página para inserir dados do sistema. Habilita os gráficos !",
                target="Link_dados"
                        ),

            # Link desabilitado, até algum dado seja cadastrado
            dcc.Link(f"Curvas de Gm", id = "Link_2d", href = "/pages/tela_graficos_binarios",
                     className="btn btn-default m-2 fs-5", style={'pointer-events': 'none', 'color': 'gray'}),

            dbc.Tooltip(
                "Visualização das curva de gM para cada par binário. Habilitado em 'Registro Dados' !",
                target="Link_2d"
            ),



            # Link desabilitado, até algum dado seja cadastrado
            dcc.Link(f"Superfície Gm/RT", id = "Link_3d", href = "/pages/tela_grafico3d",
                     className="btn btn-default m-2 fs-5", style={'pointer-events': 'none', 'color': 'gray'}),

            dbc.Tooltip(
                "Visualização da superfície de gM. Habilitado em 'Registro Dados' !",
                target="Link_3d"
            ),

        ]
    )],  style={"justify-content": "center"}),

    html.Hr(),

    # Local onde as páginas serão mostradas
    dbc.Row(dash.page_container,  justify="between"),
    ]),

    # Armazena as variáveis "ocultas" que será usada para os gráficos
    dcc.Store(id = 'A',  storage_type = 'session'), # Armazena Aij
    dcc.Store(id = 'Alfa',  storage_type = 'session'), # Armazena Alfa
    dcc.Store(id = 'Tau',  storage_type = 'session'), # Armazena Alfa

    dcc.Store(id = 'Nomes',  storage_type = 'session'), # Armazena os nomes

    dcc.Store(id = 'Temperatura_Armazenamento', storage_type = 'session'), # Armazena a temperatura em K

    dcc.Store(id = 'eixos_3d', storage_type = 'session'), # tupla com os eixos 3d

    dcc.Store(id = 'eixos_2d', storage_type = 'session'), #Tupla com os eixos 1-2, 1-3 e 2-3

    dcc.Store(id = 'tie_lines', storage_type = 'session'), # Tupla com tie_line1, tie_line2
    dcc.Store(id = 'dataframe_tielines', storage_type = 'session'), #dataframe com os dados importados
    dcc.Store(id = 'eixo_3d_tielines', storage_type = 'session'), # Tupla do tipo (x1, x2, energia)
    dcc.Store(id = 'escolha_calculo_tieline', storage_type = 'session'), # Se True, calculamos a energia da tie_line

],fluid=True)





##################### CALLBACKS PRINCIPAL #####################

# Callback para habilitar o link
@app.callback(
    Output(component_id= 'Link_3d', component_property= 'style'),
    Output(component_id= 'Link_3d',  component_property= 'className'),

    Output(component_id= 'Link_2d', component_property= 'style'),
    Output(component_id= 'Link_2d', component_property= 'className'),


    Input('A', 'data'),
    Input('Alfa', 'data'),
    Input('Tau', 'data')
)
def update_link(A, Alfa, Tau):

    # Se tivermos algum dado armazenado
    if  (A != "erro" and Alfa != "erro" and Tau != "erro") and ( A != None and Alfa != None and Tau != None) :
        # Botão 3d
        estilo_1 = {'pointer-events': 'auto'}
        classe_1 = "btn btn-success m-2 fs-5"

        # Botão das curvas
        estilo_2 = {'pointer-events': 'auto'}
        classe_2 = "btn btn-success m-2 fs-5"

        return estilo_1, classe_1, estilo_2, classe_2

    # Se não tivermos nada armazenado
    else:
        # Botão 3d
        estilo_1 = {'pointer-events': 'none', 'color': 'gray'}
        classe_1 = "btn btn-default m-2 fs-5"

        # Botão 2d
        estilo_2 = {'pointer-events': 'none', 'color': 'gray'}
        classe_2 = "btn btn-default m-2 fs-5"

        return estilo_1, classe_1, estilo_2, classe_2



##################### CALLBACKS DADOS #####################
# Alterar para um set específico
@app.callback(
    # Recebendo os valores na tela
    Output(component_id='nome_1', component_property='value'),
    Output(component_id='nome_2', component_property='value'),
    Output(component_id='nome_3', component_property='value'),

    Output(component_id='MM_1', component_property='value'),
    Output(component_id='MM_2', component_property='value'),
    Output(component_id='MM_3', component_property='value'),

    Output(component_id='A_1_2', component_property='value'),
    Output(component_id='A_1_3', component_property='value'),

    Output(component_id='A_2_1', component_property='value'),
    Output(component_id='A_2_3', component_property='value'),

    Output(component_id='A_3_1', component_property='value'),
    Output(component_id='A_3_2', component_property='value'),

    Output(component_id='Alfa_1_2', component_property='value'),
    Output(component_id='Alfa_1_3', component_property='value'),
    Output(component_id='Alfa_2_3', component_property='value'),

    Output(component_id='Temperatura', component_property='value'),
    Output(component_id='TemperaturaUnidade', component_property='value'),

    Input(component_id='Drop_dados', component_property='value'),
)
def sets_dinamicos(escolha):

    # Caso a escolha não seja personalizadas
    if escolha != "Personalizado":
        # Pegando os valores nos sets cadastrados

        if escolha == "Caso 1: Inconsistente":
            dicionario = caso_1_inconsistente

        elif escolha == "Caso 1: Consistente":
            dicionario = caso_1_consistente

        elif escolha == "Caso 2: Inconsistente":
            dicionario = caso_2_inconsistente

        else:
            dicionario = caso_2_consistente


        nome_1 = dicionario["nome_1"]
        nome_2 = dicionario["nome_2"]
        nome_3 = dicionario["nome_3"]

        mm1 =  dicionario["MM_1"]
        mm2 =  dicionario["MM_2"]
        mm3 =  dicionario["MM_3"]

        A12 = dicionario["A12"]
        A13 = dicionario["A13"]

        A21 = dicionario["A21"]
        A23 = dicionario["A23"]

        A31 = dicionario["A31"]
        A32 = dicionario["A32"]

        Alfa12 = dicionario["Alfa12"]
        Alfa13 = dicionario["Alfa13"]
        Alfa23 = dicionario["Alfa23"]

        temperatura = dicionario["temperatura"]

        return  (nome_1,nome_2,nome_3,
                 mm1, mm2, mm3,
                 A12,A13,
                 A21,A23,
                 A31,A32,
                 Alfa12,Alfa13,Alfa23,
                 temperatura, "K")

    # Se escolhermos o personalizado
    else:
        raise PreventUpdate



# Alterando a habilitação de edição dependendo do set específico
@app.callback(
    # Recebendo os valores na tela
    Output(component_id='nome_1', component_property='disabled'),
    Output(component_id='nome_2', component_property='disabled'),
    Output(component_id='nome_3', component_property='disabled'),

    Output(component_id='A_1_2', component_property='disabled'),
    Output(component_id='A_1_3', component_property='disabled'),

    Output(component_id='A_2_1', component_property='disabled'),
    Output(component_id='A_2_3', component_property='disabled'),

    Output(component_id='A_3_1', component_property='disabled'),
    Output(component_id='A_3_2', component_property='disabled'),

    Output(component_id='Alfa_1_2', component_property='disabled'),
    Output(component_id='Alfa_1_3', component_property='disabled'),
    Output(component_id='Alfa_2_3', component_property='disabled'),

    Output(component_id='Temperatura', component_property='disabled'),
    Output(component_id='TemperaturaUnidade', component_property='disabled'),

    Input(component_id='Drop_dados', component_property='value'),

)
def sets_dinamicos_inalterar(escolha):
    # com False, podemos editar, se for True não podemos
    # Caso a escolha não seja personalizadas
    if escolha != "Personalizado":
        opcao = False
        return  opcao, opcao, opcao, opcao, opcao, opcao, opcao, opcao, opcao, opcao, opcao, opcao, opcao, opcao,

    else:
        opcao = False
        return opcao, opcao, opcao, opcao, opcao, opcao, opcao, opcao, opcao, opcao, opcao, opcao, opcao, opcao,


# Desabilitando o indice de tie-lines
@app.callback(
    # Recebendo os valores na tela
    Output(component_id='Escolha_Tieline', component_property='options'),
    Output(component_id='Escolha_Tieline', component_property='value'),

    Input(component_id='Drop_dados', component_property='value'),

)
def sets_dinamicos_tielines(escolha):
    # com False, podemos editar, se for True não podemos
    # Caso a escolha não seja personalizadas
    if escolha == "Personalizado":
        opcoes = [
                    {'label': 'Adicionar', 'value': 'Sim', 'disabled': False}, 
                    {'label': 'Não Adicionar', 'value': 'Não', 'disabled': False}
                    ]
        
        valor = 'Não'

    else:
        opcoes = [
                    {'label': 'Adicionar', 'value': 'Sim', 'disabled': True}, 
                    {'label': 'Não Adicionar', 'value': 'Não', 'disabled': True}
                    ]
        
        valor = 'Sim'
    
    return opcoes, valor



# Para cadastrar os valores novos, realizando os Cálculos
@app.callback(
    # Output para cadastrar e mostrar valores
    Output(component_id='Tabela', component_property='children', allow_duplicate = True),

    Output(component_id= 'A',  component_property='data'),
    Output(component_id= 'Alfa',  component_property='data'),
    Output(component_id= 'Tau',  component_property='data'),

    Output(component_id= 'Nomes',  component_property='data'),

    Output(component_id= 'Temperatura_Armazenamento',  component_property='data'),

    Output(component_id= 'eixos_3d',  component_property='data'),
    Output(component_id='eixos_2d', component_property='data'),
    Output(component_id='eixo_3d_tielines', component_property='data'),

    # Recebendo os valores na tela
    State(component_id='nome_1', component_property='value'),
    State(component_id='nome_2', component_property='value'),
    State(component_id='nome_3', component_property='value'),

    State(component_id='UnidadeAij', component_property='value'),

    State(component_id='A_1_2', component_property='value'),
    State(component_id='A_1_3', component_property='value'),

    State(component_id='A_2_1', component_property='value'),
    State(component_id='A_2_3', component_property='value'),

    State(component_id='A_3_1', component_property='value'),
    State(component_id='A_3_2', component_property='value'),


    State(component_id='Alfa_1_2', component_property='value'),
    State(component_id='Alfa_1_3', component_property='value'),
    State(component_id='Alfa_2_3', component_property='value'),


    Input(component_id='Botao_tabela', component_property='n_clicks'),

    State(component_id='Temperatura', component_property='value'),
    State(component_id='TemperaturaUnidade', component_property='value'),

    State(component_id = 'tie_lines', component_property = 'data'), #frac_molar_1_extrato, frac_molar_1_rafinado
    State(component_id = 'escolha_calculo_tieline', component_property='data'),

    # Não será chamado automaticamento no inicio
    prevent_initial_call = True

)
def Calculos_tabela(nome1, nome2, nome3,
                  unidade_Aij,
                  a12, a13,
                  a21, a23,
                  a31, a32,
                  alfa12, alfa13, alfa23,
                  n_click_tabela,
                  T, T_unidade,
                  tielines, escolha_tieline):

    # Testando os valores, se estão corretos
    if n_click_tabela > 0:
        try:
            a_12 = float(a12.strip())
            a_13 = float(a13.strip())

            a_21 = float(a21.strip())
            a_23 = float(a23.strip())

            a_31 = float(a31.strip())
            a_32 = float(a32.strip())

            alfa_12 = float(alfa12.strip())
            alfa_13 = float(alfa13.strip())
            alfa_23 = float(alfa23.strip())

            temperatura = float(T.strip())

            valor = 'Ok'

            A_ij = np.array([
                [0,    a_12,    a_13],
                [a_21, 0,       a_23],
                [a_31, a_32,    0]
            ])

            Alfa_ij = np.array([
                [0,       alfa_12, alfa_13],
                [alfa_12, 0,       alfa_23],
                [alfa_13, alfa_23, 0]
            ])

            # Cálculo de tau_ij
            if unidade_Aij == 'J/mol':
                # Cálculo de Tau, dependendo da unidade de temperatura
                if T_unidade == 'K':
                    temperatura_nova = temperatura
                    tau_ij = A_ij / (R * temperatura_nova) # Adimensional


                elif T_unidade == '°C':
                    temperatura_nova = temperatura + 273.15
                    tau_ij = A_ij / (R * temperatura_nova )  # Adimensional


                elif T_unidade == '°F':
                    temperatura_nova = (temperatura + 459.67) / 1.8
                    tau_ij = A_ij / (R * temperatura_nova)  # Adimensional

                else:
                    tau_ij = 'erro'
                    temperatura_nova = 'erro'


            else:
                tau_ij = 'erro'
                temperatura_nova = 'erro'

        # Se os dados forem errados
        except Exception as error:
            #print(error)
            valor = 'erro'
            A_ij = 'erro'
            Alfa_ij = 'erro'
            tau_ij = 'erro'
            temperatura_nova = 'erro'

        # Valores deram erro em alguma etapa
        if valor == 'erro':
            aviso = dcc.Markdown(children = '''
            Erro, alguma das entradas inseridas está errada, verifique se não esqueceu de trocar Vírgula por Ponto final
            (1,20 -> 1.20), ou se possui algum espaço em branco entre os número (1,  20 -> 1.2).''', style={'textAlign': 'justify',}),

            return aviso, A_ij, Alfa_ij, tau_ij, (nome1, nome2, nome3), temperatura_nova, (None, None, None), (None, None, None), None

        # Caso não tenha nenhum erro
        else:

            ########### CÁLCULO DOS EIXOS ################
            # Cálculo dos eixos 3d
            eixo_x, eixo_y, eixo_z = Malha_Superficie(Alfa_ij, tau_ij, 5)

            # Cálculo dos eixos 2d
            eixo_12_G = DeltaG_Mistura_par_binario(eixo_xy, Alfa_ij, tau_ij, par = '1-2', mostrar = False)
            eixo_13_G = DeltaG_Mistura_par_binario(eixo_xy, Alfa_ij, tau_ij, par = '1-3', mostrar = False)
            eixo_23_G = DeltaG_Mistura_par_binario(eixo_xy, Alfa_ij, tau_ij, par = '2-3', mostrar = False)

            #se for para calcular as tie_lines
            if escolha_tieline:
                # Tupla do tipo (x1, x2, energia)
                tupla_tie_lines = Eixo_Tie_lines(Alfa_ij, tau_ij, tielines[0], tielines[1])

            #Se não for para calcular as tie_lines
            else:
                tupla_tie_lines = None




            ########### MOSTRANDO OS RESULTADOS ################
            # Mostramos a tabela
            tabela =  html.Div([

                dcc.Markdown(children='''
                Os botões para os gráficos estão LIBERADOS !!''',
                style={'textAlign': 'justify', }),

                html.Br(),

                # Tabela mostrando Aij
                dbc.Table([
                    html.Tbody([
                        html.Tr([html.Th(f'A_ij [{unidade_Aij}]'), html.Th(f'{nome1}'), html.Th(f'{nome2}'), html.Th(f'{nome3}')]),

                        html.Tr([html.Td(f'{nome1}'),
                                 html.Td([
                                     html.Label(children = f'{A_ij[0][0]}', style={'width': '100px', 'textAlign': 'center'})
                                     ]),
                                 html.Td([
                                     html.Label(children = f'{A_ij[0][1]}', style={'width': '100px', 'textAlign': 'center'})
                                     ]),
                                 html.Td([
                                     html.Label(children = f'{A_ij[0][2]}', style={'width': '100px', 'textAlign': 'center'})
                                     ]),
                                ]),

                        html.Tr([html.Td(f'{nome2}'),
                                 html.Td([
                                     html.Label(children = f'{A_ij[1][0]}', style={'width': '100px', 'textAlign': 'center'})
                                     ]),
                                 html.Td([
                                     html.Label(children = f'{A_ij[1][1]}', style={'width': '100px', 'textAlign': 'center'})
                                     ]),
                                 html.Td([
                                     html.Label(children = f'{A_ij[1][2]}', style={'width': '100px', 'textAlign': 'center'})
                                     ]),
                                 ]),

                        html.Tr([html.Td(f'{nome3}'),
                                 html.Td([
                                     html.Label(children = f'{A_ij[2][0]}', style={'width': '100px', 'textAlign': 'center'})
                                     ]),
                                 html.Td([
                                     html.Label(children = f'{A_ij[2][1]}', style={'width': '100px', 'textAlign': 'center'})
                                     ]),
                                 html.Td([
                                     html.Label(children = f'{A_ij[2][2]}', style={'width': '100px', 'textAlign': 'center'})
                                     ]),
                                 ])
                    ])
                ], bordered=True ),

                html.Br(),

                # Tabela mostrando Tau
                dbc.Table([
                    html.Tbody([
                        html.Tr([html.Th(f'Tau_ij [Adimensional]'), html.Th(f'{nome1}'), html.Th(f'{nome2}'),
                                 html.Th(f'{nome3}')]),

                        html.Tr([html.Td(f'{nome1}'),
                                 html.Td([
                                     html.Label(children=f'{tau_ij[0][0]}',
                                                style={'width': '100px', 'textAlign': 'center'})
                                 ]),
                                 html.Td([
                                     html.Label(children=f'{tau_ij[0][1]:.2f}',
                                                style={'width': '100px', 'textAlign': 'center'})
                                 ]),
                                 html.Td([
                                     html.Label(children=f'{tau_ij[0][2]:.2f}',
                                                style={'width': '100px', 'textAlign': 'center'})
                                 ]),
                                 ]),

                        html.Tr([html.Td(f'{nome2}'),
                                 html.Td([
                                     html.Label(children=f'{tau_ij[1][0]:.2f}',
                                                style={'width': '100px', 'textAlign': 'center'})
                                 ]),
                                 html.Td([
                                     html.Label(children=f'{tau_ij[1][1]}',
                                                style={'width': '100px', 'textAlign': 'center'})
                                 ]),
                                 html.Td([
                                     html.Label(children=f'{tau_ij[1][2]:.2f}',
                                                style={'width': '100px', 'textAlign': 'center'})
                                 ]),
                                 ]),

                        html.Tr([html.Td(f'{nome3}'),
                                 html.Td([
                                     html.Label(children=f'{tau_ij[2][0]:.2f}',
                                                style={'width': '100px', 'textAlign': 'center'})
                                 ]),
                                 html.Td([
                                     html.Label(children=f'{tau_ij[2][1]:.2f}',
                                                style={'width': '100px', 'textAlign': 'center'})
                                 ]),
                                 html.Td([
                                     html.Label(children=f'{tau_ij[2][2]}',
                                                style={'width': '100px', 'textAlign': 'center'})
                                 ]),
                                 ])
                    ])
                ], bordered=True),

                html.Br(),

                tabela_eixo_tielines(tupla_tie_lines),

                html.Br(),

                # Botão de download
                dbc.Button(children="Download do CSV", id='Botao_download', n_clicks=0, outline=True, color="primary",
                           className="me-1"),
                dcc.Download(id="download_Resultados"),

            ], style={'width': '48%'})


            return tabela, A_ij, Alfa_ij, tau_ij, (nome1, nome2, nome3), temperatura_nova, (eixo_x, eixo_y, eixo_z), (eixo_12_G, eixo_13_G, eixo_23_G), tupla_tie_lines

    # Se o botão não for presionado
    else:
        return dash.no_update



# Mostrar os valores se já existir
@app.callback(
    # Output para cadastrar e mostrar valores
    Output(component_id='Tabela', component_property='children'),

    # Recebendo os valores na tela
    Input(component_id='Botao_tabela', component_property='n_clicks'),
    Input(component_id='UnidadeAij', component_property='value'),

    # Verificar se existe valores já cadastrados
    Input(component_id='A', component_property='data'),
    Input(component_id='Tau', component_property='data'),

    Input(component_id='Nomes', component_property='data'),

)
def mostrar_tabela(n_click_tabela, unidade_Aij,
                  Aij_matriz, Tauij_matriz,
                  Nomes_matriz):

    #print("Mostrando tabela, se existir.")

    # Caso exista valores já cadastrados e o botão não foi pressionado.
    if Aij_matriz is not None and Aij_matriz != "erro" and n_click_tabela == 0:
        #print(Aij_matriz )
        # Mostramos a tabela
        tabela = html.Div([

            dcc.Markdown(children='''
                       Os botões para os gráficos estão LIBERADOS !!''',
                         style={'textAlign': 'justify', }),

            html.Br(),

            # Tabela mostrando Aij
            dbc.Table([
                html.Tbody([
                    html.Tr([html.Th(f'A_ij [{unidade_Aij}]'), html.Th(f'{Nomes_matriz[0]}'), html.Th(f'{Nomes_matriz[1]}'),
                             html.Th(f'{Nomes_matriz[2]}')]),

                    html.Tr([html.Td(f'{Nomes_matriz[0]}'),
                             html.Td([
                                 html.Label(children=f'{Aij_matriz[0][0]}', style={'width': '100px', 'textAlign': 'center'})
                             ]),
                             html.Td([
                                 html.Label(children=f'{Aij_matriz[0][1]}', style={'width': '100px', 'textAlign': 'center'})
                             ]),
                             html.Td([
                                 html.Label(children=f'{Aij_matriz[0][2]}', style={'width': '100px', 'textAlign': 'center'})
                             ]),
                             ]),

                    html.Tr([html.Td(f'{Nomes_matriz[1]}'),
                             html.Td([
                                 html.Label(children=f'{Aij_matriz[1][0]}', style={'width': '100px', 'textAlign': 'center'})
                             ]),
                             html.Td([
                                 html.Label(children=f'{Aij_matriz[1][1]}', style={'width': '100px', 'textAlign': 'center'})
                             ]),
                             html.Td([
                                 html.Label(children=f'{Aij_matriz[1][2]}', style={'width': '100px', 'textAlign': 'center'})
                             ]),
                             ]),

                    html.Tr([html.Td(f'{Nomes_matriz[2]}'),
                             html.Td([
                                 html.Label(children=f'{Aij_matriz[2][0]}', style={'width': '100px', 'textAlign': 'center'})
                             ]),
                             html.Td([
                                 html.Label(children=f'{Aij_matriz[2][1]}', style={'width': '100px', 'textAlign': 'center'})
                             ]),
                             html.Td([
                                 html.Label(children=f'{Aij_matriz[2][2]}', style={'width': '100px', 'textAlign': 'center'})
                             ]),
                             ])
                ])
            ], bordered=True),

            html.Br(),

            # Tabela mostrando Tau
            dbc.Table([
                html.Tbody([
                    html.Tr([html.Th(f'Tau_ij [Adimensional]'), html.Th(f'{Nomes_matriz[0]}'), html.Th(f'{Nomes_matriz[1]}'),
                             html.Th(f'{Nomes_matriz[2]}')]),

                    html.Tr([html.Td(f'{Nomes_matriz[0]}'),
                             html.Td([
                                 html.Label(children=f'{Tauij_matriz[0][0]}',
                                            style={'width': '100px', 'textAlign': 'center'})
                             ]),
                             html.Td([
                                 html.Label(children=f'{Tauij_matriz[0][1]:.2f}',
                                            style={'width': '100px', 'textAlign': 'center'})
                             ]),
                             html.Td([
                                 html.Label(children=f'{Tauij_matriz[0][2]:.2f}',
                                            style={'width': '100px', 'textAlign': 'center'})
                             ]),
                             ]),

                    html.Tr([html.Td(f'{Nomes_matriz[1]}'),
                             html.Td([
                                 html.Label(children=f'{Tauij_matriz[1][0]:.2f}',
                                            style={'width': '100px', 'textAlign': 'center'})
                             ]),
                             html.Td([
                                 html.Label(children=f'{Tauij_matriz[1][1]}',
                                            style={'width': '100px', 'textAlign': 'center'})
                             ]),
                             html.Td([
                                 html.Label(children=f'{Tauij_matriz[1][2]:.2f}',
                                            style={'width': '100px', 'textAlign': 'center'})
                             ]),
                             ]),

                    html.Tr([html.Td(f'{Nomes_matriz[2]}'),
                             html.Td([
                                 html.Label(children=f'{Tauij_matriz[2][0]:.2f}',
                                            style={'width': '100px', 'textAlign': 'center'})
                             ]),
                             html.Td([
                                 html.Label(children=f'{Tauij_matriz[2][1]:.2f}',
                                            style={'width': '100px', 'textAlign': 'center'})
                             ]),
                             html.Td([
                                 html.Label(children=f'{Tauij_matriz[2][2]}',
                                            style={'width': '100px', 'textAlign': 'center'})
                             ]),
                             ])
                ])
            ], bordered=True),

            # Botão de download
            dbc.Button(children="Download do CSV", id='Botao_download', n_clicks=0, outline=True, color="primary",
                       className="me-1"),

            dcc.Download(id="download_Resultados"),

        ], style={'width': '48%'})

        return tabela

    else:
        return dash.no_update






#################### DADOS TIE LINE #####################
# Para ativar a opção de tie-lines
@app.callback(
    # Output para armazenar os dados
    Output(component_id='Upload_tielines', component_property='disable_click'),
    Output(component_id='Upload_tielines', component_property='disable'),
    Output(component_id='Botao_tielines', component_property='disabled'),

    # Recebendo os dados
    Input(component_id='Escolha_Tieline', component_property='value'),
    Input(component_id='Drop_dados', component_property='value')
)
def ativar_tieline(escolha_ties, escolha_set):
    if escolha_ties == 'Sim' and escolha_set == "Personalizado":
        return False, False, False
    else:
        return True, True, True



# Para fazer a leitura do arquivo do upload
@app.callback(
    # Output para armazenar os dados
    Output(component_id = 'Conteudo_tieline', component_property = 'children'),
    Output(component_id = 'tie_lines', component_property = 'data'),
    Output(component_id = 'escolha_calculo_tieline', component_property= 'data'),

    # Recebendo os dados
    Input(component_id='Botao_tielines', component_property='n_clicks'),

    # Recebendo os dados
    Input(component_id='Escolha_Tieline', component_property='value'),

    Input(component_id='Upload_tielines', component_property='contents'),
    Input(component_id='Upload_tielines', component_property='filename'),

    Input(component_id='Drop_dados', component_property='value'),

    prevent_initial_call=True,
)
def registro_tieline(n_click_tieline, escolha_tieline, contente, nome, escolha_set):

    # Caso a opção de set é Personalizado
    if escolha_set == "Personalizado":
        # Caso não queiramos adicionar tie_lines
        if escolha_tieline == 'Não':
            mensagem = dcc.Markdown(children = '''
                Caso queira adicionar Tie-Lines escolha "Adicionar" nas opções iniciais para habilitar o botão.''', style={'textAlign': 'justify',}
                                ),

            return mensagem, None, False
        
        # Se for para adicionar alguma tie-line
        else:
            # Se o botão for clicado e já tiver algum valor cadastrado
            if contente != None:

                #tentamos atribuir o dataframe e array
                try:
                    df, tie_line1, tie_line2 = df_tielines(contente, nome)

                    mensagem = html.Div([
                        html.P('''Os dados foram carregados com sucesso''', style={'text-align': 'justify'}),
                    ])

                    return mensagem, (tie_line1, tie_line2), True

                # Se ocorrer algum erro na importação dos dados
                except:
                    mensagem = dcc.Markdown(children='''
                            Ocorreu um erro na importação dos dados !''',
                                            style={'textAlign': 'justify', } )

                    return mensagem, None, False

            elif n_click_tieline == 0 or contente == None:
                mensagem = "Nenhum valor adicionado"

                return mensagem, None, False
    

    # Se o caso não for personalizado
    else:
        mensagem = dcc.Markdown(children = '''
                Tie-lines carregadas com sucesso.''', style={'textAlign': 'justify',}
                                ),
        
        # Adicionamos as tie-lines para os casos 1
        if escolha_set == "Caso 1: Inconsistente" or escolha_set == "Caso 1: Consistente":
            tielines = (frac_molar_1_extrato, frac_molar_1_rafinado)
        
        # Se caso 2
        else:
            tielines = (fracao_molar_caso_2_extrato, fracao_molar_caso_2_rafinado)
    

        return mensagem, tielines, True






##################### CALLBACKS 2D #####################
@app.callback(
    Output(component_id='Graficos_2d_12', component_property='children'),
    Output(component_id='Graficos_2d_13', component_property='children'),
    Output(component_id='Graficos_2d_23', component_property='children'),
    Output(component_id='Graficos_2d_fronteira', component_property='children'),

    Input(component_id='Botao_2d', component_property = 'n_clicks'),
    Input(component_id='Checkbox_2d', component_property = 'value'),

    State(component_id= 'Nomes',  component_property='data'),
    State(component_id='eixos_2d', component_property = 'data'),
    State(component_id='Tau', component_property= 'data'),

    # Não será chamado automaticamento no inicio
    prevent_initial_call=True
)

def graficos_2d(n_click_2d, opcao, nomes, eixos, Tauij):

    if n_click_2d == 0:
        raise PreventUpdate

    else:
        # Caso nenhuma opção esteja selecionada
        if not opcao:
            aviso = dcc.Markdown(children = '''
            Nenhum par binário foi selecionado, por favor, escolha pelo menos um deles.''', style={'textAlign': 'justify',}
                             ),
            return aviso, '', '', ''

        # Caso tenha alguma selecionada
        else:

            if '1-2' in opcao:
                titulo = "Curva de Gm para o par binário"
                figura_12 = Grafico_Par_Binario(eixo_x, eixos[0], titulo, Nome_Par = f"{nomes[0]}(1) <br>{nomes[1]}(2)",
                                                cor = "black", legenda = False, eixos = ("X1", "GM / RT"))

                grafico_12 = dcc.Graph(figure = figura_12, style={'text-align': 'center'})
            else:
                grafico_12 = dcc.Markdown(children = "Par 1-2 NÃO foi selecionado", style={'textAlign': 'justify',})


            if '1-3' in opcao:
                titulo = "Curva de Gm para o par binário"
                figura_13 = Grafico_Par_Binario(eixo_x, eixos[1], titulo, Nome_Par=f"{nomes[0]}(1) <br>{nomes[2]}(3)",
                                                cor="blue", legenda=False, eixos=("X1", "GM / RT"))

                grafico_13 = dcc.Graph(figure = figura_13, style={'text-align': 'center'})
            else:
                grafico_13 = dcc.Markdown(children = '''Par 1-3 NÃO foi selecionado''',
                                         style={'textAlign': 'justify',})


            if '2-3' in opcao:
                titulo = "Curva de Gm para o par binário"
                figura_23 = Grafico_Par_Binario(eixo_x, eixos[2], titulo, Nome_Par=f"{nomes[1]}(2) <br>{nomes[2]}(3)",
                                                cor="green", legenda=False, eixos=("X2", "GM / RT"))

                grafico_23 = dcc.Graph(figure = figura_23, style={'text-align': 'center'})
            else:
                grafico_23 = dcc.Markdown(children = '''Par 2-3 NÃO foi selecionado''',
                                         style={'textAlign': 'justify',})

            if "Fronteira (Alfa < 0.43)" in opcao:
                titulo = "Fronteira de solubilidade para os parâmetros Aij <br> Para Alfa < 0.43 "
                figura_front = Fronteira_Tauij(Tauij, titulo)

                grafico_fronteira =  dcc.Graph(figure = figura_front, style={'text-align': 'center'})
            else:
                grafico_fronteira = dcc.Markdown(children='''Fronteira NÃO foi selecionada''',
                                          style={'textAlign': 'justify', })


            return grafico_12, grafico_13, grafico_23, grafico_fronteira






##################### CALLBACKS 3D #####################
@app.callback(
    Output(component_id = 'Grafico_3d', component_property = 'figure'),

    Input(component_id= 'Botao_Gerar_Grafico3d', component_property = 'n_clicks'),

    Input(component_id= 'eixos_3d',  component_property = 'data'),

    State(component_id= 'Titulo', component_property= 'value'),

    State(component_id= 'LimSup', component_property= 'value'),
    State(component_id='LimInf', component_property='value'),

    Input(component_id= 'Transparencia', component_property= 'value'),

    State(component_id='escolha_calculo_tieline', component_property='data'),
    State(component_id='eixo_3d_tielines', component_property='data'),

    # Não será chamado automaticamento no inicio
    prevent_initial_call=True

)
def mostrar_grafico(n_click_3d,
                    eixos,
                    titulo,
                    LimSup, LimInf,
                    transpa,
                    escolha_tieline, tupla_eixo_tieline):

    if n_click_3d > 0:
        # Avaliando se a entrada de dados está correta

        try:
            sup = float(LimSup.strip()) #strip() para retirar qualquer espaço no final
        except:
            sup = None

        try:
            inf = float (LimInf.strip())
        except:
            inf = None

        if escolha_tieline:
            fig = Grafico_Superficie(eixos[0], eixos[1], eixos[2], titulo, limitesG=(inf, sup), tamanho_fig=(1000, 600),
                                     tupla_tie_line = tupla_eixo_tieline, transparencia=transpa)

        else:
            fig =  Grafico_Superficie(eixos[0], eixos[1], eixos[2], titulo, limitesG = (inf, sup), tamanho_fig = (1000,600),
                                      tupla_tie_line = None, transparencia = transpa)
        return fig

    else:
        return grafico_vazio






################ DOWNLOAD DO CSV #################
@app.callback(
    Output(component_id = 'download_Resultados', component_property = 'data'),

    Input(component_id= 'Botao_download', component_property = 'n_clicks'),

    Input(component_id='Nomes', component_property='data'),


    Input(component_id='eixos_2d', component_property='data'),

    # Não será chamado automaticamento no inicio
    prevent_initial_call=True

)
def download_csv(n_click_download,
                 Nomes,
                 deltaG_2d):

    if n_click_download > 0:

        deltaG_12, deltaG_13, deltaG_23 = deltaG_2d
        eixo_y = 1 - eixo_x

        df_binario = pd.DataFrame({
            "x1_12":  eixo_x,
            "Delta G da mistura (12)": deltaG_12,
            "x1_13": eixo_x,
            "Delta G da mistura (13)": deltaG_13,
            "x3_23": eixo_y,
            "Delta G da mistura (23)": deltaG_23
        })
        return dcc.send_data_frame(df_binario.to_csv, "Dados.csv")


    else:
        raise PreventUpdate

# Tupla com os eixos 1-2, 1-3 e 2-3

# Final, executando
if __name__ == '__main__':
    app.run(debug=True)
