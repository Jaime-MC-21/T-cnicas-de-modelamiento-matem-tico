
import dash
from dash import html, dcc, Output, Input, State, callback
import plotly.graph_objects as go
from utils.funciones import obtener_datos_covid_actuales, obtener_datos_covid_historicos

dash.register_page(__name__, path='/dashboard-covid', name='Dashboard COVID')

layout = html.Div(className='dashboard-container', children=[
    

    html.Div(className='panel-izquierdo', children=[
        html.H3("Configuración"),
        
        html.Label("Seleccione el país:"),
        dcc.Dropdown(
            id='dropdown-pais',
            options=[
                {'label': 'Perú', 'value': 'Peru'},
                {'label': 'México', 'value': 'Mexico'},
                {'label': 'Estados Unidos', 'value': 'USA'},
                {'label': 'España', 'value': 'Spain'},
                {'label': 'Colombia', 'value': 'Colombia'},
                {'label': 'Argentina', 'value': 'Argentina'}
            ],
            value='Peru',
            className='dropdown-estilo'
        ),
        
        html.Label("Días históricos:"),
        dcc.Dropdown(
            id='dropdown-dias',
            options=[
                {'label': 'Últimos 30 días', 'value': '30'},
                {'label': 'Últimos 60 días', 'value': '60'},
                {'label': 'Últimos 90 días', 'value': '90'},
                {'label': 'Todo el histórico', 'value': 'all'}
            ],
            value='30',
            className='dropdown-estilo'
        ),
        
        html.Button('Actualizar Datos', id='btn-covid', n_clicks=0, className='btn-primary-action')
    ]),


    html.Div(className='panel-derecho', children=[
        html.H2("Estadísticas en tiempo real", className="titulo-seccion"),
        

        html.Div(className='cards-container', children=[
            html.Div([html.H4("Total Casos"), html.H3(id="card-casos", children="0")], className="info-card card-blue"),
            html.Div([html.H4("Casos Hoy"), html.H3(id="card-hoy", children="0")], className="info-card card-orange"),
            html.Div([html.H4("Total Muertes"), html.H3(id="card-muertes", children="0")], className="info-card card-red"),
            html.Div([html.H4("Recuperados"), html.H3(id="card-recuperados", children="0")], className="info-card card-green"),
        ]),


        html.Div(className='grafica-container', children=[
            dcc.Graph(id='grafica-covid')
        ])
    ])
])


@callback(
    [Output('card-casos', 'children'),
     Output('card-hoy', 'children'),
     Output('card-muertes', 'children'),
     Output('card-recuperados', 'children'),
     Output('grafica-covid', 'figure')],
    Input('btn-covid', 'n_clicks'),
    State('dropdown-pais', 'value'),
    State('dropdown-dias', 'value'),
    prevent_initial_call=False
)
def actualizar_dashboard(n_clicks, pais, dias):
   
    data_actual = obtener_datos_covid_actuales(pais)
    
    casos, hoy, muertes, recup = "---", "---", "---", "---"
    
    if data_actual:
        casos = f"{data_actual.get('cases', 0):,}"
        hoy = f"+{data_actual.get('todayCases', 0):,}"
        muertes = f"{data_actual.get('deaths', 0):,}"
        recup = f"{data_actual.get('recovered', 0):,}"


    data_hist = obtener_datos_covid_historicos(pais, dias)
    fig = go.Figure()
    
    if data_hist and 'timeline' in data_hist:
        timeline = data_hist['timeline']
        fechas = list(timeline['cases'].keys())
        val_casos = list(timeline['cases'].values())
        val_muertes = list(timeline['deaths'].values())
        val_recup = list(timeline['recovered'].values())

        fig.add_trace(go.Scatter(x=fechas, y=val_casos, name='Casos', line=dict(color='#3498db', width=2)))
        fig.add_trace(go.Scatter(x=fechas, y=val_muertes, name='Muertes', line=dict(color='#e74c3c', width=2)))
        fig.add_trace(go.Scatter(x=fechas, y=val_recup, name='Recuperados', line=dict(color='#27ae60', width=2)))

    fig.update_layout(
        title=f"Evolución histórica en {pais}",
        paper_bgcolor='white',
        plot_bgcolor='#f9f9f9',
        font=dict(family='Poppins'),
        margin=dict(l=40, r=20, t=40, b=40),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return casos, hoy, muertes, recup, fig