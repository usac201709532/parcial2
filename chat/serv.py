import socket
import os 
import logging
import binascii
#JFMB importamos las librerias necesrias para conceccion entre servidor y usuario 


# Crea un socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP_ADDR = '157.245.82.242' #La IP donde desea levantarse el server
IP_ADDR_ALL = '' #En caso que se quiera escuchar en todas las interfaces de red
IP_PORT = 9816 #Puerto al que deben conectarse los clientes

BUFFER_SIZE = 16 * 1024 #Bloques de 16 KB

# Bind the socket to the port
serverAddress = (IP_ADDR_ALL, IP_PORT) #Escucha en todas las interfaces
print('Iniciando servidor en {}, puerto {}'.format(*serverAddress))
sock.bind(serverAddress) #Levanta servidor con parametros especificados

#JFMB Mantener  al servidor activo siempre

sock.listen(10)
while True:
    # JFM Esperando conexion
    print('Esperando conexion remota')
    connection, clientAddress = sock.accept()
    try:
        print('Conexion establecida desde', clientAddress)

        # Se envia informacion en bloques de BUFFER_SIZE bytes
        # y se espera respuesta de vuelta
        while True:
            #JFMB data recibe los datos mandados desde el cliente
            data = connection.recv(BUFFER_SIZE)
            #print('Recibido: {!r}'.format(data))
            #JFMB Condiciones recibidas para grabar, mandar o reproducir o desconertar
            if (data == binascii.unhexlify("01")): #Si se reciben datos (o sea, no ha finalizado la transmision del cliente)
                #connection.sendall(binascii.unhexlify("CC"))
                print('Enviando confirmacion al cliente')

                logging.basicConfig(
                    level = logging.DEBUG, 
                    format = '%(message)s'
                    )
                dur = 5
                logging.info('Comenzando grabacion')
                os.system('arecord -d ' + str(dur) + ' -f U8 -r 8000 2017.wav')

            if (data == binascii.unhexlify("02")): #Si se reciben datos (o sea, no ha finalizado la transmision del cliente)
                print('Enviando confirmacion al cliente')
  
                os.system('aplay 2017.wav')

 #               with open('201701026_server.wav', 'rb') as f: #Se abre el archivo a enviar en BINARIO
  #                  conn.sendfile(f, 0)
   #                 f.close()
    #            conn.close()                
           
            else:
                print('Transmision finalizada desde el cliente ', clientAddress)
                break
    
    except KeyboardInterrupt:
        sock.close()

    finally:
        # Se baja el servidor para dejar libre el puerto para otras aplicaciones o instancias de la aplicacion
        connection.close()