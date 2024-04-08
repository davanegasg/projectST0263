from flask import Flask, request, jsonify

app = Flask(__name__)

PORTS_LIST = []
FILE_PORTS_MAP = {}


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
            FILE_PORTS_MAP[filename].append(port)
    else:
        FILE_PORTS_MAP[filename] = [port]

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

app.run(host="0.0.0.0", port=5000)