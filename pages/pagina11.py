
import dash
from dash import html, dcc, Output, Input, State, callback
from utils.funciones import generar_grafica_gripe_san_marcos, generar_grafica_rumor, generar_grafica_app

dash.register_page(__name__, path='/modelos-integrados', name='DASHBOARD DEL PROYECTO FINAL', order=11)

layout = html.Div(className='dashboard-container', children=[
    html.H1("Graficas interactivas de las asignaciones", style={'width': '100%', 'textAlign': 'center', 'marginBottom': '20px', 'color': '#2c3e50'}),

    dcc.Tabs(id="tabs-modelos", value='tab-1', children=[
        
       
        dcc.Tab(label='Asignacion 1: Gripe en San Marcos', value='tab-1', className='custom-tab', selected_className='custom-tab--selected', children=[
            html.Div(className='tab-content', children=[
                html.Div(className='panel-izquierdo', children=[
                    html.H4("Parámetros Gripe"),
                    html.Label("Población Total (N):"),
                    dcc.Input(id='gripe-N', type='number', value=7138, className='input-field'),
                    html.Label("Infectados Iniciales (I0):"),
                    dcc.Input(id='gripe-I0', type='number', value=1, className='input-field'),
                    html.Label("Tasa de Recuperación (k):"),
                    dcc.Input(id='gripe-k', type='number', value=0.40, step=0.01, className='input-field'),
                    html.Label("Días a simular:"),
                    dcc.Input(id='gripe-t', type='number', value=40, className='input-field'),
                    html.Button('Simular Gripe', id='btn-gripe', n_clicks=0, className='btn-primary-action')
                ]),
                html.Div(className='panel-derecho', children=[
                    dcc.Graph(id='grafica-gripe')
                ])
            ])
        ]),

        
        dcc.Tab(label='Asignacion 2: Propagación de Rumor', value='tab-2', className='custom-tab', selected_className='custom-tab--selected', children=[
            html.Div(className='tab-content', children=[
                html.Div(className='panel-izquierdo', children=[
                    html.H4("Parámetros Rumor"),
                    html.Label("Alumnos Susceptibles (S0):"),
                    dcc.Input(id='rumor-S0', type='number', value=266, className='input-field'),
                    html.Label("Propagadores Iniciales (I0):"),
                    dcc.Input(id='rumor-I0', type='number', value=1, className='input-field'),
                    html.Label("Racionales Iniciales (R0):"),
                    dcc.Input(id='rumor-R0', type='number', value=8, className='input-field'),
                    html.Label("Tasa Propagación (b):"),
                    dcc.Input(id='rumor-b', type='number', value=0.004, step=0.001, className='input-field'),
                    html.Label("Tasa Racionalización (k):"),
                    dcc.Input(id='rumor-k', type='number', value=0.01, step=0.01, className='input-field'),
                    html.Button('Simular Rumor', id='btn-rumor', n_clicks=0, className='btn-primary-action')
                ]),
                html.Div(className='panel-derecho', children=[
                    dcc.Graph(id='grafica-rumor')
                ])
            ])
        ]),

        
        dcc.Tab(label='Asignacion 3: App Móvil', value='tab-3', className='custom-tab', selected_className='custom-tab--selected', children=[
            html.Div(className='tab-content', children=[
                html.Div(className='panel-izquierdo', children=[
                    html.H4("Parámetros App"),
                    html.Div(style={'marginBottom': '15px'}, children=[
                        html.Button("Cargar Éxito", id="btn-app-exito", className="btn-mini success"),
                        html.Button("Cargar Fracaso", id="btn-app-fracaso", className="btn-mini danger", style={'marginLeft': '5px'}),
                    ]),
                    html.Label("Población Objetivo (N):"),
                    dcc.Input(id='app-N', type='number', value=10000, className='input-field'),
                    html.Label("Tasa Adopción (b):"),
                    dcc.Input(id='app-b', type='number', value=0.0005, step=0.0001, className='input-field'),
                    html.Label("Tasa Abandono (k):"),
                    dcc.Input(id='app-k', type='number', value=0.05, step=0.01, className='input-field'),
                    html.Button('Simular App', id='btn-app', n_clicks=0, className='btn-primary-action')
                ]),
                html.Div(className='panel-derecho', children=[
                    dcc.Graph(id='grafica-app-final')
                ])
            ])
        ]),
    ])
])


@callback(
    Output('grafica-gripe', 'figure'),
    Input('btn-gripe', 'n_clicks'),
    State('gripe-N', 'value'), State('gripe-I0', 'value'),
    State('gripe-k', 'value'), State('gripe-t', 'value'),
    prevent_initial_call=False
)
def update_gripe(n, N, I0, k, t):
    N = N or 7138
    I0 = I0 or 1
    k = k or 0.40
    t = t or 40
    return generar_grafica_gripe_san_marcos(N, I0, 0, k, t)


@callback(
    Output('grafica-rumor', 'figure'),
    Input('btn-rumor', 'n_clicks'),
    State('rumor-S0', 'value'), State('rumor-I0', 'value'),
    State('rumor-R0', 'value'), State('rumor-b', 'value'),
    State('rumor-k', 'value'),
    prevent_initial_call=False
)
def update_rumor(n, S0, I0, R0, b, k):
    S0, I0, R0 = S0 or 266, I0 or 1, R0 or 8
    b, k = b or 0.004, k or 0.01
    N = S0 + I0 + R0
    return generar_grafica_rumor(N, I0, R0, b, k, 15)


@callback(
    [Output('app-b', 'value'), Output('app-k', 'value'), Output('grafica-app-final', 'figure')],
    [Input('btn-app', 'n_clicks'), Input('btn-app-exito', 'n_clicks'), Input('btn-app-fracaso', 'n_clicks')],
    [State('app-N', 'value'), State('app-b', 'value'), State('app-k', 'value')],
    prevent_initial_call=False
)
def update_app(n_gen, n_exito, n_fracaso, N, b, k):
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    
    N = N or 10000
    b_final = b or 0.0005
    k_final = k or 0.05

    if trigger_id == 'btn-app-exito':
        b_final, k_final = 0.0005, 0.05
    elif trigger_id == 'btn-app-fracaso':
        b_final, k_final = 0.0001, 0.2

    fig = generar_grafica_app(N, 10, b_final, k_final, 100)
    return b_final, k_final, fig
