import files_pb2
import files_pb2_grpc
import time
import grpc
#import requests #Libreria para realizar las request
import aiohttp #Libreria para realizar request de forma asincrona
import asyncio 
import os
import tkinter as tk
from tkinter import filedialog
import aiofiles


# La URL del endpoint al cual quieres enviar el archivo
url = 'http://127.0.0.1:80/check-size'

# Define el nombre del archivo que quieres enviar desde la carpeta testData
file_name = "test-2.txt"  # Reemplaza esto con el nombre real del archivo

async def run():
    print("1. Send File")
    print("2. List Files")
    rpc_call = input("What u want to do: ")

    if rpc_call == "1":
        # Configura la ventana de selección de archivo
        root = tk.Tk()
        #root.withdraw()  # Oculta la ventana principal de tkinter
        file_path = filedialog.askopenfilename()  # Muestra el diálogo de selección de archivo
        # Comprueba si se seleccionó un archivo
        if file_path:
            # Envía el archivo y espera la respuesta
            response = await send_file(url, file_path)
            # Maneja la respuesta
            print(response)
            send_to_datanode_1(file_path)
        else:
            print("No se seleccionó ningún archivo.")
    elif rpc_call == "2":
            print("Not implemented")

async def send_file(url, file_path):
    # Abre el archivo en modo binario y lee su contenido de manera sincrónica
    with open(file_path, 'rb') as f:
        file_content = f.read()

    # Ahora entra al contexto asincrónico
    async with aiohttp.ClientSession() as session:
        # Prepara los datos para enviar, nota que 'data' ahora se construye de manera diferente
        data = {'file': file_content}
        # Realiza la solicitud POST de manera asíncrona
        async with session.post(url, data=data) as response:
            # Espera y lee la respuesta
            response_text = await response.text()
            return response_text

def send_to_datanode_1(file_path):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = files_pb2_grpc.FileManagerStub(channel)
        with open(file_path, 'rb') as file:
            file_bytes = file.read()

        # Obtiene solo el nombre del archivo de la ruta completa
        file_name = os.path.basename(file_path)
        file_request = files_pb2.FileRequest(filename =file_name, content=file_bytes)
        file_response = stub.SendFile(file_request)
        print("File successfully added")
        print(file_response)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())