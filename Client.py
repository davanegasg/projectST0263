import grpc
import namenode_pb2
import namenode_pb2_grpc
import datanode_pb2
import datanode_pb2_grpc

def send_file_to_namenode(stub, file_name, data):
    response = stub.SendFileToDataNode(namenode_pb2.SendFileToDataNodeRequest(file_name=file_name, data=data))
    if response.success:
        print("Operación exitosa")
    else:
        print(f"Error: {response.error_message}")

def read_file_from_datanode(datanode_address, file_name):
    channel = grpc.insecure_channel(datanode_address)
    stub = datanode_pb2_grpc.DataNodeServiceStub(channel)
    try:
        response = stub.ReadFile(datanode_pb2.ReadFileRequest(file_name=file_name))
        if response.success:
            print("Archivo leído exitosamente.")
            return response.data
        else:
            print(f"Error al leer archivo: {response.error_message}")
    except grpc.RpcError as e:
        print(f"Error de RPC: {e}")

def main():
    namenode_channel = grpc.insecure_channel('localhost:50052')
    namenode_stub = namenode_pb2_grpc.NameNodeServiceServicer(namenode_channel)

    # Ejemplo de cómo enviar un archivo al NameNode
    send_file_to_namenode(namenode_stub, "example.txt", b"datos del archivo")

    # Aquí necesitarías determinar la dirección del DataNode adecuado
    # Para este ejemplo, usaremos una dirección de ejemplo
    datanode_address = 'localhost:50051'
    file_content = read_file_from_datanode(datanode_address, "example.txt")
    if file_content:
        print(f"Contenido del archivo: {file_content}")

if __name__ == '__main__':
    main()
