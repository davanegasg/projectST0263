from flask import Flask, request, jsonify
import files_pb2
import files_pb2_grpc
import time
import grpc

app = Flask(__name__)

@app.route("/")
def index():
    return "Flask test"

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

app.run(host="0.0.0.0", port=80)