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

- Tenemos dos canales de comunicación
- - Canal de Control mediante API REST para gestionar los recursos que ingresan y salen.
  - Canal de Datos mediante gRPC para enviar diversas solicitudes y realizar la escritura y lectura de bloques
 
La escritura y lectura de los archivos, debe ser directamente realizado entre el Cliente y el
DataNode. Debe definir un algoritmo para distribución de los bloques y su replicación.
• La unidad mínima de replicación – por facilidad – se tomará como bloque.
• Un bloque al menos debe estar en dos DataNode
• La transferencia de un archivo, se hace desde cada uno de los Datanodes que contengan
bloques principales o replicas. Por facilidad y producto mínimo viable, el namenode
entrega al cliente la lista y el orden donde se encuentran los bloques de un archivo (lista
de bloques y URI).
• A nivel de escritura de un archivo en el sistema, se realizará la transferencia directa entre
el cliente y un grupo de DataNode seleccionado con un criterio de op:mización del
NameNode para elegir los DataNodes más adecuado de acuerdo a alguna métrica.
• Un DataNode que recibe un bloque de un Cliente se convierte en un Leader del bloque y
este será encargado de replicar a otro DataNode el bloque de este archivo para Tolerancia
a fallos, este segundo DataNode lo conoceremos como Follower para este archivo.

El envio de archivos se realiza mediante el filtrado del archivo, pasando por namenode y este nos devuelve el grupo al cual se enviará el archivo que vayamos a almacenar. De esta forma, podemos filtrar y diferentes archivos y tener una mejor gestión de nuestros recursos

Implementamos un filtro simple, que consiste en si el archivo pesa más de 50kb, se va para el grupo 2 y sino, se va para el grupo 1.

## 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

# 2. información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.

![image](https://github.com/davanegasg/davanegasg-ST0263/assets/68928488/c4d4c844-3a20-4e47-b28f-b42c61c16998)

La arquitectura utilizada para este diseño es una Arquitectura P2P no estructurada con servidor descentralizado. 
Estamos comunicando cada nodo mediante API REST y utilizando MOM para guardar en la cola las notificaciones de cada petición realizada

# 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

## Cómo se compila y ejecuta.
Se ejecuta metiante python Peer/boostrap.py
## detalles del desarrollo.
Está desarrollado con Python y con Flask para realizar las peticiones al Servidor.

## descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)
Las IP asignadas en el archivo de configuración es 0.0.0.0, los puertos cambian dependiendo del Peer, pero comienzan desde 5001

## opcional - detalles de la organización del código por carpetas o descripción de algún archivo. (ESTRUCTURA DE DIRECTORIOS Y ARCHIVOS IMPORTANTE DEL PROYECTO, comando 'tree' de linux)
## Las carpetas estan organizadas Peer como carpeta principal y dentro está cada Peer, con su archivo de configuración, servidor y cliente. Luego tenemos el archivo boostrap.py el cual nos permite ejecutar todo al mismo tiempo y realizar ciertas acciones ya programadas en este archivo como hacer un Update y un Download
## opcionalmente - si quiere mostrar resultados o pantallazos 
![image](https://github.com/davanegasg/davanegasg-ST0263/assets/68928488/f927bda5-a398-4144-a5a8-682fdaf3a56f)

# 4. Descripción del ambiente de EJECUCIÓN (en producción) lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

# IP o nombres de dominio en nube o en la máquina servidor.

## descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)

## como se lanza el servidor.

El servidor se puede lanzar utilizando python Peer/Peer1/Server.py o con python Peer/boostrap.py

## opcionalmente - si quiere mostrar resultados o pantallazos 

# 5. otra información que considere relevante para esta actividad.

# referencias:
