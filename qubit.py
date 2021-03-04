"""
Class to create a qubit object

"""

import numpy as np
import math
import random 
import QuantumRegister as QR

class Qubit(object):
    
    def __init__(self, alpha, beta):
        
        # Normalised coefficients
        self.norm_alpha = alpha/(math.sqrt(abs(alpha)**2 + abs(beta)**2))
        self.norm_beta = beta/(math.sqrt((abs(alpha))**2 + (abs(beta))**2))

        # Matrix form
        self.vector = np.array([self.norm_alpha, self.norm_beta])

        # Probabilities
        self.P_alpha = (abs(self.norm_alpha))**2
        self.P_beta = (abs(self.norm_beta))**2
        
    # Method to collapse the wave function and return |0> or |1>    
    def measure(self): 
        if random.random() <= self.P_alpha:
            return np.array([1, 0])
        else:
            return np.array([0,1])
        
    # Method to return quantum register from tensor product of qubits
    def qubit_product(self, other):
        return QR.state(self.vector,other.vector)
    


        

                    
        
        
