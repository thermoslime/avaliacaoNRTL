'''
Tela do gráfico binário
'''

# Importando as bibliotecas
from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import dash

# Registro da página
dash.register_page(__name__, path="/pages/tela_graficos_binarios", name = "Gráficos Binários")



# Layout da pagina lateral
sidebar = dbc.Col([

    # Descrição da página
    dcc.Markdown(children = '''
    Selecione os pares binários que deseja plotar as curvas''',
    style={
        'textAlign': 'left',
    }),

    html.Label("Selecione os Pares Binários:"),
    dcc.Checklist( id="Checkbox_2d", options=["1-2", "1-3", "2-3", "Fronteira (Alfa < 0.43)"], value=["1-2"], inline=False, persistence = True),

    html.Br(),

    dbc.Button(children = "Gerar Gráficos", id='Botao_2d', n_clicks=0, outline=True, color="primary", className="me-1"),


], width=3, style={"background-color": "#f8f9fa"})  # Tamanho da coluna de sumario (3/12)


# Conteúdo principal, onde apareceram os gráficos

# Conteúdo principal, configuramos cada seção
conteudo = dbc.Col([

    dbc.Row([
        dcc.Loading(
            id="Icone_Loading_2d_12",
            type="circle",  # Tipo de ícone (pode ser "circle", "dot", ou "default")
            children=html.Div(id="Graficos_2d_12")  # Local que será mostrado o gráfico
        ),
    ]),
    dbc.Row([
        dcc.Loading(
            id = "Icone_Loading_2d_13",
            type = "circle",  # Tipo de ícone (pode ser "circle", "dot", ou "default")
            children = html.Div(id="Graficos_2d_13")  # Local que será mostrado o gráfico
        ),
    ]),
    dbc.Row([
        dcc.Loading(
            id="Icone_Loading_2d_23",
            type="circle",  # Tipo de ícone (pode ser "circle", "dot", ou "default")
            children = html.Div(id="Graficos_2d_23")  # Local que será mostrado o gráfico
        ),
    ]),

    dbc.Row([
        dcc.Loading(
            id="Icone_Loading_2d_fronteira",
            type="circle",  # Tipo de ícone (pode ser "circle", "dot", ou "default")
            children=html.Div(id="Graficos_2d_fronteira")  # Local que será mostrado o gráfico
        ),
    ])


], width = 9, style={"justify-content": "center", "height": "100vh", "text-align": "center"})


# Layout da página
layout = dbc.Container([
    dbc.Row([
        sidebar,
        conteudo
    ]), # Inclui a coluna do sumário e a coluna do conteúdo

], fluid=True)

