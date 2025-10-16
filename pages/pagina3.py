import dash
from dash import html, dcc, Output, Input, State, callback
from utils.funciones import funcion_graficas_ecu_log

dash.register_page(__name__, path='/modelo-logistico', name='Modelo Logístico')


layout = html.Section(className='content-section', children=[
    html.Div(className='text-content', children=[
        html.H2("Modelo Logístico Interactivo"),
        html.P("Ajusta los parámetros a continuación y presiona 'Generar' para visualizar el modelo de crecimiento logístico. Este modelo describe cómo una población crece y se estabiliza al alcanzar su capacidad de carga.")
    ]),


    html.Div(className='interactive-container', children=[
        # Panel de controles
        html.Div(className='controls-panel', children=[
            html.H4("Parámetros del Modelo"),
            html.Label("Población Inicial (P₀)"),
            dcc.Input(id="p0-logistico", type="number", value=50, className="input-field"),

            html.Label("Tasa de Crecimiento (r)"),
            dcc.Input(id="r-logistico", type="number", value=0.2, step=0.01, className="input-field"),

            html.Label("Capacidad de Carga (K)"),
            dcc.Input(id="k-logistico", type="number", value=1000, className="input-field"),

            html.Label("Tiempo Máximo (t)"),
            dcc.Input(id="tmax-logistico", type="number", value=80, className="input-field"),

            html.Button("Generar Gráfica", id="btn-logistico", n_clicks=0, className="btn-generar")
        ]),
        # Panel de la gráfica
        html.Div(className='graph-panel', children=[
            dcc.Graph(id="grafica-logistica")
        ])
    ])
])


@callback(
    Output('grafica-logistica', 'figure'),
    Input('btn-logistico', 'n_clicks'),
    State('p0-logistico', 'value'),
    State('r-logistico', 'value'),
    State('k-logistico', 'value'),
    State('tmax-logistico', 'value'),
    prevent_initial_call=False 
)
def update_logistic_graph(n_clicks, p0, r, k, tmax):
 
    fig = funcion_graficas_ecu_log(P0=p0, r=r, K=k, t_max=tmax)
    return fig
