# Ejercicio 2
# Construye un API con GraphQL para gestionar el seguimiento de las plantas de un vivero. La API debe permitir:

# Crear una planta
# Listar todas las plantas
# Buscar plantas por especie
# Buscar las plantas que tienen frutos
# Actualizar la información de una planta
# Eliminar una planta
# De las plantas se debe almacenar la siguiente información:

# ID (identificador único)
# Nombre común (nombre popular)
# Especie (nombre científico)
# Edad (en meses)
# Altura (en cm)
# Frutos (booleano)
# Rutas esperadas:

# /graphql




from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from graphene import ObjectType, String, Int, Float, Boolean, List, Schema, Field, Mutation


class Planta(ObjectType):
    id = Int()
    nombre = String()
    especie = String()
    edad = String()
    altura = Float()
    frutos = Boolean()


class Query(ObjectType):
    plantas = List(Planta)
    planta_especie = Field(Planta, especie=String())
    plantas_frutos = List(Planta)
    
    def resolve_plantas(root, info):
        return plantas
    
    def resolve_planta_especie(root, info, especie):
        for planta_especie in plantas:
            if planta_especie.especie == especie:
                return planta_especie
        return None

    def resolve_plantas_frutos(root, info):
        for plantas_frutos in plantas:
            if plantas_frutos.frutos == True:
                plantas_fruta.append(plantas_frutos)
        return plantas_fruta


class CrearPlanta(Mutation):
    class Arguments:
        nombre = String()
        especie = String()
        edad = String()
        altura = Float()
        frutos = Boolean()

    planta = Field(Planta)

    def mutate(root, info, nombre, especie, edad, altura, frutos):
        nueva_planta = Planta(
            id=len(plantas) + 1,
            nombre=nombre,
            especie=especie,
            edad = edad,
            altura = altura,
            frutos = frutos
        )
        plantas.append(nueva_planta)
        print("entro")

        return CrearPlanta(planta=nueva_planta)

class DeletePlanta(Mutation):
    class Arguments:
        id = Int()

    planta = Field(Planta)

    def mutate(root, info, id):
        for i, planta in enumerate(plantas):
            if planta.id == id:
                plantas.pop(i)
                return DeletePlanta(planta=planta)
        return None

class ActualizarPlanta(Mutation):
    class Arguments:
        id = Int()
        nombre = String()
        especie = String()
        edad = String()
        altura = Float()
        frutos = Boolean()

    planta = Field(Planta)

    def mutate(root, info, id, nombre, especie, edad, altura, frutos):
        for i, planta in enumerate(plantas):
            if planta.id == id:
                planta.nombre = nombre
                planta.especie = especie
                planta.edad = edad
                planta.altura = altura
                planta.frutos = frutos
                return ActualizarPlanta(planta=planta)
        return None



class Mutations(ObjectType):
    crear_planta = CrearPlanta.Field()
    delete_planta = DeletePlanta.Field()
    actualizar_planta = ActualizarPlanta.Field()


plantas = [
    Planta(id=1, nombre="Pino", especie="Arbol", edad="18 meses", altura=325.55, frutos=False),
    Planta(id=2, nombre="Laurel", especie="Hierba", edad="2 meses", altura=15.30, frutos=False),
    Planta(id=3, nombre="Cerezos", especie="Arbol", edad="16 meses", altura=210.30, frutos=True)
]
plantas_fruta = [
]

schema = Schema(query=Query, mutation=Mutations)


class GraphQLRequestHandler(BaseHTTPRequestHandler):
    def response_handler(self, status, data):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_POST(self):
        if self.path == "/graphql":
            content_length = int(self.headers["Content-Length"])
            data = self.rfile.read(content_length)
            data = json.loads(data.decode("utf-8"))
            print(data)
            result = schema.execute(data["query"])
            self.response_handler(200, result.data)
        else:
            self.response_handler(404, {"Error": "Ruta no existente"})


def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, GraphQLRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()