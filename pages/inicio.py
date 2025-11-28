import dash
from dash import html


dash.register_page(__name__, path="/", name="Inicio", order=0)


layout = html.Main([
    html.Section([
       
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

      
        html.Img(
            src="/assets/imagenes/foto_perfil.jpeg",
            alt="Foto de Jaime Alfredo Muguruza Cabanillas",
            className="presentacion__imagen"
        )
    ], className="presentacion")
])
