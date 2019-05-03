import time
import random
import json
import numpy
import zmq

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

# We use a string identity for ease here
zhelpers.set_id(worker)
worker.connect("tcp://localhost:5671")
matrizR = []
total = 0

while True:
    # Tell the router we're ready for work
    worker.send(b"ready")

    # Get workload from router, until finished
    workload = worker.recv()
    workload = workload.decode()
    workload = json.loads(workload)
    #print(type(workload))
    finished = workload == b"END"
    
    if (type(workload) == list):
        matrizR= multiplicar(workload,workload)
    
    else:
        print("Processed: %d tasks" % total)
        print(matrizR)
        break
    total += 1

    
