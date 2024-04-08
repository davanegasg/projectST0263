from flask import Flask, request, jsonify
import os
import sys
import socket
import requests


app = Flask(__name__)

PORTS_LIST = []
FILE_PORTS_MAP = {}

GROUPS_PORTS = {
    "1": [50001, 50002, 50003],
    "2": [50101, 50102],
}

@app.route("/")
def index():
    return "Flask test"

@app.route('/health-check', methods=['POST'])
def health_check():
    data = request.json
    port = data.get('port')
    if port and port not in PORTS_LIST:
        PORTS_LIST.append(port)
        print(f"Health check recibido del puerto {port}. Puerto añadido a la lista.")
    else:
        print(f"Health check recibido del puerto {port}. Puerto ya presente en la lista.")
    return jsonify({"message": "Health check recibido", "ports": PORTS_LIST})

@app.route('/active-nodes', methods=['GET'])
def get_active_nodes():
    return jsonify({"active_ports": PORTS_LIST})

@app.route('/register-file', methods=['POST'])
def register_file():
    data = request.json
    filename = data.get('filename')
    port = data.get('port')

    if not filename or port is None:
        return jsonify({"error": "Filename and port are required."}), 400

    if filename in FILE_PORTS_MAP:
        if port not in FILE_PORTS_MAP[filename]:
            print(f"File {filename} saved on {port}")
            FILE_PORTS_MAP[filename].append(port)
    else:
        print(f"File {filename} saved on {port}")
        FILE_PORTS_MAP[filename] = [port]

    replicate_file_ports_map_to_other_namenode()
    return jsonify({"message": f"Archivo {filename} registrado en el puerto {port}."})


@app.route('/file-locations/<filename>', methods=['GET'])
def file_locations(filename):
    if filename in FILE_PORTS_MAP:
        ports = FILE_PORTS_MAP[filename]
        return jsonify({"filename": filename, "ports": ports})
    else:
        return jsonify({"error": f"Archivo {filename} no encontrado."}), 404

@app.route('/all-files-locations', methods=['GET'])
def all_file_locations():
    return jsonify(FILE_PORTS_MAP)


@app.route('/delete-port', methods=['POST'])
def delete_port():
    data = request.json
    port = data.get('port')
    if port in PORTS_LIST:
        PORTS_LIST.remove(port)
        message = f"Puerto {port} eliminado de la lista."
    else:
        message = f"El puerto {port} no se encontraba en la lista."
    return jsonify({"message": message, "ports": PORTS_LIST})


@app.route('/check-size', methods=['POST'])
def check_size():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Intenta obtener el tamaño del archivo directamente del objeto file
    file.seek(0, 2) # Mueve el cursor al final del archivo
    file_size = file.tell() / 1024 # Obtiene el tamaño del archivo en KB
    file.seek(0) # Regresa el cursor al inicio del archivo para futuras operaciones

    # Devuelve 1 si el archivo es mayor a 50 KB, de lo contrario devuelve 2
    if file_size > 50:
        return jsonify({"group": 1}), 200
    else:
        return jsonify({"group": 2}), 200

@app.route('/update-file-ports-map', methods=['POST'])
def update_file_ports_map():
    global FILE_PORTS_MAP  # Asegúrate de usar la variable global
    incoming_map = request.json
    FILE_PORTS_MAP = incoming_map  # Actualiza el mapa actual con el recibido
    return jsonify({"message": "FILE_PORTS_MAP actualizado exitosamente"}), 200


def scan_and_update_file_ports_map():
    for group, ports in GROUPS_PORTS.items():
        for port in ports:
            # Construye el path del directorio basado en el grupo y puerto
            dir_path = f"./group_{group}_port_{port}"

            # Verifica si el directorio existe
            if os.path.exists(dir_path) and os.path.isdir(dir_path):
                # Lista todos los archivos en el directorio
                for filename in os.listdir(dir_path):
                    file_path = os.path.join(dir_path, filename)
                    # Verifica si es un archivo y no un directorio/subdirectorio
                    if os.path.isfile(file_path):
                        # Si el archivo ya está registrado, añade el puerto si aún no está listado
                        if filename in FILE_PORTS_MAP:
                            if port not in FILE_PORTS_MAP[filename]:
                                FILE_PORTS_MAP[filename].append(port)
                        else:
                            FILE_PORTS_MAP[filename] = [port]

def check_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("127.0.0.1", port))
            return True
        except socket.error:
            return False

def replicate_file_ports_map_to_other_namenode():
    # Determina el puerto del otro namenode server
    other_namenode_port = 5098 if port == 5099 else 5099
    other_namenode_url = f"http://127.0.0.1:{other_namenode_port}/update-file-ports-map"

    try:
        # Envía FILE_PORTS_MAP al otro namenode server
        response = requests.post(other_namenode_url, json=FILE_PORTS_MAP)
        if response.status_code == 200:
            print(f"Replicación exitosa al namenode en el puerto {other_namenode_port}")
        else:
            print(f"Fallo la replicación al namenode en el puerto {other_namenode_port}: {response.status_code}")
    except Exception as e:
        print(f"Error al replicar a namenode en el puerto {other_namenode_port}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please use: python namenode_server.py {port}")
        sys.exit(1)

    port = int(sys.argv[1])  # Convierte el argumento a entero

    # Verifica si el puerto está en el rango permitido
    if port not in [5098, 5099]:
        print("Puerto no válido. Por favor, use 5098 o 5099.")
        sys.exit(1)

    if check_port(port):
        scan_and_update_file_ports_map()
        app.run(host="0.0.0.0", port=port)
    else:
        print(f"El puerto {port} ya está en uso. Por favor, intente con otro puerto.")
