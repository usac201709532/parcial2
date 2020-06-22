from socket import socket
import os
import logging

SERVER_ADDR = ''
SERVER_PORT = 9822
BUFFER_SIZE = 64 * 1024



def recibir():
    sock = socket()
    sock.connect((SERVER_ADDR, SERVER_PORT))
    try:
        buff = sock.recv(BUFFER_SIZE)
        archivo = open("recib.wav", "wb") #Aca se guarda el archivo entrante
        while buff:
            buff = sock.recv(BUFFER_SIZE) #Los bloques se van agregando al archivo
            archivo.write(buff)

        archivo.close() #Se cierra el archivo

        print("Recepcion de archivo finalizada")

    finally:
        print('Conexion al servidor finalizada')
        sock.close() #Se cierra el socket

def enviar():
    sock = socket()
    sock.connect((SERVER_ADDR, SERVER_PORT))
    
    while True:
        print("Enviando Audio...")
        audio = open('enviado.mp3', 'rb') 
        archivo = audio.read(64*1024)
        while archivo:
            sock.send(archivo)
            archivo = audio.read(64*1024)
        break
    try:
        sock.send(chr(1))
    except TypeError:
        sock.send(bytes(chr(1), "utf-8"))
    audio.close()
    sock.close()
    print("Archivo Enviado")
    print("Cerrando el servidor...")


def grabar():
    logging.basicConfig(
        level = logging.DEBUG, 
        format = '%(message)s'
        )

    logging.info('Comenzando grabacion')
    os.system('arecord -d 10 -f U8 -r 8000 enviado.mp3')

    logging.info('Grabacion finalizada, inicia reproduccion')
    os.system('aplay enviado.mp3')
if __name__ == "__main__":
    recibir()