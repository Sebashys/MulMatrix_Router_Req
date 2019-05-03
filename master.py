import time
import random
import zmq
import zhelpers
import json
import numpy

def leermatrizcompleta(nombre):
    matrizR = []
    with open(nombre,'r') as file:
        
        for linea in file.readlines():
            a = json.loads(linea)
            matrizR.append(a)
    return matrizR

def leermatrizrangos(nombre,rangoA,rangoB):
    matrizR = []
    with open(nombre,'r') as file:
        texto = itertools.islice(file, rangoA, rangoB)
        for linea in texto:
            a = json.loads(linea)
            matrizR.append(a)
    return matrizR



NBR_WORKERS = 2
matriz_prueba = leermatrizcompleta("matrizA5X5.txt")



context = zmq.Context.instance()
client = context.socket(zmq.ROUTER)
client.bind("tcp://*:5671")

for _ in range(NBR_WORKERS*3):
    
    mensaje_json = json.dumps(matriz_prueba)
    print(mensaje_json)
    address, empty, ready = client.recv_multipart()

    client.send_multipart([
        address,
        b'',
        mensaje_json.encode(),
    ])

# Now ask mama to shut down and report their results
for _ in range(NBR_WORKERS):
    mensaje_json = json.dumps("END")
    address, empty, ready = client.recv_multipart()

    client.send_multipart([
        address,
        b'',
        mensaje_json.encode(),
    ])    
