import time
import random
import zmq
import zhelpers
import json
import numpy
import math

ARCHIVO= "matrizA100X100.txt"
NBR_WORKERS = 2
MATRIZR=""

def leermatrizcompleta(nombre):
    matrizR = []
    with open(nombre,'r') as file:
        
        for linea in file.readlines():
            a = json.loads(linea)
            matrizR.append(a)
    return matrizR

def separarfilas(nombre,inicio, fin):
    #genera una matriz  nueva leyendo las lineas de la matriz inicial
    #el numero de sub_matrices depende del numero de procesos 
    matrizR = []
    with open(nombre,'r') as file:
        i = 0
        for linea in file.readlines():
            i=i+1
            if (i >= inicio) and (i <= fin):
                a = json.loads(linea)
                matrizR.append(a)
            
    return matrizR

def chunkfilas(nombre,p):
     fichero = open(nombre, 'r')
     fichero.seek(0)
     chunk= math.floor((len(fichero.readlines()) / p) / 10)
     return chunk

def numerofilas(nombre):
     fichero = open(nombre, 'r')
     fichero.seek(0)
     filas=len(fichero.readlines()) 
     return filas

def chunk_ensambler(newMatrix):
    global MATRIZR
    MATRIZR= MATRIZR + newMatrix

matriz_B = leermatrizcompleta(ARCHIVO)
chunk= chunkfilas(ARCHIVO,NBR_WORKERS)
filas = numerofilas(ARCHIVO)


context = zmq.Context.instance()
client = context.socket(zmq.ROUTER)
client.bind("tcp://*:5671")
i=0;
for _ in range(NBR_WORKERS* (math.floor(filas / chunk)) ):
    matriz_A = separarfilas(ARCHIVO,i,i+chunk)
    mensaje_json1 = json.dumps(matriz_A)
    mensaje_json2 = json.dumps(matriz_B)
    
    address, empty, ready = client.recv_multipart()
    if ready.decode() != None :
        aux= ready.decode()
        #aux= json.loads(aux)
        #print(aux)
        chunk_ensambler(aux)
    #print(ready.decode())
    client.send_multipart([
        address,
        b'',
        mensaje_json1.encode(),
        mensaje_json2.encode(),
    ])
    i=i+chunk


# Now ask mama to shut down and report their results
for _ in range(NBR_WORKERS):
    mensaje_json = json.dumps("END")
    address, empty, ready = client.recv_multipart()

    client.send_multipart([
        address,
        b'',
        mensaje_json.encode(),
        mensaje_json.encode(),
    ]) 

print(MATRIZR)   
