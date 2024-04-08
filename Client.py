import files_pb2
import files_pb2_grpc
import grpc
import aiohttp #Libreria para realizar request de forma asincrona
import asyncio 
import os



# La URL del endpoint al cual quieres enviar el archivo
url = 'http://127.0.0.1:5000/check-size'

# Define el nombre del archivo que quieres enviar desde la carpeta testData
file_name = "test-2.txt"  # Reemplaza esto con el nombre real del archivo

async def run():
    print("1. Send File")
    print("2. List Files")
    rpc_call = input("What do you want to do: ")

    if rpc_call == "1":
        # Solicita al usuario que ingrese la ruta del archivo
        file_path = input("Ingrese la ruta completa del archivo a enviar: ")
        
        # Verifica que la ruta del archivo no esté vacía y que el archivo exista
        if file_path and os.path.exists(file_path):
            # Envía el archivo y espera la respuesta
            response = await send_file(file_path)  # Actualizado para usar la nueva definición de send_file
            # Maneja la respuesta
            print(response)
            send_to_datanode_1(file_path)
        else:
            print("Ruta de archivo no válida o archivo no encontrado.")
    elif rpc_call == "2":
        # Llama a la función para obtener las ubicaciones de todos los archivos
        all_file_locations = await get_all_file_locations()
        print("Ubicaciones de todos los archivos:")
        for filename, ports in all_file_locations.items():
            print(f"{filename}: {ports}")

async def get_all_file_locations():
    urls = ['http://127.0.0.1:5098/all-files-locations', 'http://127.0.0.1:5099/all-files-locations']

    async with aiohttp.ClientSession() as session:
        for url in urls:
            try:
                async with session.get(url) as response:
                    # Verifica si la respuesta es exitosa
                    if response.status == 200:
                        response_json = await response.json()
                        return response_json
                    else:
                        print(f"Error al obtener ubicaciones de archivos desde {url}, código de estado: {response.status}")
            except Exception as e:
                print(f"Excepción al obtener ubicaciones de archivos desde {url}: {e}")

    # Si llegamos aquí, significa que todas las solicitudes fallaron
    return "No se pudieron obtener las ubicaciones de los archivos."



async def send_file(file_path):
    urls = ['http://127.0.0.1:5098/check-size', 'http://127.0.0.1:5099/check-size']
    
    # Abre el archivo en modo binario y lee su contenido de manera sincrónica
    with open(file_path, 'rb') as f:
        file_content = f.read()

    async with aiohttp.ClientSession() as session:
        for url in urls:
            try:
                # Prepara los datos para enviar
                data = aiohttp.FormData()
                data.add_field('file', file_content, filename=os.path.basename(file_path))
                
                # Intenta realizar la solicitud POST de manera asíncrona
                async with session.post(url, data=data) as response:
                    # Si la solicitud es exitosa, retorna la respuesta
                    if response.status == 200:
                        response_text = await response.text()
                        return response_text
                    else:
                        print(f"Error al enviar archivo a {url}, código de estado: {response.status}")
            except Exception as e:
                print(f"Excepción al enviar archivo a {url}: {e}")
        
        # Si llegamos aquí, significa que todas las solicitudes fallaron
        return "Todas las solicitudes fallaron."


def send_to_datanode_1(file_path):
    with grpc.insecure_channel('localhost:50001') as channel:
        stub = files_pb2_grpc.FileManagerStub(channel)
        with open(file_path, 'rb') as file:
            file_bytes = file.read()

        # Obtiene solo el nombre del archivo de la ruta completa
        file_name = os.path.basename(file_path)
        file_request = files_pb2.FileRequest(filename=file_name, content=file_bytes)
        file_response = stub.SendFile(file_request)
        print("File successfully added")
        print(file_response)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())