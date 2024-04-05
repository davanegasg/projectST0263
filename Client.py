import grpc
import namenode_pb2
import namenode_pb2_grpc

def main():
    channel = grpc.insecure_channel('localhost:50052')
    stub = namenode_pb2_grpc.NameNodeServiceStub(channel)

    # Ejemplo de cómo enviar un comando para almacenar un archivo
    response = stub.SendFileToDataNode(namenode_pb2.SendFileToDataNodeRequest(file_name="example.txt", data=b"datos"))
    if response.success:
        print("Operación exitosa")
    else:
        print(f"Error: {response.error_message}")

if __name__ == '__main__':
    main()
