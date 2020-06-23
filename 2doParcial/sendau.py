import paho.mqtt.client as mqtt
from broker import *
import logging
import os
import time

topic = "prueba"
def on_public(mosq, userdata, mid):
    mosq.disconnect()

def grabar(dur):
    logging.basicConfig(
        level = logging.DEBUG, 
        format = '%(message)s'
        )

    logging.info('Comenzando grabacion')
    os.system('arecord -d '+str(dur)+ ' -f U8 -r 8000 enviado.wav')

    logging.info('Grabacion finalizada, inicia reproduccion')
    os.system('aplay enviado.wav')

grabar(5)

def on_publish(client, userdata, mid): 
    print('publicado')

client = mqtt.Client(clean_session=True)
client.on_publish = on_publish
client.username_pw_set(MQTT_USER, MQTT_PASS) #Credenciales requeridas por el broker
client.connect(host=MQTT_HOST, port = MQTT_PORT) #Conectar al servidor remoto
client.publish('top2', "este e el mensajeeeeeee")
f=open("enviado.wav", "rb")
fileContent = f.read()
f.close()
byteArray = bytearray(fileContent)
client.publish(topic, byteArray)

rc = 0 
while rc == 0:
    rc = client.loop()
    time.sleep(5)
    rc = 1
