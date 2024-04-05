from concurrent import futures
import grpc
import datanode_pb2
import datanode_pb2_grpc

class DataNodeService(datanode_pb2_grpc.DataNodeService):
    def ReplicateData(self, request, context):
        try:
            # Suponiendo que la lógica de replicación pueda lanzar una excepción
            # Lógica para replicar datos...
            return datanode_pb2.ReplicateDataResponse(success=True)
        except Exception as e:
            return datanode_pb2.ReplicateDataResponse(success=False, error_message=str(e))

    def NotifyNameNode(self, request, context):
        # Simula una notificación al NameNode
        return datanode_pb2.NotifyNameNodeResponse(success=True)

    def ReadFile(self, request, context):
        try:
            # Simula leer un archivo, puede fallar
            # Lógica para leer archivo...
            return datanode_pb2.ReadFileResponse(data=b"Contenido del archivo", success=True)
        except Exception as e:
            return datanode_pb2.ReadFileResponse(success=False, error_message=str(e))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    datanode_pb2_grpc.add_DataNodeServiceServicer_to_server(DataNodeService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
