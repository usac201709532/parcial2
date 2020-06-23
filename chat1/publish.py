import paho.mqtt.client as paho
import logging
import time
import os 
from broker import * #Informacion de la conexion

topic = "prueba"

def on_publish(client, userdata, mid): 
    print('publicado')

client = paho.Client(clean_session=True)
client.on_publish = on_publish
client.username_pw_set(MQTT_USER, MQTT_PASS) #Credenciales requeridas por el broker
client.connect(host=MQTT_HOST, port = MQTT_PORT) #Conectar al servidor remoto
client.publish(topic, "este e el mensajeeeeeee")
