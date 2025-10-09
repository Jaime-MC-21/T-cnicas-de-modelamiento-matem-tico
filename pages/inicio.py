import dash
from dash import html

# Registra la página en la aplicación
dash.register_page(__name__, path="/", name="Inicio")

# Define el contenido de la página de inicio con la nueva presentación
layout = html.Main([
    html.Section([
        # Contenedor para el texto de presentación
        html.Div([
            html.H1([
                "Hola, soy ",
                html.Span("Jaime Muguruza", className="nombre-destacado")
            ]),
            html.P(
                "Estudiante de Computación Científica con interés en el desarrollo backend. "
                "Me caracterizo por un enfoque analítico, precisión en el uso de conceptos "
                "técnicos y compromiso con la calidad en cada proyecto académico y de "
                "programación que realizo."
            )
        ], className="presentacion__contenido"),

        # Contenedor para la imagen
        html.Img(
            src="/assets/imagenes/foto_perfil.jpeg",
            alt="Foto de Jaime Alfredo Muguruza Cabanillas",
            className="presentacion__imagen"
        )
    ], className="presentacion")
])