import time
import random
import zmq
import sys
import json
import numpy
import itertools
from collections import namedtuple

import zhelpers



def multiplicar(matrizA, matrizB):
    
    matrizR = numpy.zeros((len(matrizA),len(matrizB[0])))
    
    for i in range(len(matrizA)):
        for j in range(len(matrizB[0])):
            for k in range(len(matrizB)):
                matrizR[i][j] += matrizA[i][k] * matrizB[k][j]
    #matriz = matrizR.tolist()
    return matrizR


NBR_WORKERS = 2

context = zmq.Context.instance()
worker = context.socket(zmq.REQ)
matrizR = None
# We use a string identity for ease here
zhelpers.set_id(worker)
worker.connect("tcp://localhost:5671")

total = 0

while True:
    # Tell the router we're ready for work
    if total == 0:
        worker.send(b"ready")
    else :
        matriz_json = matrizR.tolist()
        matriz_json = json.dumps(matriz_json)
        print(matrizR)
        worker.send(matriz_json.encode())

    # Get workload from router, until finished
    workload1, workload2 = worker.recv_multipart()
    workload1 = workload1.decode()
    workload2 = workload2.decode()
    workload1 = json.loads(workload1)
    workload2 = json.loads(workload2)
    #print(type(workload))
    finished = workload1 == b"END"
    
    if (type(workload2) == list):
        matrizR= multiplicar(workload1,workload2)
    
    else:
        print("Processed: %d tasks" % total)
        break
        
        
    total += 1

    
