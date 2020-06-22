import paho.mqtt.client as mqtt
import logging
import time
import os 
import datetime #Para generar fecha/hora actual
import socket

import binascii

from broker import * #Informacion de la conexion

BUFFER_SIZE = 16 * 1024
SERVER_IP   = ''
SERVER_PORT = 9816

id = "201701026"
destino = "201700000"
mensaje = ''
n = 0


def on_message(client, userdata, msg):
    #Se muestra en pantalla informacion que ha llegado
    global mensaje
    print("--------------------------------")
    mensaje = str(msg.payload.decode("utf-8"))
    print(str(datetime.datetime.now().ctime()) + ": " +str(msg.payload.decode("utf-8")))
    print("--------------------------------")
    

# Se crea socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Se conecta al puerto donde el servidor se encuentra a la escucha
server_address = (SERVER_IP, SERVER_PORT)
print('Conectando a {} en el puerto {}'.format(*server_address))
sock.connect(server_address)


print("BIENVENIDO CLIENTE " + id)


client = mqtt.Client(clean_session=True)
client.on_message = on_message


client.username_pw_set(MQTT_USER, MQTT_PASS)
client.connect(host=MQTT_HOST, port = MQTT_PORT)
client.subscribe(id)



while True:

   
    while True:
        n=0
        print("Que desea?")
        print("1. Enviar Texto")
        print("2. Enviar Audio")
        print("3. Ver Nuevos Mensajes")        
        print("4. Salir")
        menu1 = input("que desea?: ")
        if(menu1 == '1'):
            print("------MENSAJE DE TEXTO------")
            print("     1. Enviar a Usuario")
            print("     2. Enviar a Sala")
            menu2 = input("     que desea?: ")
            if(menu2 == '1'):
                print("------A USUARIO------")
                while n!=1:
                    destino = input("Ingrese Id Usuario a mandar MSM: ")
                    if(len(destino) != 9):
                        print("Usuario invalido!!! Vuelva a ingresar")
                        n=0
                    else:
                        n=1

                msm = input("escribe y manda...")
                msm = "@"+id+": "+ msm
                client.publish(destino, msm)
            if(menu2 == '2'):
                print("------A SALA------")
                while n!=1:
                    destino = input("Ingrese la sala: ")
                    if(len(destino) != 4):
                        print("Sala invalida!!! Vuelva a ingresar")
                        n=0
                    else:
                        n=1

                msm = input("escribe y manda...")
                msm = "@"+id+": "+ msm
                client.publish(destino, msm)

        if(menu1 == '2'):
            print('VOZZZZ')

            FTR = b'\x03'
            tam = b'123'
            ida = id.encode("utf-8")
            FTR = FTR + ida + tam
            #print(FTR[3])
            sock.sendall(FTR) #Se envia utilizando "socket.sendall"
  #          sock.sendall(binascii.unhexlify("01"))
            print('\n\nEnviando request al servidor')

        if(menu1 == '3'):   
            print("Nuevos Mensajes: ")
            print("---Hora/Fecha -----  Usuario----- MSM---")
            client.loop_start()
            time.sleep(1)
            client.loop_stop()

        if(menu1 == '4'):
            exit 




        break

