

import dash
from dash import html, dcc, Output, Input, State, callback
from utils.funciones import generar_modelo_seir 

dash.register_page(__name__, path='/modelo-seir', name='Modelo SEIR', order=7)


layout = html.Div(className='epidemic-page-container', children=[
    
    
    html.Div(className='controls-column', children=[
        html.H2("Modelo SEIR - Epidemiología", className='column-header'),
        
        html.Label("Población Total (N):"),
        dcc.Input(id="seir-n", type="number", value=1000, className="input-field"),
        
        html.Label("Tasa de transmisión (β):"),
        dcc.Input(id="seir-beta", type="number", value=0.35, step=0.01, className="input-field"),
        
        html.Label("Tasa de incubación (σ):"),
        dcc.Input(id="seir-sigma", type="number", value=0.2, step=0.01, className="input-field",
                  placeholder="Ej: 0.2 (para 5 días de incubación)"),
        
        html.Label("Tasa de recuperación (γ):"),
        dcc.Input(id="seir-gamma", type="number", value=0.1, step=0.01, className="input-field",
                  placeholder="Ej: 0.1 (para 10 días de infección)"),
        
        html.Label("Expuestos iniciales (E₀):"),
        dcc.Input(id="seir-e0", type="number", value=1, className="input-field"),

        html.Label("Infectados iniciales (I₀):"),
        dcc.Input(id="seir-i0", type="number", value=0, className="input-field"),
        
        html.Label("Tiempo de simulación (días):"),
        dcc.Input(id="seir-t", type="number", value=160, className="input-field"),
        
        html.Button("Simular Epidemia", id="btn-simular-seir", n_clicks=0, className="btn-primary-action")
    ]),
    

    html.Div(className='visualization-column', children=[
        html.H2("Evolución de la Epidemia", className='column-header'),
        html.Div(className='sir-graph-container', children=[ 
            dcc.Graph(id="grafica-seir")
        ])
    ])
])


@callback(
    Output('grafica-seir', 'figure'),
    Input('btn-simular-seir', 'n_clicks'),
    State('seir-n', 'value'),
    State('seir-beta', 'value'),
    State('seir-sigma', 'value'),
    State('seir-gamma', 'value'),
    State('seir-e0', 'value'),
    State('seir-i0', 'value'),
    State('seir-t', 'value'),
    prevent_initial_call=False 
)
def update_seir_graph(n_clicks, N, beta, sigma, gamma, E0, I0, T):
    
    N = N if N is not None and N > 0 else 1000
    beta = beta if beta is not None else 0.35
    sigma = sigma if sigma is not None else 0.2
    gamma = gamma if gamma is not None else 0.1
    E0 = E0 if E0 is not None else 1
    I0 = I0 if I0 is not None else 0
    T = T if T is not None and T > 0 else 160

    
    fig = generar_modelo_seir(N, E0, I0, beta, sigma, gamma, T)
    return fig
