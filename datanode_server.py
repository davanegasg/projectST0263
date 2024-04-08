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

GROUP_1_PORTS = [50001, 50002, 50003]
GROUP_2_PORTS = [50101, 50102]

# Un diccionario simple para rastrear los puertos en uso (esta información no persistirá entre ejecuciones del script)
PORTS_IN_USE = []

URL = 'http://127.0.0.1:5000'

class FilesServicer(files_pb2_grpc.FileManagerServicer):
    def __init__(self, group, port, group_1_ports, group_2_ports):
        self.group = group
        self.port = port
        self.group_1_ports = group_1_ports
        self.group_2_ports = group_2_ports

    def get_target_ports(self, active_ports):
        current_group_ports = self.group_1_ports if self.group == "1" else self.group_2_ports
        # Filtra los puertos activos para incluir solo aquellos del mismo grupo y diferentes al actual
        target_ports = [port for port in active_ports if port in current_group_ports and port != self.port]
        return target_ports


    def SendFile(self, request, context):
        folder_path = f"./group_{self.group}_port_{self.port}"
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, request.filename)
        with open(file_path, 'wb') as file:
            file.write(request.content)
        print(f"Archivo {request.filename} guardado en {folder_path}")

        file_response = files_pb2.FileResponse(success=True, message=f"Archivo '{request.filename}' recibido y almacenado.")

        # Suponiendo que `get_active_ports()` devuelve la lista de puertos activos
        # y que `self.group` y `self.port` identifican el grupo y puerto actual del nodo
        active_ports = get_active_ports()
        target_ports = self.get_target_ports(active_ports)
        register_file_and_ports(request.filename, self.port)  # Registra en namenode_server

        print(f"Puertos a enviar{target_ports}")
        replication_request = files_pb2.ReplicateFileRequest(filename=request.filename, content=request.content, ports=target_ports)
        self.ReplicateFile(replication_request, context)
        return file_response

    def ReplicateFile(self, request, context):
        for port in request.ports:
            try:
                folder_path = f"./group_{self.group}_port_{port}"
                os.makedirs(folder_path, exist_ok=True)
                file_path = os.path.join(folder_path, request.filename)
                with open(file_path, 'wb') as file:
                    file.write(request.content)
                print(f"Archivo {request.filename} guardado en {folder_path}")

                print(f"Replicación a puerto {port} del archivo {request.filename} guardado en {folder_path}")
                register_file_and_ports(request.filename, port)  # Registra en namenode_server
            except Exception as e:
                print(f"Error al replicar el archivo a puerto {port}: {e}")

        # Preparar y devolver la respuesta
        return files_pb2.FileResponse(success=True, message=f"Replicación completada en el nodo {self.port}.")

def register_file_and_ports(filename, ports):
    try:
        url = f'{URL}/register-file'  # Asume este endpoint en namenode_server para registrar archivo y puertos
        data = {
            'filename': filename,
            'port': ports
        }
        response = requests.post(url, json=data)
        print(f"Registro de archivo y puertos en namenode_server: {response.text}")
    except Exception as e:
        print(f"Error al registrar el archivo y puertos en namenode_server: {e}")


def send_health_check(port):
    try:
        # Asume que el endpoint del health check está en /health-check en el namenode_server
        url = f'{URL}/health-check'
        response = requests.post(url, json={'port': port})
        print("Respuesta del HealthChecker:", response.text)
    except Exception as e:
        print(f"Error al realizar el health check: {e}")

def unregister_port(port):
    try:
        url = f'{URL}/delete-port'  # Asume este endpoint en namenode_server para eliminar un puerto
        response = requests.post(url, json={'port': port})
        print(f"Unregister port response: {response.text}")
    except Exception as e:
        print(f"Error al intentar eliminar el puerto {port}: {e}")

def get_active_ports():
    try:
        url = f'{URL}/active-nodes'
        response = requests.get(url)
        active_ports = response.json().get('active_ports', [])
        print("Nodos activos:", active_ports)
        return active_ports
    except Exception as e:
        print(f"Error al recuperar los nodos activos: {e}")
        return []


def start_datanode_server(port_group, group_number):
    for port in port_group:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        servicer = FilesServicer(group=group_number, port=port, group_1_ports=GROUP_1_PORTS, group_2_ports=GROUP_2_PORTS)
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
