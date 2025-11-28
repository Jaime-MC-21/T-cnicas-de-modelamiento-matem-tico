
import dash
from dash import html, dcc, Output, Input, State, callback
import plotly.graph_objects as go
from utils.funciones import obtener_pronostico_clima

dash.register_page(__name__, path='/dashboard-clima', name='Dashboard Clima', order=10)


CIUDADES = {
    'Lima': {'lat': -12.0464, 'lon': -77.0428},
    'Cusco': {'lat': -13.5226, 'lon': -71.9673},
    'Arequipa': {'lat': -16.4090, 'lon': -71.5375},
    'Tokio': {'lat': 35.6762, 'lon': 139.6503},
    'Londres': {'lat': 51.5074, 'lon': -0.1278},
    'Nueva York': {'lat': 40.7128, 'lon': -74.0060}
}

layout = html.Div(className='dashboard-container', children=[
    
 
    html.Div(className='panel-izquierdo', children=[
        html.H3("Modelamiento Atmosférico"),
        html.P("Consulta modelos de predicción numérica para variables físicas en tiempo real."),
        
        html.Label("Ubicación de estudio:"),
        dcc.Dropdown(
            id='drop-ciudad',
            options=[{'label': k, 'value': k} for k in CIUDADES.keys()],
            value='Lima',
            className='dropdown-estilo',
            clearable=False
        ),
        
        html.Label("Variable a graficar:"),
        dcc.RadioItems(
            id='radio-variable',
            options=[
                {'label': ' Temperatura (2m)', 'value': 'temp'},
                {'label': ' Velocidad del Viento', 'value': 'wind'},
                {'label': ' Radiación Solar', 'value': 'rad'}
            ],
            value='temp',
            labelStyle={'display': 'block', 'marginBottom': '8px'}
        ),
        
        html.Button('Analizar Datos', id='btn-clima', n_clicks=0, className='btn-primary-action')
    ]),

  
    html.Div(className='panel-derecho', children=[
        html.H2(id='titulo-ubicacion', className="titulo-seccion", children="Condiciones Meteorológicas"),
        
       
        html.Div(className='cards-container', children=[
            html.Div([html.H4("Temperatura Actual"), html.H3(id="card-temp", children="-- °C")], className="info-card card-blue"),
            html.Div([html.H4("Humedad Relativa"), html.H3(id="card-hum", children="-- %")], className="info-card card-green"),
            html.Div([html.H4("Viento (10m)"), html.H3(id="card-wind", children="-- km/h")], className="info-card card-orange"),
        ]),

        
        html.Div(className='grafica-container', children=[
            dcc.Graph(id='grafica-clima')
        ]),
        
        html.P("Datos provistos por el modelo GFS y Open-Meteo API.", style={'fontSize': '0.8rem', 'marginTop': '10px', 'color': '#666'})
    ])
])


@callback(
    [Output('titulo-ubicacion', 'children'),
     Output('card-temp', 'children'),
     Output('card-hum', 'children'),
     Output('card-wind', 'children'),
     Output('grafica-clima', 'figure')],
    Input('btn-clima', 'n_clicks'),
    State('drop-ciudad', 'value'),
    State('radio-variable', 'value'),
    prevent_initial_call=False
)
def actualizar_clima(n_clicks, ciudad, variable):
 
    coords = CIUDADES.get(ciudad, CIUDADES['Lima'])
    lat, lon = coords['lat'], coords['lon']
    
  
    data = obtener_pronostico_clima(lat, lon)
    
    if not data:
        return "Error API", "-", "-", "-", go.Figure()

   
    curr = data.get('current', {})
    temp_act = f"{curr.get('temperature_2m', 0)} °C"
    hum_act = f"{curr.get('relative_humidity_2m', 0)} %"
    wind_act = f"{curr.get('wind_speed_10m', 0)} km/h"
    
    
    hourly = data.get('hourly', {})
    tiempos = hourly.get('time', [])
    
    fig = go.Figure()
    
    if variable == 'temp':
        y_data = hourly.get('temperature_2m', [])
        titulo_y = "Temperatura (°C)"
        color_linea = '#3498db'
        fill_color = 'rgba(52, 152, 219, 0.2)' 
    elif variable == 'wind':
        y_data = hourly.get('wind_speed_10m', [])
        titulo_y = "Velocidad (km/h)"
        color_linea = '#e67e22'
        fill_color = 'rgba(230, 126, 34, 0.2)' 
    else: 
        y_data = hourly.get('shortwave_radiation', [])
        titulo_y = "Radiación (W/m²)"
        color_linea = '#e74c3c'
        fill_color = 'rgba(231, 76, 60, 0.2)' 

    fig.add_trace(go.Scatter(
        x=tiempos, 
        y=y_data, 
        mode='lines', 
        name=titulo_y,
        line=dict(color=color_linea, width=3),
        fill='tozeroy', 
        fillcolor=fill_color
    ))

    fig.update_layout(
        title=f"Pronóstico horario: {ciudad}",
        yaxis_title=titulo_y,
        xaxis_title="Tiempo",
        paper_bgcolor='white',
        plot_bgcolor='#f9f9f9',
        font=dict(family='Poppins'),
        margin=dict(l=40, r=20, t=40, b=40),
        hovermode="x unified"
    )

    return f"Meteorología en {ciudad}", temp_act, hum_act, wind_act, fig
