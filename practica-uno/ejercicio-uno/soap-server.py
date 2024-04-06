# Ejercicio 1
# Construye un servidor con el protocolo SOAP que permita a un cliente realizar 
# las operaciones de suma, resta, multiplicación y división de dos números enteros.


from http.server import HTTPServer
from pysimplesoap.server import SoapDispatcher, SOAPHandler


def suma(a, b): 
    return a+b

def resta(a, b): 
    return a-b

def producto(a, b): 
    return a*b

def division(a, b): 
    return a//b

# Creamos la ruta del servidor SOAP
dispatcher = SoapDispatcher(
    "ejemplo-soap-server",
    location="http://localhost:8000/",
    action="http://localhost:8000/",
    namespace="http://localhost:8000/",
    trace=True,
    ns=True,
)

# Registramos el servicio
dispatcher.register_function(
    "Suma", suma,
    returns={"Result": int},
    args={"a": int, "b": int}
)
dispatcher.register_function(
    "Resta", resta,
    returns={"Result": int},
    args={"a": int, "b": int}
)
dispatcher.register_function(
    "Producto", producto,
    returns={"Result": int},
    args={"a": int, "b": int}
)
dispatcher.register_function(
    "Division", division,
    returns={"Result": int},
    args={"a": int, "b": int}
)

# Iniciamos el servidor HTTP
server = HTTPServer(("0.0.0.0", 8000), SOAPHandler)
server.dispatcher = dispatcher
print("Servidor SOAP iniciado en http://localhost:8000/")
server.serve_forever()