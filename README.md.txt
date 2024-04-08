# info de la materia: ST0263 Tópicos Especiales de Telemática
#
# Estudiante(s): Diego Alejandro Vanegas González, davanegasg@eafit.edu.co
#
# Profesor: Juan Carlos Montoya Mendoza, jcmontoy@eafit.edu.co


# Reto No 1 y 2: P2P - Comunicación entre procesos mediante API REST, RPC y MOM
#
# 1. 
Realizar el diseño e implementación de un sistema P2P donde cada nodo / proceso contiene uno
o más microservicios que soportan un sistema de compartición de archivos distribuido y
descentralizado.
## 1.1. Que aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)
Cumplí con implementar 2 servicios Dummy (Download y Upload)
Implementar Middleware API REST y MOM
Cada Peer contiene 2 Modulos, Servidor y Cliente.
Archivo de configuración peer_config.json para cada Peer
Bootstrap.py para ejecutar todos los servidores y clientes y utilizar sus servicios mediante API REST
MOM Esta escuchando cada petición para notificar las peticiones que se realicen

## 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

Implementación del Middleware gRPC
Utilizar dos lenguajes de programación

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
