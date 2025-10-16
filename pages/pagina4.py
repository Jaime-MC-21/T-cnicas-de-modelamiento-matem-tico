import dash
from dash import html, dcc, Output, Input, State, callback
from utils.funciones import funcion_grafica_logistica_con_cosecha

dash.register_page(__name__, path='/modelo-con-cosecha', name='Modelo con Cosecha')

layout = html.Section(className='content-section', children=[
    html.Div(className='text-content', children=[
        html.H2("Modelo Logístico con Cosecha"),
        html.P("Este modelo simula el efecto de remover una cantidad constante (cosecha) de la población en cada unidad de tiempo. Observa cómo diferentes niveles de cosecha pueden afectar la sostenibilidad de la población.")
    ]),

    html.Div(className='interactive-container', children=[

        html.Div(className='controls-panel', children=[
            html.H4("Parámetros del Modelo"),
            html.Label("Población Inicial (P₀)"),
            dcc.Input(id="p0-cosecha", type="number", value=500, className="input-field"),

            html.Label("Tasa de Crecimiento (r)"),
            dcc.Input(id="r-cosecha", type="number", value=0.25, step=0.01, className="input-field"),

            html.Label("Capacidad de Carga (K)"),
            dcc.Input(id="k-cosecha", type="number", value=1000, className="input-field"),

            html.Label("Tiempo Máximo (t)"),
            dcc.Input(id="tmax-cosecha", type="number", value=100, className="input-field"),
            
            html.Label("Tasa de Cosecha (h)"),
            dcc.Input(id="h-cosecha", type="number", value=50, className="input-field"),

            html.Button("Generar Gráfica", id="btn-cosecha", n_clicks=0, className="btn-generar")
        ]),

        html.Div(className='graph-panel', children=[
            dcc.Graph(id="grafica-cosecha")
        ])
    ])
])


@callback(
    Output('grafica-cosecha', 'figure'),
    Input('btn-cosecha', 'n_clicks'),
    State('p0-cosecha', 'value'),
    State('r-cosecha', 'value'),
    State('k-cosecha', 'value'),
    State('tmax-cosecha', 'value'),
    State('h-cosecha', 'value'),
    prevent_initial_call=False 
)
def update_harvest_graph(n_clicks, p0, r, k, tmax, h):

    fig = funcion_grafica_logistica_con_cosecha(P0=p0, r=r, K=k, t_max=tmax, h=h)
    return fig
