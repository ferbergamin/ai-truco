# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

def sigmoid(soma):
    return 1 / (1 + np.exp(-soma))

def sigmoidDerivada(sig):
    return sig * (1 - sig)

archive = open('memory.csv', 'r')
csv_file = pd.read_csv(archive, delimiter=',')

# entradas = np.array([[0,0.3,0.2,1],
#                      [0,0,0.2,1],
#                      [0,0.2,0.2,1],
#                      [0,0.3,0,1],
#                      [0,0,0.2,1],
#                      [-1,0.3,0,2],
#                      [1,0,0.2,2],
#                      [1,0.1,0.2,2],
#                      [-1,0.2,0,2],
#                      [1,0.1,0.3,2],
#                      [-1,0,0,3],
#                      [1,0,0.1,3],
#                      [1,0.1,0,3],
#                      [-1,0.2,0,3],
#                      [1,0,0.3,3]])

# saidas = np.array([[0.0],[1.0],[0.0],[0.0],[1.0],[0.0],[1.0],[1.0],[0.0],[1.0],[0.0],[1.0],[0.0],[0.0],[1.0]])

archive = open('memory.csv', 'r')
csv_file = pd.read_csv(archive, delimiter=',')

entradas = np.array(csv_file.iloc[:, :-1])
saidas = np.array([[float(k)] for k in csv_file['result']])

pesos0 = 2*np.random.random((4,2)) - 1
pesos1 = 2*np.random.random((2,1)) - 1

epocas = 10000
taxaAprendizagem = 0.3
momento = 1

for j in range(epocas):
    camadaEntrada = entradas
    somaSinapse0 = np.dot(camadaEntrada, pesos0)
    camadaOculta = sigmoid(somaSinapse0)
    
    somaSinapse1 = np.dot(camadaOculta, pesos1)
    camadaSaida = sigmoid(somaSinapse1)
    erroCamadaSaida = saidas - camadaSaida
    mediaAbsoluta = np.mean(np.abs(erroCamadaSaida))
    print("Erro: " + str(mediaAbsoluta))
    
    derivadaSaida = sigmoidDerivada(camadaSaida)
    deltaSaida = erroCamadaSaida * derivadaSaida
    
    pesos1Transposta = pesos1.T
    deltaSaidaXPeso = deltaSaida.dot(pesos1Transposta)
    deltaCamadaOculta = deltaSaidaXPeso * sigmoidDerivada(camadaOculta)
    
    camadaOcultaTransposta = camadaOculta.T
    pesosNovo1 = camadaOcultaTransposta.dot(deltaSaida)
    pesos1 = (pesos1 * momento) + (pesosNovo1 * taxaAprendizagem)
    
    camadaEntradaTransposta = camadaEntrada.T
    pesosNovo0 = camadaEntradaTransposta.dot(deltaCamadaOculta)
    pesos0 = (pesos0 * momento) + (pesosNovo0 * taxaAprendizagem)
    
print(pesos0)
print(pesos1)

    
    
    
    
    
    
    
    
[[  1.79376379, -1.76743326],
[-11.41509836,11.63501476],
[  8.51850981,-8.29926651],
[ -0.5696793,0.55177093]]
[[14.50249387],
[-13.8153545 ]]
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


