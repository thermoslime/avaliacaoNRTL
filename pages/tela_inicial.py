'''
Tela Inicial da aplicação
'''

# Importação das bibliotecas
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import dash

# Registro da página
dash.register_page( __name__, path="/", name = "Tela Inicial")

# Criando variáveis para cada seção do conteúdo


# Introdução
introducao = html.Div(id="introducao", children=[
    html.H2("Sobre a Aplicação"),

    html.P('''Essa aplicação WEB visa fornecer uma ferramenta online que permita executar a avaliação de consistência
           termodinâmica dos parâmetros binários do modelo NRTL, para um sistema ternário, de forma a verificar se os resultados obtidos pelo
           ajuste aos dados experimentais são coerentes.''', style={'text-align': 'justify'}),

    html.P([
        
        '''Junto com esse aplicativo, também está disponível a aplicação utilizando a plataforma Google Colaboratory, como uma
           alternativa para aqueles usuários que desejam visualizar a rotina cálculos e realizar a personalização de alguma função ou etapa do algoritmo. Basta acessar o notebook com uma conta Google atrvés do link: ''',
           
           html.A("Colab - Teste dos parâmetros NRTL.", href="https://colab.research.google.com/drive/1KoPzmLG3ChYOqUnL0U-Oi01xiPJBjrYO?usp=sharing", target="_blank"),

           ], style={'text-align': 'justify'}),

    html.P([
            
        '''Os trabalhos de A. Marcilla, et. al. foram tomados como base na elaboração das aplicações (Web e Colab), sendo o aplicativo 
           fornecido por ele (Uma interface gráfica elaborada usando Matlab) mais completo e abrangente do que as aplicações aqui fornecidas. O software  GMcal_TielinesLL está disponível em: ''', 

            
            html.A("GMcal_TieLinesLL: Graphical User Interface (GUI) for the Topological Analysis of Calculated GM Surfaces and Curves, including Tie-Lines, Hessian Matrix, Spinodal Curve, Plait Point Location, etc. for Binary and Ternary Liquid -Liquid Equilibrium (LLE) Data.", href="https://rua.ua.es/dspace/handle/10045/51725", target="_blank"),
    ], style={'text-align': 'justify'}
           ),
           

    

], style={"padding-top": "50px"})



# Como usar?
instrucao = html.Div(id="Instrucao", children=[
    html.H2("Como Usar?"),

    html.P('''Das etapas para a avaliação de um set de parâmetros de um sistema ternário, através dessa aplicação web, temos:.''', style={'text-align': 'justify'}),

    html.Ol([
        html.Li("Inserção dos dados (Parâmetros Binários, Nomes, Tielines) na aba 'Registro de dados', atentando-se para o uso de ponto (.) invés de vírgula (,);"),
        html.Li("Cadastro de dados no botão 'Cadastrar valores' (Com isso as abas para os gráficos dos pares binários e 3d ficaram disponíveis);"),
        html.Li("Navegação através das abas, para a geração dos dados;"),
        html.Li("Interação com os gráficos pode ser realizado com o mouse ou através dos botões (sendo possível a ocultação das tie-lines clicando na legenda.")
    ], style={'text-align': 'justify'}),

    html.P([
        '''Está disponível um vídeo tutorial, onde é mostrado os passos de uso desse aplicativo. Acesse: ''',

        html.A("Tutorial You Tube", href="https://youtu.be/9yYf2NIech0?si=lLgmL8mIqXrAEHS-", target="_blank"),
    ], style={'text-align': 'justify'}),

], style={"padding-top": "50px"})


# ELL
ELL = html.Div(id="ELL", children=[
    html.H2("Equilibrio Líquido Líquido (ELL)"),

    html.P('''O equilíbrio de fases acontece quando temos a existência de duas ou mais fases que apresentam uma ausência 
           dos gradientes de:''', style={'text-align': 'justify'}),

    html.Ul([
        html.Li("Temperatura"),
        html.Li("Pressão"),
        html.Li("Potencial Químico")
    ], style={'text-align': 'justify'}),

    html.P('''No processo de extração líquido-líquido, temos a adição de um composto, de forma a obter a formação de duas
           fases da solução homogênea inicial, que se caracteriza quando temos uma diminuição da Energia Livre de Gibbs 
           do sistema com as fases separadas.''', style={'text-align': 'justify'}),

    html.P('''Em um sistema ternário, temos inicialmente uma mistura binária (A e B), e ao adicionar um terceiro (C), 
           temos a separação de duas fases (I e II). Nessa situação temos as seguintes condições:''', style={'text-align': 'justify'}),

    html.Ul([
        html.Li(dcc.Markdown(r'''$$ 
        {T_i}^I = {T_i}^{II} $$
        ''', mathjax=True)),

        html.Li(dcc.Markdown(r'''$$ 
        {P_i}^I = {P_i}^{II} 
        $$''', mathjax=True)),

        html.Li(dcc.Markdown(r'''$$ 
        \mu_i^I ~=~ \mu_i^{II} 
        $$''', mathjax=True))

    ], style={'listStyleType': 'none', 'text-align': 'left'}),

    html.P('''Onde i, denota o componente (A, B ou C) e I indica a fase trabalhada.''', style={'text-align': 'justify'}),

    html.P('''O critério do potencial químico pode ser relacionado diretamente com o conceito de 
                    Fugacidade (f). Dessa forma o novo critério de equilíbrio é dado por:''', style={'text-align': 'justify'}),

    dcc.Markdown(r'''$$ 
       \Large{
       \hat{f}_i^I ~=~ \hat{f}_i^{II}
       } 
        $$''', mathjax=True),


    html.P('''Que pode ser reescrita utilizando como:''', style={'text-align': 'justify'}),

    dcc.Markdown(r'''
    $$
    \large{
    (x_i ~\gamma_{i} )^I  ~=~ (x_i ~\gamma_{i} )^{II} 
    }
    $$''', mathjax=True),
    
    html.P("Onde:", style={'text-align': 'justify'}),

    dcc.Markdown(r'''
    $$ 
    x_i : ~a ~fração ~molar~ do ~composto ~i 
    $$ 
    
    $$ 
    \gamma_{i} : Coeficiente ~de~ Atividade ~do~ composto ~i
    $$ 

    ''', mathjax=True),

    html.Br()

], style={"padding-top": "50px"})


# Como usar?
referencias = html.Div(id="referencias", children=[
    html.H2("Referências"),

    html.Ol([
        html.Li("Inserção dos dados (Parâmetros Binários, Nomes, Tielines) na aba 'Registro de dados', atentando-se para o uso de ponto (.) invés de vírgula (,);"),
        html.Li("Cadastro de dados no botão 'Cadastrar valores' (Com isso as abas para os gráficos dos pares binários e 3d ficaram disponíveis);"),
        html.Li("Navegação através das abas, para a geração dos dados;"),
        html.Li("Interação com os gráficos pode ser realizado com o mouse ou através dos botões (sendo possível a ocultação das tie-lines clicando na legenda.")
    ], style={'text-align': 'justify'}),

], style={"padding-top": "50px"})




# Sumário com os links
sidebar = dbc.Col([

    html.H2("Sumário", style={"text-align": "center"}),

    html.Ul([  # Lista de itens no sumário com links
        html.Li(html.A("Sobre a Aplicação", href="#introducao")),
        html.Li(html.A("Como Usar?", href="#Instrucao")),
        html.Li(html.A("Equilíbrio de Fases", href="#ELL"))
    ])

], width = 2, style={"background-color": "#f8f9fa"}) # Tamanho da coluna de sumario (2/12)


# Conteúdo principal, configuramos cada seção
content = dbc.Col([
    introducao,
    instrucao,
    ELL,

], width = 10, style={"justify-content": "center", "height": "100vh", "text-align": "center"})


# Layout da página
layout = dbc.Container([
    dbc.Row([
        sidebar,
        content
    ]), # Inclui a coluna do sumário e a coluna do conteúdo

], fluid=True)