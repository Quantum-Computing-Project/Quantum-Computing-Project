#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 17:50:09 2021

@author: nadiyahall
"""
import numpy as np
import Qubit as Q
import basic 

class State(object):
    
    def __init__(self, qubits):
    
        if isinstance(qubits, Q.Qubit):
            
            self.state = np.array(qubits.vector)
    
        elif len(qubits) == 2:
            
            self.state = basic.kronecker_product(qubits[0].vector, qubits[1].vector)
            
        elif len(qubits) > 2:
            vectors = []
            for qubit in qubits :      
                vectors.append(qubit.vector)
            
            self.state = basic.kronecker_product_multi(vectors)
            # This only work when you remove the * from the kronecker_delta_
            # multi function so you can input a list
            
        else:
            raise TypeError('Inputted parameter is not qubit/list of qubits!')
             
x = Q.Qubit(5, 3j)
y = Q.Qubit(7j, 2)
k = Q.Qubit(8, 5)

z = State(x)
print(z.state)
