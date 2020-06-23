import paho.mqtt.client as mqtt
from broker import *
import time
import os


def on_message(client, userdata, msg):
    print("Ha llegado el mensaje al topic: ")
    print(str(msg.topic)) 
    if(str(msg.topic) == 'prueba'):
        f = open('recibido.wav', 'wb')
        f.write(msg.payload)
        f.close()
        os.system('aplay recibido.wav')
    elif (str(msg.topic) == 'top2'):
        print(str(msg.payload.decode("utf-8")))



client = mqtt.Client(clean_session=True) #Nueva instancia de cliente
client.on_message = on_message #Se configura la funcion "Handler" que se activa al llegar un mensaje a un topic subscrito
client.username_pw_set(MQTT_USER, MQTT_PASS) #Credenciales requeridas por el broker
client.connect(host=MQTT_HOST, port = MQTT_PORT) #Conectar al servidor remoto
client.subscribe("prueba",0)
client.subscribe("top2",0)
client.loop_forever()