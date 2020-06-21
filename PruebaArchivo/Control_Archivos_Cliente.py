import socket
import os
import logging

SERVER_ADDR = '167.71.243.238'
SERVER_PORT = 9822

BUFFER_SIZE = 64 * 1024

sock = socket.socket()
sock.connect((SERVER_ADDR, SERVER_PORT))

def recibir():
    try:
        buff = sock.recv(BUFFER_SIZE)
        archivo = open('recibido', 'wb') #Aca se guarda el archivo entrante
        while buff:
            buff = sock.recv(BUFFER_SIZE) #Los bloques se van agregando al archivo
            archivo.write(buff)

        archivo.close() #Se cierra el archivo

        print("Recepcion de archivo finalizada")

    finally:
        print('Conexion al servidor finalizada')
        sock.close() #Se cierra el socket

recibir()