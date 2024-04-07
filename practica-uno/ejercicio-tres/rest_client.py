import requests

# Consultando a un servidor RESTful
url = "http://localhost:8000/"
# GET obtener a todos los estudiantes por la ruta /pacientes
ruta_get = url + "pacientes"
get_response = requests.request(method="GET", url=ruta_get)
print("Todos los pacientes")
print(get_response.text)


# POST agrega un nuevo estudiante por la ruta /pacientes
ruta_post = url + "pacientes"
new_paciente = {
    "ci": "12345",
    "nombre": "Luis",
    "apellido": "Lopez",
    "edad": 12,
    "genero": "Masculino",
    "diagnostico": "Resfrio",
    "doctor": "Pedro Perez"
}
post_response = requests.request(method="POST", url=ruta_post, json=new_paciente)
print()
print("Paciente creado")
print(post_response.text)


# GET por diagnóstico 

ruta_diagnostico = url + "pacientes?diagnostico=Diabetes"
get_diagnostico_response = requests.request(method="GET", url=ruta_diagnostico)
print()
print("Pacientes por diagnostico")
print(get_diagnostico_response.text)


# GET por doctor 

ruta_doctor = url + "pacientes?doctor=Pedro Perez"
doctor = requests.request(method="GET", url=ruta_doctor)
print()
print("Pacientes por doctor")
print(doctor.text)


# GET buscando por CI /pacientes/{ci}
ci = 10001
ruta_ci = url + "pacientes?ci=10001"
get_ci = requests.request(method="GET", url=ruta_ci)
print()
print("Paciente por ci")
print(get_ci.text)


# PUT actualizar la información de un paciente
ruta_put = url + "pacientes/10001"
paciente_actualizado = {
    "edad": 20,
    "diagnostico": "Tuberculosis"
}
put_response = requests.request(method="PUT", url=ruta_put, json=paciente_actualizado)
print()
print("Actualizando el paciente")
print(put_response.text)

# DELETE eliminar un paciente
ruta_delete = url + "pacientes/10001"
delete_response = requests.request(method="DELETE", url=ruta_delete)
print()
print("Eliminando el paciente")
print(delete_response.text)