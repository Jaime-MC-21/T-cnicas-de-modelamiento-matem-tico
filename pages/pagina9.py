
import dash
from dash import html, dcc, Output, Input, State, callback
from utils.funciones import buscar_personajes_rickmorty

dash.register_page(__name__, path='/api-rick-morty', name='API de Rick & Morty')

layout = html.Div(className='rm-page', children=[
    html.H1("Rick and Morty"),
    html.P("Coloca el nombre de aun personaje de la serie"),
    
    html.Div(className='search-bar-container', children=[
        dcc.Input(id='input-personaje', type='text', value='Rick', placeholder="Escribe un nombre (ej: Morty)", className='input-field'),
        html.Button('Buscar', id='btn-buscar-rm', n_clicks=0, className='btn-primary-action')
    ]),
    
    html.Div(id='grid-personajes', className='grid-resultados')
])

@callback(
    Output('grid-personajes', 'children'),
    Input('btn-buscar-rm', 'n_clicks'),
    State('input-personaje', 'value'),
    prevent_initial_call=False
)
def actualizar_grid(n_clicks, nombre):
    if not nombre:
        return html.H3("Por favor ingresa un nombre.")
        
    personajes = buscar_personajes_rickmorty(nombre)
    
    if not personajes:
        return html.H3(f"No se encontraron personajes con el nombre '{nombre}'.")
    

    tarjetas = []
    for p in personajes:
        tarjeta = html.Div(className='rm-card', children=[
            html.Img(src=p['image']),
            html.Div(className='rm-card-info', children=[
                html.H4(p['name']),
                html.P(f"Status: {p['status']}"),
                html.P(f"Especie: {p['species']}")
            ])
        ])
        tarjetas.append(tarjeta)
        
    return tarjetas
