import paho.mqtt.client as mqtt
import logging
import time
import os 
from broker import * #Informacion de la conexion




#Callback que se ejecuta cuando llega un mensaje al topic suscrito
def on_message(client, userdata, msg):
    #Se muestra en pantalla informacion que ha llegado
    print("Ha llegado el mensaje al topic: " + str(msg.topic))
    print("El contenido del mensaje es: " + str(msg.payload))
    
    #Y se almacena en el log 
 #   logCommand = 'echo "(' + str(msg.topic) + ') -> ' + str(msg.payload) + '" >> ' + LOG_FILENAME
  #  os.system(logCommand)



client = mqtt.Client(clean_session=True) #Nueva instancia de cliente
client.on_message = on_message #Se configura la funcion "Handler" que se activa al llegar un mensaje a un topic subscrito
client.username_pw_set(MQTT_USER, MQTT_PASS) #Credenciales requeridas por el broker
client.connect(host=MQTT_HOST, port = MQTT_PORT) #Conectar al servidor remoto
client.subscribe("prueba")
client.loop_forever()

