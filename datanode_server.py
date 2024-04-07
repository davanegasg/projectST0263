from concurrent import futures
import time

import grpc
import files_pb2
import files_pb2_grpc
import sys
import os
import requests
import atexit



# Establecer la verbosidad de gRPC a ERROR para suprimir mensajes detallados
os.environ['GRPC_VERBOSITY'] = 'ERROR'

GROUP_1_PORTS = [50001, 50002]
GROUP_2_PORTS = [50101, 50102]

# Un diccionario simple para rastrear los puertos en uso (esta información no persistirá entre ejecuciones del script)
PORTS_IN_USE = []

class FilesServicer(files_pb2_grpc.FileManagerServicer):
    def __init__(self, group, port):
        self.group = group
        self.port = port

    def SendFile(self, request, context):
        folder_path = f"./group_{self.group}_port_{self.port}"
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, request.filename)
        with open(file_path, 'wb') as file:
            file.write(request.content)
        print(f"Archivo {request.filename} guardado en {folder_path}")

        # Aquí iría la lógica de replicación (ver paso 2)
        file_response = files_pb2.FileResponse()
        file_response.message = f"Archivo enviado: {request.filename}"
        # Añade puertos que guardaron el archivo a la respuesta
        # file_response.ports.extend([self.port])  # Ejemplo, ajustar con lógica de replicación
        return file_response

    def ListFiles(self, request, context):
        return super().ListFiles(request, context)

    def FileSavedNotification(self, request, context):
        return super().FileSavedNotification(request, context)

    def FileReplicatedNotification(self, request, context):
        return super().FileReplicatedNotification(request, context)

    def ReplicateFile(self, request, context):
        return super().ReplicateFile(request, context)

def send_health_check(port):
    try:
        # Asume que el endpoint del health check está en /health-check en el namenode_server
        url = f'http://localhost/health-check'
        response = requests.post(url, json={'port': port})
        print("Respuesta del HealthChecker:", response.text)
    except Exception as e:
        print(f"Error al realizar el health check: {e}")

def unregister_port(port):
    try:
        url = 'http://localhost/delete-port'  # Asume este endpoint en namenode_server para eliminar un puerto
        response = requests.post(url, json={'port': port})
        print(f"Unregister port response: {response.text}")
    except Exception as e:
        print(f"Error al intentar eliminar el puerto {port}: {e}")


def start_datanode_server(port_group, group_number):
    for port in port_group:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        servicer = FilesServicer(group=group_number, port=port)
        files_pb2_grpc.add_FileManagerServicer_to_server(servicer, server)
        server_address = f"localhost:{port}"
        try:
            port_binding_result = server.add_insecure_port(server_address)
            if port_binding_result == 0:
                raise RuntimeError(f"Failed to bind to address {server_address}")
            server.start()
            print(f"DataNode iniciado en {server_address} del grupo {group_number}")

            # Enviar petición de HealthChecker al namenode_server
            send_health_check(port)

            # Registra la función de limpieza para desregistrar el puerto al terminar
            atexit.register(unregister_port, port)

            server.wait_for_termination()
            return
        except RuntimeError as e:
            print(f"No se pudo iniciar el DataNode en el puerto {port}: {e}")
    print(f"No hay puertos disponibles en el grupo {group_number} para iniciar un DataNode.")



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python datanode_server.py {group}")
        sys.exit(1)

    group = sys.argv[1]

    if group == "1":
        start_datanode_server(GROUP_1_PORTS, group)
    elif group == "2":
        start_datanode_server(GROUP_2_PORTS, group)
    else:
        print("Grupo no válido. Por favor, especifique 1 o 2.")
