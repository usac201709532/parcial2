#socket.sendfile() disponible desde Python 3.3
from socket import socket, error
import threading #Concurrencia con hilos
import time      #Retardos
import logging   #Logging
import sys       #Requerido para salir (sys.exit())

SERVER_ADDR = ''
SERVER_PORT = 9822

BUFFER_SIZE = 64 * 1024 #64 KB para buffer de transferencia de archivos


class arch(object):

    def enviar():
        server_socket = socket()
        server_socket.bind((SERVER_ADDR, SERVER_PORT))
        server_socket.listen(0) #1 conexion activa y 9 en cola
        print("\nEsperando conexion remota...\n")
        conn, addr = server_socket.accept()
        try:
            while True:
                print('Conexion establecida desde ', addr)
                print('Enviando Audio...')

                audio = open('servi.wav', 'rb') 
                archivo = audio.read(64*1024)
                while archivo:
                    conn.sendfile(audio)
                    archivo = audio.read(64*1024)
                audio.close()
                conn.close()
                print("\n\nArchivo enviado a: ", addr)
                break
        finally:
            print("Cerrando el servidor...")
            server_socket.close()

    def recibir():
        server_socket = socket()
        server_socket.bind((SERVER_ADDR, SERVER_PORT))
        server_socket.listen(0) #1 conexion activa y 9 en cola
        
        conn, addr = server_socket.accept()
        audior = open("servi.wav", "wb")

        while True:
            try:
                input_data = conn.recv(40*1024) #Aca se guarda el archivo entrante
            except error:
                pirnt("Error de lectura")
                break
            else:
                if input_data:
                    if isinstance(input_data, bytes):
                        end = input_data[0] == 1
                    else:
                        end = input_data == chr(1)
                    if not end:
                        audior.write(input_data)
                    else:
                        break
                    print("Se ha recibido el archivo")
        audior.close()
        server_socket.close()

if __name__ == "__main__":
    arch.enviar()
