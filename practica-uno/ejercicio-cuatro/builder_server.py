# Ejercicio 4
# Aplica el patron de diseño BUILDER al ejercicio 3.


from http.server import BaseHTTPRequestHandler, HTTPServer
import json

pacientes = {}
# Producto: Paciente s
class Paciente:
    def __init__(self):
        self.ci = None
        self.nombre = None
        self.apellido = None
        self.edad = None
        self.genero = None
        self.diagnostico = None
        self.doctor = None

    def __str__(self):
        return f"ci: {self.ci}, nombre: {self.nombre}, apellido: {self.apellido}, edad: {self.edad}, genero: {self.genero}, diagnostico: {self.diagnostico}, doctor: {self.doctor}"

# Builder: Constructor de pacientes
class PacienteBuilder:
    def __init__(self):
        self.paciente = Paciente()

    def set_ci(self, ci):
        self.paciente.ci = ci

    def set_nombre(self, nombre):
        self.paciente.nombre = nombre

    def set_apellido(self, apellido):
        self.paciente.apellido = apellido

    def set_edad(self, edad):
        self.paciente.edad = edad

    def set_genero(self, genero):
        self.paciente.genero = genero

    def set_diagnostico(self, diagnostico):
        self.paciente.diagnostico = diagnostico

    def set_doctor(self, doctor):
        self.paciente.doctor = doctor

    def get_paciente(self):
        return self.paciente

# Director: Hospital
class Hospital:
    def __init__(self, builder):
        self.builder = builder

    def registrar_paciente(self, ci, nombre, apellido, edad, genero, diagnostico, doctor):
        self.builder.set_ci(ci)
        self.builder.set_nombre(nombre)
        self.builder.set_apellido(apellido)
        self.builder.set_edad(edad)
        self.builder.set_genero(genero)
        self.builder.set_diagnostico(diagnostico)
        self.builder.set_doctor(doctor)
        return self.builder.get_paciente()


class PacientesService:
    def __init__(self):
        self.builder = PacienteBuilder()
        self.hospital = Hospital(self.builder)
    
    def registrar_paciente(self, post_data):
        ci = post_data.get('ci')
        nombre = post_data.get('nombre')
        apellido = post_data.get('apellido')
        edad = post_data.get('edad')
        genero = post_data.get('genero')
        diagnostico = post_data.get('diagnostico')
        doctor = post_data.get('doctor')

        paciente = self.hospital.registrar_paciente(ci, nombre, apellido, edad, genero, diagnostico, doctor)
        pacientes[ci] = paciente
        return paciente

    def lista_pacientes(self):
        return [paciente.__dict__ for paciente in pacientes]
    
    def eliminar_paciente(self, ci):
        if ci in pacientes:
            return pacientes.pop(ci)
        else:
            return None

    def buscar_paciente_ci(self, ci):
        if ci in pacientes:
            return pacientes[ci]
        else:
            return None

    def buscar_paciente_diagnostico(self, diagnostico):
        return [paciente for paciente in pacientes.values() if paciente.diagnostico == diagnostico]

    def buscar_paciente_doctor(self, doctor):
        return [paciente for paciente in pacientes.values() if paciente.doctor == doctor]
    


# Manejador de solicitudes HTTP
class PacienteHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/pizza':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            data = json.loads(post_data.decode('utf-8'))

            tamaño = data.get('tamaño', None)
            masa = data.get('masa', None)
            toppings = data.get('toppings', [])

            builder = PizzaBuilder()
            pizzeria = Pizzeria(builder)

            pizza = pizzeria.create_pizza(tamaño, masa, toppings)

            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            response = {
                'tamaño': pizza.tamaño,
                'masa': pizza.masa,
                'toppings': pizza.toppings
            }

            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run(server_class=HTTPServer, handler_class=PizzaHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Iniciando servidor HTTP en puerto {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()