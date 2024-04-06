import requests

# Definir la URL del servidor GraphQL
url = 'http://localhost:8000/graphql'

# Definir la consulta GraphQL simple
query_lista = """
{
        plantas{
            id
            nombre
            especie
            edad
            altura
            frutos
        }
    }
"""
# Solicitud POST al servidor GraphQL
# response = requests.post(url, json={'query': query_lista})
# print(response.text)



# Definir la consulta GraphQL para crear nuevo estudiante
query_crear = """
mutation {
        crearPlanta(nombre: "Romero", especie: "Hierba", edad: "2 meses", altura: 1.30, frutos: False) {
            planta{
                id
                nombre
                especie
                edad
                altura
                frutos
            }
        }
    }
"""

response_mutation = requests.post(url, json={'query': query_crear})
print(response_mutation.text)

# Lista de todos los estudiantes
response = requests.post(url, json={'query': query_lista})
print(response.text)



# Definir la consulta GraphQL con parametros
query = """
    {
        plantaId(id: 2){
            id
            nombre
            especie
        }
    }
"""

# Solicitud POST al servidor GraphQL
response = requests.post(url, json={'query': query})
print(response.text)



# Definir la consulta GraphQL para eliminar un estudiante
query_eliminar = """
mutation {
        deletePlanta(id:1) {
            planta{
                id
                nombre
                especie
                altura
                frutos
            }
        }
    }
"""

response_mutation = requests.post(url, json={'query': query_eliminar})
print(response_mutation.text)

# Lista de todos los estudiantes
response = requests.post(url, json={'query': query_lista})
print(response.text)

