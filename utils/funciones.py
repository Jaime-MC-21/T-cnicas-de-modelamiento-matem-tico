import numpy as np
import plotly.graph_objects as go
from scipy.integrate import odeint

def funcion_graficas_ecu_log(P0, r, K, t_max):

    t = np.linspace(0, t_max, 200)
  
    P = K / (1 + ((K - P0) / P0) * np.exp(-r * t))

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=t, y=P, mode='lines', name='Población',
        line=dict(color='#3498db', width=3),
        hovertemplate='Tiempo: %{x:.1f}<br>Población: %{y:.1f}<extra></extra>'
    ))

    fig.add_hline(y=K, line=dict(color='#e74c3c', dash='dash', width=2),
                  annotation_text=f"Capacidad (K={K})", annotation_position="bottom right")

    fig.update_layout(
        title='<b>Modelo Logístico de Crecimiento</b>',
        xaxis_title='Tiempo (t)',
        yaxis_title='Población P(t)',
        paper_bgcolor='white', plot_bgcolor='#f9f9f9',
        font=dict(family='Poppins', size=12),
        margin=dict(l=40, r=40, t=80, b=40),
        hovermode='x unified'
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#e0e0e0')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#e0e0e0')

    return fig


def funcion_grafica_logistica_con_cosecha(P0, r, K, t_max, h):
    """
    Genera una gráfica del modelo logístico con cosecha constante.
    Usa un solver numérico para resolver la EDO.
    """
    t = np.linspace(0, t_max, 500)

    def modelo(P, t, r, K, h):
        return r * P * (1 - P / K) - h

   
    P = odeint(modelo, P0, t, args=(r, K, h))
    P = P.flatten() 

    fig = go.Figure()


    fig.add_trace(go.Scatter(
        x=t, y=P, mode='lines', name='Población con Cosecha',
        line=dict(color='#27ae60', width=3),
        hovertemplate='Tiempo: %{x:.1f}<br>Población: %{y:.1f}<extra></extra>'
    ))

    fig.add_hline(y=K, line=dict(color='#e74c3c', dash='dash', width=2),
                  annotation_text=f"Capacidad Original (K={K})", annotation_position="top right")

    fig.update_layout(
        title='<b>Modelo Logístico con Cosecha Constante</b>',
        xaxis_title='Tiempo (t)',
        yaxis_title='Población P(t)',
        paper_bgcolor='white', plot_bgcolor='#f9f9f9',
        font=dict(family='Poppins', size=12),
        margin=dict(l=40, r=40, t=80, b=40),
        hovermode='x unified'
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#e0e0e0')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#e0e0e0', zeroline=False)

    return fig