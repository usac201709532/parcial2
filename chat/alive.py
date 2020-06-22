import threading #Concurrencia con hilos
import time      #Retardos
import logging   #Logging
import sys       #Requerido para salir (sys.exit())

#Esta función será lanzada en múltiples hilos, con distintos parámetros
def contador(rango = range(100), delay = 2):
    for i in rango:
        #print("contadpor : "+ str(i))
        time.sleep(delay) #Delay en segundos

#Configuracion inicial para logging. logging.DEBUG muestra todo.


#Lanza el primer hilo con los parámetros:
#name: Nombre "humano" para identificar fácil al hilo
#target: La función a ejecutar (o método de un objeto)
#args: argumentos, deben ser enviados como tupla
#daemon: servicio corriendo de fondo -> permite detener el hilo con "Thread._stop()"
t1 = threading.Thread(name = 'Contador 1 seg', target = contador, args = (range(100), ), daemon = True
                    )

#t2 = threading.Thread(name = 'Contador rapido',target = contador,args = ((range(250), 0.2)),daemon = True)

listaHilos = []

#for i in range(20):
#    listaHilos.append(threading.Thread(name = 'Contador ' + str(i),target = contador,args = (()),daemon = True)
 #   )

                     

#Luego de configurar cada hilo, se inicializan

t1.start()
#t2.start()

#for i in listaHilos:
 #   i.start()


#Programa principal

cnt = 0

try:
    while True:
        a = input("hola")
       #print('Contador: ' + str(cnt))
        cnt += 1
        time.sleep(3)


except KeyboardInterrupt:
    
    logging.INFO("Terminando hilos")
    
    if t1.isAlive():
        t1._stop()
    
    if t2.isAlive():
        t1._stop()

finally:
    sys.exit()
