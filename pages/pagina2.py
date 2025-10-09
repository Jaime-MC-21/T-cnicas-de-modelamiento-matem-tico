import dash
from dash import html, dcc
import plotly.graph_objects as go
import numpy as np


P0 = 50     
r = 0.20    
K = 1200    
t = np.linspace(0, 100, 100)
P_logistica = K / (1 + ((K - P0) / P0) * np.exp(-r * t))


trace_logistica = go.Scatter(
    x=t, y=P_logistica, mode='lines',
    line=dict(color='#3498db', width=3),
    name='Población',
    hovertemplate='Tiempo: %{x:.1f}<br>Población: %{y:.1f}<extra></extra>'
)

trace_capacidad = go.Scatter(
    x=t, y=[K]*len(t), mode='lines',
    line=dict(color='#e74c3c', dash='dash', width=2),
    name=f'Capacidad de Carga (K={K})',
    hoverinfo='skip'
)

fig = go.Figure(data=[trace_logistica, trace_capacidad])

fig.update_layout(
    title=dict(
        text='<b>Crecimiento Poblacional Logístico</b>',
        font=dict(size=22, color='#2c3e50'),
        x=0.5
    ),
    xaxis_title='Tiempo (t)',
    yaxis_title='Población P(t)',
    paper_bgcolor='white',
    plot_bgcolor='white',
    font=dict(family='Poppins', size=12, color='black'),
    margin=dict(l=40, r=40, t=80, b=40),
    showlegend=True,
    legend=dict(x=0.02, y=0.98),
    hovermode='x unified'
)
fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0', zerolinecolor='#cccccc')
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0', zerolinecolor='#cccccc')


dash.register_page(__name__, path='/Clase_2', name='Crecimiento Logístico')

layout = html.Section(className='content-section', children=[
    html.Div(className='text-content', children=[
        html.H2("Modelo de Crecimiento Logístico"),
        dcc.Markdown(r"""
            El crecimiento logístico ocurre cuando el crecimiento de una población se desacelera a medida que se acerca a su **capacidad de carga**, denotada por $K$. La ecuación diferencial logística es:
            $$\frac{dP}{dt} = rP\left(1 - \frac{P}{K}\right)$$
            La solución a esta ecuación es:
            $$P(t) = \frac{K}{1 + \left(\frac{K - P_0}{P_0}\right)e^{-rt}}$$
            Para esta gráfica, los nuevos parámetros son $P_0=50$, $r=0.20$ y $K=1200$.
        """, mathjax=True),
    ]),
    html.Div(className='graph-content', children=[
        dcc.Graph(figure=fig)
    ])
])