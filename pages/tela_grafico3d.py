'''
Tela do gráfico 3d da aplicação
'''

# Importando as bibliotecas
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash

# Registro da página
dash.register_page(__name__, path="/pages/tela_grafico3d", name = "Superfície Gm/RT")

# Layout da pagina
layout = dbc.Container([

    dcc.Markdown(
        # Descrição da página
        children = 'Página para a superfície de Energia Livre de Gibbs',
        className = 'mb-2',
        style={'textAlign': 'left'}
            ),

    html.Div([
        html.Br(),

        dbc.Input(id = "Titulo", type = "text", placeholder="Titulo do grafico", className = "form-control",
                  persistence = True, persistence_type = "session"),

        html.Br(),

        dbc.Row([

            dbc.Col([
                dcc.Markdown(children="Limite Superior do eixo Gm:"),
                dbc.Input(id = "LimSup", type = "text", placeholder = "Use ponto invés de vírgula", className = "form-control",
                          persistence = True, persistence_type = "session")
            ]),

            dbc.Col([
                dcc.Markdown(children="Limite Inferior do eixo Gm:"),
                dbc.Input(id = "LimInf", type = "text", placeholder = "Use ponto invés de vírgula", className = "form-control",
                          persistence = True, persistence_type = "session")
            ]),

            dbc.Col([
                dcc.Markdown(children="Opacidade da superfície:"),
                dcc.Slider(
                    id = "Transparencia",
                    min = 0,
                    max = 1,
                    value = 0.8,
                    persistence = True, persistence_type = "session"
                )
            ])

        ]),

        html.Br(),

        # Botão que mostra o gráfico
        html.Button(children= "Gerar Gráfico", id = "Botao_Gerar_Grafico3d", n_clicks = 0, className = "btn btn-warning btn-lg" ),

        html.Br(),
        html.Br(),

        dcc.Loading(
            id = "Icone_Loading",
            type="circle",  # Tipo de ícone (pode ser "circle", "dot", ou "default")
            children = dcc.Graph(id='Grafico_3d', style={'text-align': 'center'})  # Local que será mostrado o gráfico
        ),

    ]),

    html.Div(
        html.Br()
    )

])
