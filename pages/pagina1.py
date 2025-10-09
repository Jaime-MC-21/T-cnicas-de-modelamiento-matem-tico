import dash
from dash import html, dcc
import plotly.graph_objects as go
import numpy as np


P0 = 100
r = 0.03
t = np.linspace(0, 100, 50)
P = P0 * np.exp(r * t)


trace = go.Scatter(
    x=t,
    y=P,
    mode='lines+markers',
    line=dict(
        color='#3498db', 
        width=3
    ),
    marker=dict(
        symbol='circle',
        size=8,
        color='#2c3e50'
    ),
    name='P(t) = P₀ * e^(rt)',
    hovertemplate='Tiempo: %{x:.1f}<br>Población: %{y:.1f}<extra></extra>'
)

fig = go.Figure(data=trace)

fig.update_layout(
    title=dict(
        text='<b>Crecimiento Poblacional Exponencial</b>',
        font=dict(size=22, color='#2c3e50'),
        x=0.5
    ),
    xaxis_title='Tiempo (t)',
    yaxis_title='Población P(t)',
    paper_bgcolor='white',
    plot_bgcolor='white',
    font=dict(family='Poppins', size=12, color='black'),
    margin=dict(l=40, r=40, t=80, b=40),
    hovermode='x unified'
)
fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0', zerolinecolor='#cccccc')
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0', zerolinecolor='#cccccc')


dash.register_page(__name__, path='/Clase_1', name='Crecimiento Exponencial')

layout = html.Section(className='content-section', children=[
    html.Div(className='text-content', children=[
        html.H2("Modelo de Crecimiento Exponencial"),
        dcc.Markdown("""
            Para modelar el crecimiento de una población, usamos la variable $t$ para el tiempo y $P(t)$ para la población en función del tiempo. Si $P(t)$ es una función diferenciable, su derivada $\\frac{dP}{dt}$ representa la tasa de cambio instantánea de la población.
            
            La función de crecimiento exponencial es $P(t)=P_0e^{rt}$, donde $P_0$ es la población inicial, y $r>0$ es la tasa de crecimiento. Para esta gráfica, usamos $P_0=100$ y $r=0.03$.
        """, mathjax=True),
    ]),
    html.Div(className='graph-content', children=[
        dcc.Graph(figure=fig)
    ])
])