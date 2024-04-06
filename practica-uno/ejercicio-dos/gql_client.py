import requests

# Definir la URL del servidor GraphQL
url = 'http://localhost:8000/graphql'

# Definir la consulta GraphQL para listar las plantas
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



# Definir la consulta GraphQL para crear
query_crear = """
mutation {
        crearPlanta(nombre: "Romero", especie: "Hierba", edad: "2 meses", altura: 1.30, frutos: false) {
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
# Muestra la planta creada
result = requests.post(url, json={'query': query_crear})
print(result.text)


# Lista de todas las plantas
response = requests.post(url, json={'query': query_lista})
print(response.text)



# Definir la consulta GraphQL con parametros
query = """
    {
        plantaEspecie(especie: "Hierba"){
            id
            nombre
            especie
        }
    }
"""
response = requests.post(url, json={'query': query})
print(response.text)



# Definir la consulta GraphQL para eliminar una planta
query_eliminar = """
mutation {
        deletePlanta(id:1) {
            planta{
                id
                nombre
                especie
            }
        }
    }
"""
response_mutation = requests.post(url, json={'query': query_eliminar})
print(response_mutation.text)



# Definir la consulta GraphQL para actualizar una planta
query_actualizar = """
mutation {
        actualizarPlanta(id:2, nombre: "Hortensias", especie: "arbusto", edad: "3 meses", altura: 18.75, frutos: true) {
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
response_mutation = requests.post(url, json={'query': query_actualizar})
print(response_mutation.text)


# Lista de todas las plantas
response = requests.post(url, json={'query': query_lista})
print(response.text)


# Lista de todas las plantas con frutos
query = """
    {
        plantasFrutos{
            id
            nombre
            especie
            frutos
        }
    }
"""
response = requests.post(url, json={'query': query})
print(response.text)