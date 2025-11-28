

import dash
from dash import html, dcc, Output, Input, State, callback
from utils.funciones import generar_modelo_sir 

dash.register_page(__name__, path='/modelo-sir', name='Modelo SIR', order=6)


layout = html.Div(className='epidemic-page-container', children=[
    
   
    html.Div(className='controls-column', children=[
        html.H2("Modelo SIR - Epidemiología", className='column-header'),
        
        html.Label("Población Total (N):"),
        dcc.Input(id="sir-n", type="number", value=1000, className="input-field"),
        
        html.Label("Tasa de transmisión (β):"),
        dcc.Input(id="sir-beta", type="number", value=0.3, step=0.01, className="input-field"),
        
        html.Label("Tasa de recuperación (γ):"),
        dcc.Input(id="sir-gamma", type="number", value=0.1, step=0.01, className="input-field"),
        
        html.Label("Infectados iniciales (I₀):"),
        dcc.Input(id="sir-i0", type="number", value=1, className="input-field"),
        
        html.Label("Tiempo de simulación (días):"),
        dcc.Input(id="sir-t", type="number", value=100, className="input-field"),
        
        html.Button("Simular Epidemia", id="btn-simular-sir", n_clicks=0, className="btn-primary-action")
    ]),
    
   
    html.Div(className='visualization-column', children=[
        html.H2("Evolución de la Epidemia", className='column-header'),
        html.Div(className='sir-graph-container', children=[
            dcc.Graph(id="grafica-sir")
        ])
    ])
])


@callback(
    Output('grafica-sir', 'figure'),
    Input('btn-simular-sir', 'n_clicks'),
    State('sir-n', 'value'),
    State('sir-beta', 'value'),
    State('sir-gamma', 'value'),
    State('sir-i0', 'value'),
    State('sir-t', 'value'),
    prevent_initial_call=False 
)
def update_sir_graph(n_clicks, N, beta, gamma, I0, T):
    
    N = N if N is not None and N > 0 else 1000
    beta = beta if beta is not None else 0.3
    gamma = gamma if gamma is not None else 0.1
    I0 = I0 if I0 is not None and I0 > 0 else 1
    T = T if T is not None and T > 0 else 100

   
    fig = generar_modelo_sir(N, I0, beta, gamma, T)
    return fig
