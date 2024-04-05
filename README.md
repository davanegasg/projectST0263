## git install...
pip install grpcio
pip install grpcio-tools

## Comando para correr proto python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. datanode.proto namenode.proto