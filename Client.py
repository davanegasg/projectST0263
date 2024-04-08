import files_pb2
import files_pb2_grpc
import grpc
import aiohttp #Libreria para realizar request de forma asincrona
import asyncio
import os


GROUP_1_PORTS = [50051, 50052, 50053]
GROUP_2_PORTS = [50101, 50102, 50103]

# Define el nombre del archivo que quieres enviar desde la carpeta testData
file_name = "test-2.txt"  # Reemplaza esto con el nombre real del archivo

async def run():
    print("1. Send File")
    print("2. List Files")
    rpc_call = input("What do you want to do: ")

    if rpc_call == "1":
        file_path = input("Ingrese la ruta completa del archivo a enviar: ")
        if file_path and os.path.exists(file_path):
            # Envía el archivo y espera la respuesta para determinar el grupo
            response = await send_file(file_path)  # Asumiendo que la respuesta incluye el grupo
            if not response:
                print("Fallo al enviar el archivo o al determinar el grupo.")
                return

            try:
                group = response
                print(group)
                if group not in [1, 2]:
                    print("Respuesta del servidor no incluyó un grupo válido.")
                    return
            except Exception as e:
                print(f"Error al procesar la respuesta del servidor: {e}")
                return

            # Obtiene los puertos activos y selecciona basado en el grupo
            active_ports = await get_active_ports()
            group_ports = GROUP_1_PORTS if group == 1 else GROUP_2_PORTS
            active_group_ports = [port for port in group_ports if port in active_ports]
            if active_group_ports:
                # Si hay puertos activos en el grupo, envía el archivo al primer puerto activo
                send_to_datanode_1(file_path, active_group_ports[0])
            else:
                print(f"No hay datanodes activos en el grupo {group}.")
        else:
            print("Ruta de archivo no válida o archivo no encontrado.")
    elif rpc_call == "2":
        # Llama a la función para obtener las ubicaciones de todos los archivos
        all_file_locations = await get_all_file_locations()
        print("Ubicaciones de todos los archivos:")
        for filename, ports in all_file_locations.items():
            print(f"{filename}: {ports}")

async def get_active_ports():
    urls = [
        'http://127.0.0.1:5098/active-nodes',
        'http://127.0.0.1:5099/active-nodes'
    ]

    async with aiohttp.ClientSession() as session:
        for url in urls:
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('active_ports', [])
                    else:
                        print(f"Error al obtener nodos activos desde {url}, código de estado: {response.status}")
            except Exception as e:
                print(f"Excepción al obtener nodos activos desde {url}: {e}")
        # Si llegamos aquí, significa que todas las solicitudes fallaron
        print("No se pudo obtener la lista de nodos activos de ninguna de las URLs.")
        return []


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
                        response_json = await response.json()
                        group = response_json.get('group')
                        return group  # Devuelve el grupo para su uso posterior
                    else:
                        print(f"Error al enviar archivo a {url}, código de estado: {response.status}")
            except Exception as e:
                print(f"Excepción al enviar archivo a {url}: {e}")

        # Si llegamos aquí, significa que todas las solicitudes fallaron
        return "Todas las solicitudes fallaron."


def send_to_datanode_1(file_path, port):
    address = f'localhost:{port}'
    with grpc.insecure_channel(address) as channel:
        stub = files_pb2_grpc.FileManagerStub(channel)
        with open(file_path, 'rb') as file:
            file_bytes = file.read()

        file_name = os.path.basename(file_path)
        file_request = files_pb2.FileRequest(filename=file_name, content=file_bytes)
        try:
            file_response = stub.SendFile(file_request)
            print("File successfully added:", file_response)
        except Exception as e:
            print(f"Failed to send file to {address}: {e}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())