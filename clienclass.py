#Jose Fernando Marticorena Barrientos 201701026
#Jonathan Mardoqueo Lorenzo Lopez 201709532
#Jose Carlos Sagastume Ovalle 201742012

import paho.mqtt.client as mqtt #JFMB para definirse como cliente
import logging                  #FRMB para la depuracion
import time                     #JCSO para manejar tiempos      
import os                       #JFMB para manejar funcionalidades del sistema operativo  
import logging                  #JMLL para dar informacion
import datetime                 #JMLL Para generar fecha/hora actual
import binascii                 #JCSO para manejar numeros binarios
import threading                #JCSO Concurrencia con hilos
from socket import socket       #JMLL para utilizar sockets 
from broker import *            #JMLL Informacion de la conexion





class menu():                   #JCSO Clase para el menu
    def __init__(self, id):      #JCSO constructor de la clase
        self.id = id              #JCSO variables globales
        self.destino = ''
        self.mensaje = ''
        self.n = 0 

    def ejec(self):                                     

        client = mqtt.Client(clean_session=True)        #JCSO Nueva instancia de cliente
        client.on_message = self.on_message             


        client.username_pw_set(MQTT_USER, MQTT_PASS)      #JCSO Credenciales requeridas por el broker
        client.connect(host = MQTT_HOST, port = MQTT_PORT) #JCSO Conectar al servidor remoto
        client.subscribe(self.id)                           #JCSO Subscripcion a carnet de usuario, sin embargo no se usa
        #JCSO subcripcion a Usuario y Audios
        def subs():                                     #JCSO Funcion para subcrcibir a todos los topicos
            g = open("usuario","r")                     #JCSO Se abre el archivo en donde esta el usuario
            while(True):
                linea = g.readline()
                linea = linea[:9]                        #JCSO guardamos en linea el carne o ID
                if not linea:
                    break    
                print("----------------------------- ")
                print("BIENVENIDO CLIENTE " + linea)      #JCSO Al menu le damos la bienvenida al ID
                self.id = linea                             #JCSO guardamos el id para usarlo luego
                client.subscribe('usuarios/22/'+linea)        #JCSO Subscribimos a usarios y audios
                client.subscribe('audio/22/'+linea)
            g.close()        
            #JCSO Subscripciones a salas 
            f = open("salas","r")                               #JCSO el mismo procedimeinto para salas de conver.
            while(True):
                linea = f.readline()
                linea = linea[:5]
                if not linea:
                    break    
                client.subscribe('salas/'+linea[:2]+'/'+linea[2:])
                client.subscribe('audio/'+linea[:2]+'/'+linea[2:])
            f.close()

        subs()                                      #JCSO llamamos a la funcion subscribir

        def enviar(destino):                        #JMLL funcion a llamar para enviar audios
            f=open("enviado.wav", "rb")             #JMLL abrimos el archivo como f
            fileContent = f.read()                  #JMLL luego almacenamos en filecontent
            f.close()                               #JMLL cerramos el archivo
            byteArray = bytearray(fileContent)      #JMLL ingresamos el contenido en bytearray
            client.publish(destino, byteArray)      #JMLL lo publicamos con el destino dado
            print("----Audios Enviado-----")        #JMLL se imprime para indicar que el audio fue enviado exitosamente

        def grabar(dur):                        #JMLL funcion a llamar para grabar audios
            logging.basicConfig(                #JMLL se utiliza logging para mostrar el mensaje
                level = logging.DEBUG, 
                format = '%(message)s'
                )

            logging.info('****COMIENZA LA GRABACION****')                   #JMLL se indica que comienza la grabacion
            os.system('arecord -d '+str(dur)+ ' -f U8 -r 8000 enviado.wav') #JMLL se graba el audio con la duracion variable

            logging.info('------Grabacion finalizada, inicia reproduccion') #JMLL se indica que la grbacion finalizo
            os.system('aplay enviado.wav')                                  #JMLL se reproduce el audio que se 
                                                                            #JMLL acaba de grabar


        while True:                                                  
            #JMLL client.publish('hola', "alive")
            #JMLL client.connect(host = MQTT_HOST, port = MQTT_PORT)
            while True:
                self.n=0
                print("---------------------------- ")          #JFMB comenzamos lanzado un menu con las opciones
                print("Que desea?")
                print("1. Enviar Texto")
                print("2. Enviar Audio")
                print("3. Ver Nuevos Mensajes") 
                print("4. Reconectar(recomend.cada 5 min.)")        
                print("5. Salir")
                menu1 = input("que desea?: ")                   #JFMB ingresamos en menu1 la eleccion del usuario


                if(menu1 == '1'):                               #JFMB Op.1 enviar texto a Usuario o Sala
                    print("------MENSAJE DE TEXTO------")
                    print("     1. Enviar a Usuario")
                    print("     2. Enviar a Sala")
                    menu2 = input("     que desea?: ")
                    
                    if(menu2 == '1'):                           #JFMB Si es usuario...
                        print("------A USUARIO------")
                        while self.n != 1:                      #JFMB Pedimos que ingrese un usuario hasta que cumpla con el tamaño de un carne
                            self.destino = input("Ingrese Id Usuario a mandar MSM: usuarios/22/:")
                            if(len(self.destino) != 9):
                                print("Usuario invalido!!! Vuelva a ingresar")      #si no cumple con el tamaño no es valido
                                self.n =0
                            else:
                                self.n =1
                        self.destino = 'usuarios/22/' + self.destino    #JFMB agregamos el topic completo al usr ingresado 
                        msm = input("escribe y manda...")
                        msm = "@"+self.id+": "+ msm                   #JFMB se le agrega sel ID al msm para que el receptor sepa quien lo envia
                        client.publish(self.destino, msm)       #JFMB publicamos la info al destino
                        print("-------Enviado--------- ")

                    if(menu2 == '2'):                       #JFMB lo mismo en sala...
                        print("------A SALA------")
                        while self.n !=1:
                            self.destino = input("Ingrese la sala: salas/22/S:") #JFMB el usr debe ingresar el No. de sala
                            if(len(self.destino) != 2):
                                print("Sala invalida!!! Vuelva a ingresar")
                                self.n =0
                            else:
                                self.n =1
                        self.destino = 'salas/22/S' + self.destino
                        msm = input("escribe y manda...")
                        msm = "@"+self.id+": "+ msm
                        client.publish(self.destino, msm)
                        print("-------Enviado--------- ")

                if(menu1 == '2'):                       #JFMB Mensaje de voz 
                    print("------MENSAJE DE VOZ------")
                    print("     1. Enviar a Usuario")
                    print("     2. Enviar a Sala")
                    menu2 = input("     que desea?: ")
                    if(menu2 == '1'):                       #JFMB a usr lo mismo se engresa el destinatario
                        print("------A USUARIO------")
                        while self.n != 1:
                            self.destino = input("Ingrese Id Usuario a mandar MSM: audio/22/:")
                            if(len(self.destino) != 9):
                                print("Usuario invalido!!! Vuelva a ingresar")
                                self.n =0
                            else:
                                self.n =1
                        self.destino = 'audio/22/' + self.destino      #JFMB topic entero
                        duracion = input('------Ingrese la duracion del audio(Seg.): ')     #JFMB pedimos el tiempo de grabacion
                        grabar(duracion)            #JFMB llamamos funcion grabar con el valor de duracion
                        enviar(self.destino)        #JFMB Luego de grabar enviamos el audio
                        #JFMB client.publish(self.destino, "@" + self.id)


                    if(menu2 == '2'):                   #JFMB lo mismo para las salas...
                        print("------A SALA------")
                        while self.n !=1:
                            self.destino = input("Ingrese la sala: audio/22/S:")
                            if(len(self.destino) != 2):
                                print("Sala invalida!!! Vuelva a ingresar")
                                self.n =0
                            else:
                                self.n =1
                        self.destino = 'audio/22/S' + self.destino
                        duracion = input('------Ingrese la duracion del audio(Seg.): ')
                        grabar(duracion)
                        enviar(self.destino)


                if(menu1 == '3'):               #JFMB LEER mensajes
                    print("Nuevos Mensajes: ")
                    print("-----Hora/Fecha --------  Usuario----- MSM---")  #JFMB Si son de texto nos indica hora/usuario que mando/ msm
                    for i in range(0,1):                        #JFMB ciclio para que revise bien si hay mensajes
                        client.on_message = self.on_message     # JFMB onmessage para que llame a la funcion si hay mensajes
                        client.loop_start()                     #JFMBel loop que inicia la busqueda de mensajes
                        time.sleep(2)
                        client.loop_stop()                        
                    print("*****SI NO HAY MENSAJES SE RECOMIENDA:")
                    print("***** 5. RECONECTAR  O LOS MENSAJES ESTAN POR LLEGAR")                    #JFMB Si no hay mensajes se recomienda reconectr

                if (menu1 == '4' ):                 #JFMB OP 4 recconectar 
                    self.ejec()                     #JFMB basicamente vuelve a llamar a la funcion principal
                    print('RECONECTANDO...')        #JFMB porque la conexion es muy corta y ya no se resiven msm despes de mucho tiempo

                if(menu1 == '5'):               #JFMB Op 5 salir del programa
                    print('ADIOS...')
                    exit()                  #JFMB  exit para salir




                break

    def on_message(self, client, userdata, msg):                #JCSO funcion que si llegan mensajes los extrae de sus respectivos topic
        #JCSO Se muestra en pantalla informacion que ha llegado
        tipo = str(msg.topic)                                   #JCSO Se ve de que topic viene el mensaje
        tipo = tipo[:5]
        if(tipo == 'audio'):                                        #JCSOsverificai el topic es de audios 
            print("-------------" + tipo +  "-------------------")
            print("Reprodcir audio")            
            f = open('recibido.wav', 'wb')                          #JCSO aca es donde se guarda el audioque fue recibido
            f.write(msg.payload)
            f.close()
            os.system('aplay recibido.wav')                         #JCSO y lo reproducimos despues de recibirlo
            print("----------------------------------------------")   
        else:                                                           #JCSO en el caso contrario que sea audio, entonces es un texto
                                                                
            print("-------------" + tipo +  "-------------------")    #JCSO Mostramos el mensaje y la hora en que fue recibido
            print(str(datetime.datetime.now().ctime()) + ": " +str(msg.payload.decode("utf-8")))
            print("----------------------------------------------")  
            
        
deunavariable = menu('user')           #JCSO llamamos a la clase 

deunavariable.ejec()                    #JCSO y ejecutamos la clase


