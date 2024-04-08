# info de la materia: ST0263 Tópicos Especiales de Telemática
#
# Estudiante(s): Diego Alejandro Vanegas González y Sebastián Marin Gallego, davanegasg@eafit.edu.co - smaring2@eafit.edu.co
#
# Profesor: Juan Carlos Montoya Mendoza, jcmontoy@eafit.edu.co


# PROYECTO 1: SISTEMA DE ARCHIVOS DISTRIBUIDOS
#
# 1. 
Realizar el diseño e implementación de un sistema de archivos distribuidos, que permite compartir y acceder de forma concurrente un conjunto de archivos que se encuentran almacenados en diferentes nodos. El cual, permite visualizar la ubicación de un bloque y su URI, si esta URI está caida, intenta acceder al archivo en el resto de puertos que están habilitados y contienen este archivo.

## 1.1. Que aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

- Canal de Control mediante API REST para gestionar los recursos que ingresan y salen.
- Canal de Datos mediante gRPC para enviar diversas solicitudes y realizar la escritura y lectura de bloques
 
- La escritura y lectura de los archivos, son directamente realizado entre el Cliente y el DataNode. Definimos la distribución de los bloques y su replicación mediante peticiones por gRPC
- La unidad mínima de replicación – por facilidad – se tomará como bloque.
- Un bloque al menos debe estar en dos DataNode
- La transferencia de un archivo, se hace desde cada uno de los Datanodes que contengan bloques principales o replicas. Por facilidad y producto mínimo viable, el namenode entrega al cliente la lista y el orden donde se encuentran los bloques de un archivo (lista de bloques y URI).
- A nivel de escritura de un archivo en el sistema, se realizará la transferencia directa entre el cliente y un grupo de DataNode seleccionado con un criterio de optimización del NameNode para elegir los DataNodes más adecuado de acuerdo a alguna métrica. Esta optimización, es realizada por el peso del archivo, si es el peso es menor a 50kb, se dirige al grupo de datanodes 1, sino, al grupo de datanodes 2
- Un DataNode que recibe un bloque de un Cliente se convierte en un Leader del bloque y este será encargado de replicar a otro DataNode el bloque de este archivo para Tolerancia a fallos, este segundo DataNode lo conoceremos como Follower para este archivo.

## 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

# 2. información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.

![image](https://github.com/davanegasg/projectST0263/assets/68928488/c2f03703-8046-41b5-82da-720958efa61a)

La arquitectura utilizada para este diseño es una Arquitectura P2P no estructurada con servidor descentralizado. 
Estamos comunicando cada nodo mediante API REST y utilizando MOM para guardar en la cola las notificaciones de cada petición realizada

# 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

## En AWS

1. Creamos un entorno en Linux
2. Accedemos al entorno mediante los siguientes comandos
  ```
  cd ~/.ssh
  ssh -i {nombre de la key} ec2-user@{ip de la instancia}
  ```
4. Realizamos git clone del proyecto dentro de la instancia
  ```
  git clone https://github.com/davanegasg/projectST0263.git
  ```
5. Ahora accedemos a la carpeta del proyecto
  ```
  cd projectST0263/
  ```
7. Ahora realizamos la instalación de las librerias que usamos.
  ```
  bash sudorequirements.txt
  ```
  ó con los siguientes 3 comandos
  ```
  mv sudorequirements.txt install_requirements.sh
  chmod +x install_requirements.sh
  ./install_requirements.sh
  ```
8. Ahora procedemos a inicializar el namenode primero y luego los datanodes en el orden que querramos
  ```
  sudo python3.11 namenode_server.py {puerto} //Puertos disponibles 5098 ó 5099
  sudo python3.11 datanode_server.py {grupo} {puerto} //Grupo 1 o 2 - Puertos del 50051 al 50053 para grupo 1 y para el 2 es de 50101 al 50103
  ```
9. Y ahora podemos correr el cliente 
  ```
  sudo python3.11 client.py
  ```

## En Local

1. Realizamos git clone del proyecto dentro de la instancia
  ```
  git clone https://github.com/davanegasg/projectST0263.git
  ```
2. Ahora accedemos a la carpeta del proyecto
  ```
  cd projectST0263/
  ```
3. Ahora realizamos la instalación de las librerias que usamos.
  ```
  bash sudorequirements.txt
  ```
  ó con los siguientes 3 comandos
  ```
  mv sudorequirements.txt install_requirements.sh
  chmod +x install_requirements.sh
  ./install_requirements.sh
  ```
4. Ahora procedemos a inicializar el namenode primero y luego los datanodes en el orden que querramos
  ```
  python namenode_server.py {puerto} //Puertos disponibles 5098 ó 5099
  python datanode_server.py {grupo} {puerto} //Grupo 1 o 2 - Puertos del 50051 al 50053 para grupo 1 y para el 2 es de 50101 al 50103
  ```
5. Y ahora podemos correr el cliente 
  ```
  python client.py
  ```


## descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)

namenode_server: 
- Las IPs están en 0.0.0.0 y los puertos disponibles para este son los 5098 y el 5099

datanode_server:
- Las IPs están en el localhost y los puertos disponibles para este son 50051, 50052, 50053 para el grupo 1 y 50101, 50102, 50103 para el grupo 3


## opcional - detalles de la organización del código por carpetas o descripción de algún archivo. (ESTRUCTURA DE DIRECTORIOS Y ARCHIVOS IMPORTANTE DEL PROYECTO, comando 'tree' de linux)

El proyecto está organizado por carpetas, tenemos las carpetas protos (Contiene el archivo .proto para el gRPC), downloads (Para los archivos descargados) y group\_{group}\_port\_{port} (Este contiene los archivos que se guardan, dependiendo del grupo y del puerto) y los archivos de datanode_server.py, namenode_server.py y client.py

## opcionalmente - si quiere mostrar resultados o pantallazos 
![image](https://github.com/davanegasg/projectST0263/assets/68928488/97f458ef-6039-4ac7-b528-b112dd17e13d)
![image](https://github.com/davanegasg/projectST0263/assets/68928488/2a56f6f0-9deb-4650-af3b-14f4c0a8645e)
![image](https://github.com/davanegasg/projectST0263/assets/68928488/217573a5-8457-439e-839b-4946d2049b18)
![image](https://github.com/davanegasg/projectST0263/assets/68928488/3fd09a8a-a342-4b4d-bb67-4d9d72824652)


# 4. Descripción del ambiente de EJECUCIÓN (en producción) lenguaje de programación, librerias, paquetes, etc.

Desplegamos el entorno de ejecución en AWS con Linux. 
Utilizamos python como lenguaje principal para todo el código
Librerias utilizadas: Flask, request, grpcio, grpcio-tools, aiohttp
