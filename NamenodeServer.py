from concurrent import futures
import grpc
import namenode_pb2
import namenode_pb2_grpc
import flask
from flask import Flask, request, jsonify

class NameNodeService(namenode_pb2_grpc.NameNodeService):
    def SendFileToDataNode(self, request, context):
        # Intenta enviar el archivo a un DataNode
        return namenode_pb2.SendFileToDataNodeResponse(success=True)

    def ReceiveResponseFromDataNode(self, request, context):
        # Procesa la respuesta de un DataNode
        return namenode_pb2.ReceiveResponseFromDataNodeResponse(acknowledged=True)

    def GetFileRegistry(self, request, context):
        # Devuelve el registro de archivos
        return namenode_pb2.FileRegistryResponse(success=True)

def start_grpc_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    namenode_pb2_grpc.add_NameNodeServiceServicer_to_server(NameNodeService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("gRPC server running on port 50052")
    # No llames a server.wait_for_termination() aquí

app = Flask(__name__)

@app.route('/files', methods=['GET', 'POST'])
def handle_files():
    if request.method == 'POST':
        # Lógica para manejar la subida de archivos
        return jsonify({"status": "File uploaded", "success": True})
    elif request.method == 'GET':
        # Lógica para manejar la obtención de archivos
        return jsonify({"files": ["file1", "file2"], "success": True})

if __name__ == '__main__':
    from threading import Thread
    grpc_server_thread = Thread(target=start_grpc_server)
    grpc_server_thread.start()
    app.run(debug=True, use_reloader=False)  # Flask toma el hilo principal
