
import paho.mqtt.client as mqtt
import logging
import time
import os 
from broker import * #Informacion de la conexion

#topic = "prueba"
id = "201701026"
destino = "201700000"
mensaje = ''

def on_message(client, userdata, msg):
    #Se muestra en pantalla informacion que ha llegado
    global mensaje
    mensaje = str(msg.payload.decode("utf-8"))
    print("NUEVO:")
    print(str(msg.payload.decode("utf-8")))
    print("--------------------------------")
    


client = mqtt.Client(clean_session=True)
client.on_message = on_message


client.username_pw_set(MQTT_USER, MQTT_PASS)
client.connect(host=MQTT_HOST, port = MQTT_PORT)
client.subscribe(id)
#client.loop_forever()

while True:

   
    while True:
        
        msm = input("escribe y manda...")
        msm = "@"+id+": "+ msm
        client.publish(destino, msm)

        client.loop_start()
        time.sleep(1)
        client.loop_stop()

        break

