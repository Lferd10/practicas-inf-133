# Ejercicio 3
# Aplicando los principios de desarrollo de Software DRY, KISS, YAGNI y la S de SOLID 
# construye un API RESTful para gestionar la información de los pacientes de un hospital. La API debe permitir:

# Crear un paciente
# Listar todos los pacientes
# Buscar pacientes por CI
# Listar a los pacientes que tienen diagnostico de Diabetes
# Listar a los pacientes que atiende el Doctor Pedro Pérez
# Actualizar la información de un paciente
# Eliminar un paciente


# De los pacientes se debe almacenar la siguiente información:

# CI (identificador único)
# Nombre
# Apellido
# Edad
# Género
# Diagnóstico
# Doctor (nombre del doctor que atiende al paciente)


# Rutas esperadas:

# POST /pacientes
# GET /pacientes
# GET /pacientes/{ci}
# GET /pacientes/?diagnostico={diagnostico}
# GET /pacientes/?doctor={doctor}
# PUT /pacientes/{ci}
# DELETE /pacientes/{ci}


from http.server import HTTPServer, BaseHTTPRequestHandler
import json

from urllib.parse import urlparse, parse_qs

pacientes = [
    {"ci": 10001, "nombre": "Juan", "apellido": "Garcia", "edad": 19, "genero": "Masculino",
    "diagnostico": "Diabetes", "doctor": "Julian",
    },
    {"ci": 10002, "nombre": "Pedro", "apellido": "Escobar", "edad": 32, "genero": "Masculino",
    "diagnostico": "Covid-19", "doctor": "Pedro Perez",
    },
    {"ci": 10010, "nombre": "Zoe", "apellido": "Castillo", "edad": 21, "genero": "Femenino",
    "diagnostico": "Diabetes", "doctor": "Pedro Perez",
    },
]

class PacientesService:
    @staticmethod
    def buscar_paciente_ci(ci):
        return next((paciente for paciente in pacientes if paciente["ci"] == ci),None)

    @staticmethod
    def buscar_paciente_diagnostico(diagnostico):
        return [paciente for paciente in pacientes if paciente["diagnostico"] == diagnostico]
    
    @staticmethod
    def buscar_paciente_doctor(doctor):
        return [paciente for paciente in pacientes if paciente["doctor"] == doctor]

    @staticmethod
    def agregar_paciente(data):
        pacientes.append(data)
        return pacientes

    @staticmethod
    def update_paciente(ci, data):
        paciente = PacientesService.buscar_paciente_ci(ci)
        if paciente:
            paciente.update(data)
            return pacientes
        else:
            return None

    @staticmethod
    def delete_paciente(ci):
        return [paciente for paciente in pacientes if paciente["ci"] != ci]


class HTTPResponseHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))


class RESTRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        if parsed_path.path == "/pacientes":
            if "diagnostico" in query_params:
                diagnostico = query_params["diagnostico"][0]
                pacientes_filt = PacientesService.buscar_paciente_diagnostico(diagnostico)
                if pacientes_filt != []:
                    HTTPResponseHandler.handle_response(
                        self, 200, pacientes_filt
                    )
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            
            elif "doctor" in query_params:
                doctor = query_params["doctor"][0]
                pacientes_filt = PacientesService.buscar_paciente_doctor(doctor)
                if pacientes_filt != []:
                    HTTPResponseHandler.handle_response(self, 200, pacientes_filt)
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            
            elif "ci" in query_params:
                ci = query_params["ci"][0]
                pacientes_filt = PacientesService.buscar_paciente_ci(ci)
                if pacientes_filt != []:
                    HTTPResponseHandler.handle_response(self, 200, pacientes_filt)
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            
            else:
                HTTPResponseHandler.handle_response(self, 200, pacientes)
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_POST(self):
        if self.path == "/pacientes":
            data = self.read_data()
            pacientes = PacientesService.agregar_paciente(data)
            HTTPResponseHandler.handle_response(self, 201, pacientes)
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_PUT(self):
        if self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[-1])
            data = self.read_data()
            pacientes = PacientesService.update_paciente(ci, data)
            if pacientes:
                HTTPResponseHandler.handle_response(self, 200, pacientes)
            else:
                HTTPResponseHandler.handle_response(self, 404, {"Error": "Paciente no encontrado"})
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_DELETE(self):
        if self.path == "/pacientes/":
            ci = self.path.split("/")[-1]
            pacientes = PacientesService.delete_paciente(ci)
            if pacientes:
                HTTPResponseHandler.handle_response(self, 200, pacientes)
            else:
                HTTPResponseHandler.handle_response(self, 404, {"Error": "Paciente no encontrado"})
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def read_data(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data


def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, RESTRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()