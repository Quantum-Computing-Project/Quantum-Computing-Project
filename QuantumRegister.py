#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: nadiyahall
"""
import numpy as np
import Qubit as Q
import basic 

class State(object):
    
    def __init__(self, qubits):
        
        # If arg is Qubit object then state is just array with 1 qubit
        if isinstance(qubits, Q.Qubit):
            self.state = np.array(qubits.vector)
            
        # Else if args are two qubits then state is tensor product of the two
        elif len(qubits) == 2:
            self.state = basic.kronecker_product(qubits[0].vector, qubits[1].vector)
            
        # Else if there is a longer list of qubits then state is tensor product of them all
        # This only work when you remove the * from the kronecker_delta_multi function so you can input a list
        elif len(qubits) > 2:
            vectors = []
            for qubit in qubits :      
                vectors.append(qubit.vector)
            self.state = basic.kronecker_product_multi(vectors)
        else:
            raise TypeError('Inputted parameter is not qubit/list of qubits!')
             
x = Q.Qubit(5, 3j)
y = Q.Qubit(7j, 2)
k = Q.Qubit(8, 5)

z = State(x)
print(z.state)
