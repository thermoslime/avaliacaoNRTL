'''
Tela de dados da aplicação
'''

# Importação das bibliotecas
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash

# Registro da página
dash.register_page(__name__,  path="/pages/tela_dados")


##################### Layout da pagina ################
layout = dbc.Container([

    # Descrição da página
    dcc.Markdown(children = '''
    Entre com o set de informações do sistema, ou escolha um dos registrados. Esses dados são usados para gerar a 
    análise da consistência termodinâmica dos parâmetros do modelo de energia de gibbs em excesso.''',
    style={
        'textAlign': 'left',
    }),

    # Opções gerais
    dbc.Row ([
    # Dropbox para a escolha do set
        dbc.Col([
            html.Label("Escolha o set de dados:"),
            dcc.Dropdown(options = ["Personalizado", "Caso 1: Inconsistente", "Caso 1: Consistente", "Caso 2: Inconsistente", "Caso 2: Consistente"],
                         id = "Drop_dados", multi = False, value = "Personalizado", clearable = False,
                         persistence = True, persistence_type = "session"),
        ]),

        dbc.Col([
            html.Label("Deseja adicionar as Tie-lines?"),
            dcc.RadioItems(
                options = [
                    {'label': 'Adicionar', 'value': 'Sim', 'disabled': False}, 
                    {'label': 'Não Adicionar', 'value': 'Não', 'disabled': False}
                    ],
                value = 'Não', id='Escolha_Tieline', persistence = True, persistence_type = "session"),
        ])
    ]),

    html.Br(),


    ################## parâmetros ##########################

    # Div com as informações interativas
    html.Div(id="dados_interativos", children=[
        dbc.Accordion([

            # Informações Gerais do sistema
            dbc.AccordionItem(
                children = html.Div([
                    dcc.Markdown(
                        '''
                        Informações gerais a respeito do sistema trabalhado. Entre com os nomes dos componentes em ordem, e com
                        a temperatura trabalhada.
                        ''',
                        style={'textAlign': 'left'}),

                    # Tabela com temperatura
                    dbc.Table([
                        html.Tbody([
                            html.Tr([html.Th(''), html.Th('Valor'), html.Th('Unidade')]),

                            html.Tr([html.Td('Temperatura'),
                                     html.Td([
                                         dcc.Input(id='Temperatura', value='298.15', type='text',
                                                   style={'textAlign': 'center'},
                                                   persistence = True, persistence_type = "session")
                                     ]),

                                     html.Td([
                                         dcc.Dropdown(id='TemperaturaUnidade', options=['K', '°C', '°F'], value='K',
                                                      multi=False,
                                                      clearable=False,
                                                      disabled= False,
                                                      persistence = True, persistence_type = "session")
                                     ]),
                                     ]),
                        ])  # Final do Tbody
                    ], bordered=True),  # Final da tabela

                    # Tabela com os nomes
                    dbc.Table([
                        html.Tbody([
                            html.Tr([html.Th(''), html.Th('Composto 1'), html.Th('Composto 2'), html.Th('Composto 3')]),

                            html.Tr([html.Td('Nome'),
                                     html.Td([
                                         dcc.Input(id='nome_1', type='text',
                                                   style={'width': '100px', 'textAlign': 'center'},
                                                   persistence = True, persistence_type = "session")
                                     ]),
                                     html.Td([
                                         dcc.Input(id='nome_2', type='text',
                                                   style={'width': '100px', 'textAlign': 'center'},
                                                   persistence = True, persistence_type = "session")
                                     ]),
                                     html.Td([
                                         dcc.Input(id='nome_3', type='text',
                                                   style={'width': '100px', 'textAlign': 'center'},
                                                   persistence = True, persistence_type = "session")
                                     ])
                                     ]),

                            html.Tr([html.Td('Massa Molar (g/mol)'),
                                     html.Td([
                                         dcc.Input(id='MM_1', type='text',
                                                   style={'width': '100px', 'textAlign': 'center'},
                                                   persistence = True, persistence_type = "session")
                                     ]),
                                     html.Td([
                                         dcc.Input(id='MM_2', type='text',
                                                   style={'width': '100px', 'textAlign': 'center'},
                                                   persistence = True, persistence_type = "session")
                                     ]),
                                     html.Td([
                                         dcc.Input(id='MM_3', type='text',
                                                   style={'width': '100px', 'textAlign': 'center'},
                                                   persistence = True, persistence_type = "session")
                                     ])
                                     ]),
                        ])  # Final do Tbody
                    ], bordered=True),  # Final da tabela

                ], style={'width': '48%'}),  # Final do Div dos parametros
                title = 'Informações Gerais do sistema',
                item_id = 'id0'),

            # Tabela Aij
            dbc.AccordionItem(
                children = html.Div([
                html.Label('Unidade:'),

                dcc.RadioItems(['J/mol', ], 'J/mol', id='UnidadeAij', persistence = True, persistence_type = "session"),

                html.Br(),

                # Tabela interativa
                dbc.Table([
                    html.Tbody([
                        html.Tr(
                            [html.Th(dcc.Markdown("$A_{ij}$", mathjax=True)), html.Th('Composto 1'), html.Th('Composto 2'),
                             html.Th('Composto 3')]),

                        html.Tr([html.Td('Composto 1'),
                                 html.Td([
                                     html.Label(children='', style={'width': '100px', 'textAlign': 'center'})
                                 ]),
                                 html.Td([
                                     dcc.Input(id='A_1_2', type='text',
                                               style={'width': '100px', 'textAlign': 'center'},
                                               persistence = True, persistence_type = "session")
                                 ]),
                                 html.Td([
                                     dcc.Input(id='A_1_3', type='text',
                                               style={'width': '100px', 'textAlign': 'center'},
                                               persistence = True, persistence_type = "session")
                                 ]),
                                 ]),

                        html.Tr([html.Td('Composto 2'),
                                 html.Td([
                                     dcc.Input(id='A_2_1', type='text',
                                               style={'width': '100px', 'textAlign': 'center'},
                                               persistence = True, persistence_type = "session")
                                 ]),
                                 html.Td([
                                     html.Label(children='', style={'width': '100px', 'textAlign': 'center'})
                                 ]),
                                 html.Td([
                                     dcc.Input(id='A_2_3', type='text',
                                               style={'width': '100px', 'textAlign': 'center'},
                                               persistence = True, persistence_type = "session")
                                 ]),
                                 ]),

                        html.Tr([html.Td('Composto 3'),
                                 html.Td([
                                     dcc.Input(id='A_3_1', type='text',
                                               style={'width': '100px', 'textAlign': 'center'},
                                               persistence = True, persistence_type = "session")
                                 ]),
                                 html.Td([
                                     dcc.Input(id='A_3_2', type='text',
                                               style={'width': '100px', 'textAlign': 'center'},
                                               persistence = True, persistence_type = "session")
                                 ]),
                                 html.Td([
                                     html.Label(children='', style={'width': '100px', 'textAlign': 'center'})
                                 ]),
                                 ]),

                    ])  # Final do Tbody
                ], bordered=True),  # Final da tabela
            ], style={'width': '48%'}),  # Final do Div dos parametros
                title = 'Parâmetros de Interação Binários',
                item_id = 'id1'),

            # Tabela Alfa
            dbc.AccordionItem(
                children = html.Div([
                # Tabela interativa
                dbc.Table([
                    html.Tbody([
                        html.Tr([html.Th('Interação'), html.Th('Valor')]),

                        html.Tr([html.Td(dcc.Markdown("$\\alpha_{12}$", mathjax=True)),
                                 html.Td([
                                     dcc.Input(id='Alfa_1_2', type='text',
                                               style={'width': '100px', 'textAlign': 'center'},
                                               persistence = True, persistence_type = "session")
                                 ])
                                 ]),
                        html.Tr([html.Td(dcc.Markdown("$\\alpha_{13}$", mathjax=True)),
                                 html.Td([
                                     dcc.Input(id='Alfa_1_3', type='text',
                                               style={'width': '100px', 'textAlign': 'center'},
                                               persistence = True, persistence_type = "session")
                                 ])
                                 ]),

                        html.Tr([html.Td(dcc.Markdown("$\\alpha_{23}$", mathjax=True)),
                                 html.Td([
                                     dcc.Input(id='Alfa_2_3', type='text',
                                               style={'width': '100px', 'textAlign': 'center'},
                                               persistence = True, persistence_type = "session")
                                 ])
                                 ]),

                    ])  # Final do Tbody
                ], bordered=True),  # Final da tabela
            ], style={'width': '48%'}),  # Final do Div dos parametros
                title = 'Parâmetros de Não Aleatoriedade',
                item_id = 'id2'),

            # Tie-lines
            dbc.AccordionItem(
                children = html.Div([
                    html.P( [
                        '''
                        Entre com as informações das composições das tie-lines. 
                        ''',
                        
                        html.A("Modelo CSV.", href="https://drive.google.com/file/d/1g4xgjgio91iCbLyHw62VfC7c_bcG7AYr/view?usp=sharing", target="_blank")
                        
                        ], style={'textAlign': 'left',
                        }),

                    dcc.Upload(id="Upload_tielines", children=html.Button("Upload das tie-lines", id = "Botao_tielines", n_clicks = 0),
                               disable_click=False, disabled=False, accept=".csv, .xlsx, .xls", ),

                    html.Br(),

                    dcc.Loading(
                        id="Icone_Loading_tielines",
                        type="circle",  # Tipo de ícone (pode ser "circle", "dot", ou "default")
                        children=html.Div(id="Conteudo_tieline")  # O que vai ser mostrado no final
                    ),

                ], style={'width': '48%'}),  # Final do Div dos parametros,

                title = 'Tie-Lines',
                item_id = 'id3'
            )

        ], always_open= True, flush = False, start_collapsed = True, active_item = ['id0', 'id1', 'id2', 'id3'])

    ]),

    # Inicio dos cálculos
    html.Br(),
    dbc.Button("Cadastrar valores", id='Botao_tabela', n_clicks=0, outline=True, color="primary", className="me-1"),

    html.Br(),
    html.Br(),

    # Componente de carregamento
    dcc.Loading(
        id = "Icone_Loading",
        type="circle",  # Tipo de ícone (pode ser "circle", "dot", ou "default")
        children = html.Div(id = "Tabela")  # O que vai ser mostrado no final
    ),

    html.Br(),
    html.Br()

])



