


import paho.mqtt.client as mqtt
import logging
import time
import os 
import socket
from brock_dt import *    #Informacion de la conexion



SERV_ADDR = '167.71.243.238'     #direccion
SERV_PRT = 9822                  #puerto


class server():                   #verificaciones del servidor
    
   
    def __init__(self):           #constructor
        self.state = True
        self.listaalives = []

        client = mqtt.Client(clean_session=True) #Nueva instancia de cliente
        client.on_connect = self.on_connect #Se configura la funcion "Handler" cuando suceda la conexion
        client.on_message = self.on_message #Se configura la funcion "Handler" que se activa al llegar un mensaje a un topic subscrito
        client.username_pw_set(MQTT_USER, MQTT_PASS) #Credenciales requeridas por el broker
        client.connect(host=MQTT_HOST, port = MQTT_PORT) #Conectar al servidor remoto
        self.LOG_FILENAME = 'mqtt.log'


    
    def on_connect(self, client, userdata, flags, rc): 
        connectionText = "CONNACK recibido del broker con codigo: " + str(rc)
        logging.info(connectionText)

    #Handler en caso se publique satisfactoriamente en el broker MQTT
    def on_publish(self, client, userdata, mid): 
        publishText = "Publicacion satisfactoria"
        logging.debug(publishText)


    def agregar(self, codigo):            #agrega usuarios a la lista de ALIVES
        self.listaalives.append(codigo)

    def elimin(self, codigo):
        self.listaalive.remove(codigo)       #elimina usuarios de la lista de ALIVES

    #Callback que se ejecuta cuando llega un mensaje al topic suscrito
    def on_message(self, client, userdata, msg):
        #Se muestra en pantalla informacion que ha llegado
        logging.info("Ha llegado el mensaje al topic: " + str(msg.topic))
        logging.info("El contenido del mensaje es: " + str(msg.payload))
    
        # se almacena en el log 
        logCommand = 'echo "(' + str(msg.topic) + ') -> ' + str(msg.payload) + '" >> ' + self.LOG_FILENAME
        os.system(logCommand)

    def decoder(self, trama):                #extrae el comando de la trama
        resultado = ''
        if trama[:2] == '02': 
            resultado = self.FTR(trama[3:])
        elif trama[:2] == '03':
            resultado = self.ALIVE(trama[3:])
        elif trama[:2] == '04':
            resultado = self.FRR(trama[3:])
        elif trama[:2] == '05':
            resultado = self.ACK(trama[3:])
        elif trama[:2] == '06':
            resultado = self.OK(trama[3:])
        elif trama[:2] == '07':
            resultado = self.NO(trama[2:])
        return resultado
   
    def FTR(self, trama):                         #gestiona la solicitud de envio de archivos

        usuario = trama.split('$')[0]
        filesize = trama.split('$')[1]

        if self.state:
            self.state = False 
            if usuario in self.listaalives: 
                return '06' + usuario
            else:                                   #aqui va a leer el archivo donde se encuentra la lista de usuarios con sus respectivos grupos
                datos = open('/home/josex/Escritorio/ejecutable/usuarios.txt', 'r')
                doc = datos.read()
                datos.close()

                for variable in doc.split('\n'):               #aqui se separa el comando de la trama 
                    if usuario in  variable.split(',')[2:]:
                        if variable.split(',')[0] in self.listaalives:
                            return '06' + usuario

                return '07' + usuario    

        else:
            return '07' + usuario


    def ALIVE(self, trama):                  #corrobora que el cliente este conectado
        print('ALIVE')


    def FRR(self, trama):                     #envia la solicitud de recepcion de archivos
        print('solicitud de recepción de archivos')



    def ACK(self, id):                       #notifica de enterado al cliente que solicite una gestion
        usuario = '05' + id 
        result = usuario


       
    def OK(self, trama):                    #notifica de aceptacion a una solicitud
        print('solicitud de transferencia de archivo')




    def NO(self, trama):                     #notifica de negacion a una solicitud
        print('solicitud de transferencia de archivo')
          
objeto = server()  
                          
#objeto.agregar('201742012')   #manejo de usuarios
#objeto.agregar('201742013')                                    
#print(objeto.decoder('02$22S02$789'))        #respuesta

