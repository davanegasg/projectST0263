from concurrent import futures
import time

import grpc
import files_pb2
import files_pb2_grpc

class FilesServicer(files_pb2_grpc.FileManagerServicer):
    def SendFile(self, request, context):
        print("Send file request made")
        print(request)
        file_response = files_pb2.FileResponse()
        file_response.message = f"Filed sended: {request.filename}"
        return file_response

    def ListFiles(self, request, context):
        return super().ListFiles(request, context)

    def FileSavedNotification(self, request, context):
        return super().FileSavedNotification(request, context)

    def FileReplicatedNotification(self, request, context):
        return super().FileReplicatedNotification(request, context)

    def ReplicateFile(self, request, context):
        return super().ReplicateFile(request, context)

def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    files_pb2_grpc.add_FileManagerServicer_to_server(FilesServicer(), server)
    server.add_insecure_port("localhost:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    server()
