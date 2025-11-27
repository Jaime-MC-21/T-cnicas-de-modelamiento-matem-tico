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

def generar_campo_vectorial(ecu_dx_dt, ecu_dy_dt, rango_x, rango_y, mallado):
    """
    Genera una figura Plotly para la visualización de un campo vectorial 2D.

    Args:
        ecu_dx_dt (str): Expresión para dx/dt, con 'X' y 'Y' como variables.
        ecu_dy_dt (str): Expresión para dy/dt, con 'X' y 'Y' como variables.
        rango_x (float): Rango máximo para el eje X (simétrico, ej. 5 -> de -5 a 5).
        rango_y (float): Rango máximo para el eje Y (simétrico, ej. 5 -> de -5 a 5).
        mallado (int): Número de puntos en cada dirección (ej. 20 -> 20x20 rejilla).

    Returns:
        go.Figure: Una figura Plotly con el campo vectorial.
    """
    x = np.linspace(-rango_x, rango_x, mallado)
    y = np.linspace(-rango_y, rango_y, mallado)
    X, Y = np.meshgrid(x, y)


    dx_dt = np.nan_to_num(eval(ecu_dx_dt, {'__builtins__': None, 'X': X, 'Y': Y, 'np': np}))
    dy_dt = np.nan_to_num(eval(ecu_dy_dt, {'__builtins__': None, 'X': X, 'Y': Y, 'np': np}))

 
    magnitudes = np.sqrt(dx_dt**2 + dy_dt**2)
    
    dx_dt_norm = np.where(magnitudes == 0, 0, dx_dt / magnitudes)
    dy_dt_norm = np.where(magnitudes == 0, 0, dy_dt / magnitudes)

   
    escala_vector = min(rango_x, rango_y) / (mallado * 1.5) 

    fig = go.Figure(
        data=go.Cone(
            x=X.flatten(),
            y=Y.flatten(),
            z=np.zeros_like(X).flatten(), 
            u=dx_dt_norm.flatten() * escala_vector,
            v=dy_dt_norm.flatten() * escala_vector,
            w=np.zeros_like(X).flatten(), 
            sizemode="absolute",
            sizeref=escala_vector * 0.5, 
            colorscale=[[0, '#3498db'], [1, '#2c3e50']], 
            colorbar=None,
            showscale=False,
            anchor="tail" 
        )
    )

    
    fig.add_trace(go.Scatter(
        x=[-rango_x, rango_x], y=[0, 0], mode='lines', name='Eje X',
        line=dict(color='red', width=1), showlegend=False
    ))
    fig.add_trace(go.Scatter(
        x=[0, 0], y=[-rango_y, rango_y], mode='lines', name='Eje Y',
        line=dict(color='red', width=1), showlegend=False
    ))

    
    fig.update_layout(
        scene=dict(
            xaxis=dict(range=[-rango_x, rango_x], title='X', showgrid=True, zeroline=False, gridcolor='#e0e0e0'),
            yaxis=dict(range=[-rango_y, rango_y], title='Y', showgrid=True, zeroline=False, gridcolor='#e0e0e0'),
            zaxis=dict(range=[-0.1, 0.1], title='Z', showgrid=False, zeroline=False, showticklabels=False), # Ocultar Z
            aspectmode='data', 
        ),
        scene_camera_eye=dict(x=0, y=0, z=2.5), 
        scene_camera_up=dict(x=0, y=1, z=0),
        scene_camera_center=dict(x=0, y=0, z=0),
        title_text='<b>Visualización del Campo Vectorial</b>',
        title_font=dict(size=22, color='#2c3e50'),
        margin=dict(l=40, r=40, t=80, b=40),
        paper_bgcolor='white', plot_bgcolor='#f9f9f9',
        font=dict(family='Poppins', size=12, color='black'),
        height=600 
    )
   
    fig.update_scenes(
        xaxis_visible=True, yaxis_visible=True, zaxis_visible=False,
        camera_projection_type='orthographic',
        bgcolor='rgba(0,0,0,0)' 
    )


    
    magnitudes_validas = magnitudes[magnitudes > 0] 
    min_magnitud = np.min(magnitudes_validas) if magnitudes_validas.size > 0 else 0
    max_magnitud = np.max(magnitudes_validas) if magnitudes_validas.size > 0 else 0

    fig.add_annotation(
        text=f"Magnitud: min {min_magnitud:.2f}, max {max_magnitud:.2f}",
        xref="paper", yref="paper",
        x=1, y=-0.1, showarrow=False,
        font=dict(size=10, color="#555")
    )

    return fig

def generar_modelo_sir(N, I0, beta, gamma, T):
    """
    Resuelve el modelo SIR y genera una gráfica.
    """
   
    t = np.linspace(0, T, T*5) 
    
   
    S0 = N - I0
    R0 = 0
    y0 = S0, I0, R0 


    def deriv(y, t, N, beta, gamma):
        S, I, R = y
        dSdt = - (beta * S * I) / N
        dIdt = (beta * S * I) / N - (gamma * I)
        dRdt = gamma * I
        return dSdt, dIdt, dRdt

  
    ret = odeint(deriv, y0, t, args=(N, beta, gamma))
    S, I, R = ret.T

   
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=t, y=S, mode='lines', name='Susceptibles (S)',
        line=dict(color='#3498db', width=3),
        hovertemplate='Día %{x:.0f}<br>Susceptibles: %{y:.0f}<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=t, y=I, mode='lines', name='Infectados (I)',
        line=dict(color='#e74c3c', width=3),
        hovertemplate='Día %{x:.0f}<br>Infectados: %{y:.0f}<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=t, y=R, mode='lines', name='Recuperados (R)',
        line=dict(color='#27ae60', width=3),
        hovertemplate='Día %{x:.0f}<br>Recuperados: %{y:.0f}<extra></extra>'
    ))

    
    fig.update_layout(
        title='<b>Evolución del Modelo SIR</b>',
        title_font=dict(size=22, color='#2c3e50'),
        xaxis_title='Tiempo (días)',
        yaxis_title='Número de personas',
        paper_bgcolor='white',
        plot_bgcolor='#f9f9f9', 
        font=dict(family='Poppins', size=12, color='black'),
        margin=dict(l=40, r=40, t=80, b=40),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        hovermode='x unified'
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#e0e0e0', range=[0, T])
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#e0e0e0', range=[0, N*1.05])
    
    return fig

def generar_modelo_seir(N, E0, I0, beta, sigma, gamma, T):
    """
    Resuelve el modelo SEIR y genera una gráfica.
    N = Población total
    E0 = Expuestos iniciales
    I0 = Infectados iniciales
    beta = Tasa de transmisión
    sigma = Tasa de incubación (1/periodo de incubación)
    gamma = Tasa de recuperación (1/duración de la infección)
    T = Tiempo de simulación
    """
    
    t = np.linspace(0, T, T*5)
    
   
    R0 = 0
    S0 = N - E0 - I0
    y0 = S0, E0, I0, R0 


    def deriv(y, t, N, beta, sigma, gamma):
        S, E, I, R = y
        dSdt = - (beta * S * I) / N
        dEdt = (beta * S * I) / N - (sigma * E)
        dIdt = (sigma * E) - (gamma * I)
        dRdt = gamma * I
        return dSdt, dEdt, dIdt, dRdt


    ret = odeint(deriv, y0, t, args=(N, beta, sigma, gamma))
    S, E, I, R = ret.T

   
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=t, y=S, mode='lines', name='Susceptibles (S)',
        line=dict(color='#3498db', width=3),
        hovertemplate='Día %{x:.0f}<br>Susceptibles: %{y:.0f}<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=t, y=E, mode='lines', name='Expuestos (E)',
        line=dict(color='#f39c12', width=3, dash='dash'), 
        hovertemplate='Día %{x:.0f}<br>Expuestos: %{y:.0f}<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=t, y=I, mode='lines', name='Infectados (I)',
        line=dict(color='#e74c3c', width=3),
        hovertemplate='Día %{x:.0f}<br>Infectados: %{y:.0f}<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=t, y=R, mode='lines', name='Recuperados (R)',
        line=dict(color='#27ae60', width=3),
        hovertemplate='Día %{x:.0f}<br>Recuperados: %{y:.0f}<extra></extra>'
    ))

    
    fig.update_layout(
        title='<b>Evolución del Modelo SEIR</b>',
        title_font=dict(size=22, color='#2c3e50'),
        xaxis_title='Tiempo (días)',
        yaxis_title='Número de personas',
        paper_bgcolor='white',
        plot_bgcolor='#f9f9f9', 
        font=dict(family='Poppins', size=12, color='black'),
        margin=dict(l=40, r=40, t=80, b=40),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        hovermode='x unified'
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#e0e0e0', range=[0, T])
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#e0e0e0', range=[0, N*1.05])
    
    return fig


# utils/funciones.py (Añadir al final)
import requests

def obtener_datos_covid_actuales(pais):
    """Consulta la API de disease.sh para datos actuales"""
    try:
        url = f"https://disease.sh/v3/covid-19/countries/{pais}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def obtener_datos_covid_historicos(pais, dias):
    
    try:
        # 'all' trae todo el historial, si es un número trae esos días
        url = f"https://disease.sh/v3/covid-19/historical/{pais}?lastdays={dias}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def buscar_personajes_rickmorty(nombre):
    
    try:
        url = f"https://rickandmortyapi.com/api/character/?name={nombre}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data['results'] # Retorna la lista de personajes
        return []
    except:
        return []
