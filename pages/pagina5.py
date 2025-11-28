

import dash
from dash import html, dcc, Output, Input, State, callback
from utils.funciones import generar_campo_vectorial 

dash.register_page(__name__, path='/campo-vectorial', name='Campo Vectorial 2D', order=5)


layout = html.Div(className='campo-vectorial-page', children=[
    html.Div(className='controls-column', children=[
        html.H2("Campo Vectorial 2D", className='column-header'),
        html.Label("Ecuación dx/dt ="),
        dcc.Input(id="ecu-dx-dt", type="text", value="Y*(X**2 + Y**2)", className="input-field-large"),
        html.Label("Ecuación dy/dt ="),
        dcc.Input(id="ecu-dy-dt", type="text", value="-X*(X**2 + Y**2)", className="input-field-large"),
        html.Label("Rango del Eje X:"),
        dcc.Input(id="rango-x", type="number", value=5, step=1, className="input-field"),
        html.Label("Rango del Eje Y:"),
        dcc.Input(id="rango-y", type="number", value=5, step=1, className="input-field"),
        html.Label("Mallado (puntos por eje):"),
        dcc.Input(id="mallado", type="number", value=20, step=1, min=5, max=50, className="input-field"),
        html.Button("Generar Campo", id="btn-primary-action", n_clicks=0, className="btn-primary-action"),

        html.Div(className='ejemplos-section', children=[
            html.H3("Ejemplos para probar:"),
            html.Ul([
                html.Li(dcc.Markdown("`dx/dt = Y`, `dy/dt = -X` (Giro en sentido horario)")),
                html.Li(dcc.Markdown("`dx/dt = -Y`, `dy/dt = X` (Giro en sentido antihorario)")),
                html.Li(dcc.Markdown("`dx/dt = X`, `dy/dt = Y` (Fuente)")),
                html.Li(dcc.Markdown("`dx/dt = -X`, `dy/dt = -Y` (Sumidero)")),
                html.Li(dcc.Markdown("`dx/dt = X + Y`, `dy/dt = np.cos(Y)`")),
                html.Li(dcc.Markdown("`dx/dt = Y*(X**2+Y**2)`, `dy/dt = -X*(X**2+Y**2)` (El que está por defecto)")),
            ])
        ])
    ]),
    html.Div(className='visualization-column', children=[
        html.H2("Visualización del Campo Vectorial", className='column-header'),
        html.Div(id="campo-vectorial-output", className='vector-field-graph-container', children=[
            dcc.Graph(id="grafica-campo-vectorial")
        ])
    ])
])


@callback(
    Output('grafica-campo-vectorial', 'figure'),
    Input('btn-primary-action', 'n_clicks'),
    State('ecu-dx-dt', 'value'),
    State('ecu-dy-dt', 'value'),
    State('rango-x', 'value'),
    State('rango-y', 'value'),
    State('mallado', 'value'),
    prevent_initial_call=False 
)
def update_vector_field(n_clicks, ecu_dx, ecu_dy, r_x, r_y, malla):
    
    ecu_dx = ecu_dx if ecu_dx else "Y"
    ecu_dy = ecu_dy if ecu_dy else "-X"
    r_x = r_x if r_x is not None else 5
    r_y = r_y if r_y is not None else 5
    malla = malla if malla is not None else 20


    fig = generar_campo_vectorial(ecu_dx, ecu_dy, r_x, r_y, malla)
    return fig
