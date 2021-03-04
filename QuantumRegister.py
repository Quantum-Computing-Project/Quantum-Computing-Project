#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class State(object):
    
    # Initialising state vector and number of qubits
    def __init__(self, *arrays):
        
        self.vector = np.array([1])

        for array in arrays:
            self.vector = basic.kronecker_product(self.vector,array)

        self.num_qubits = len(self.vector)

    # Method to make random measurement 
    def measure(self):
        
        P = 0
        x = random.random()
        i = -1
        print("random number", x) # For testing DELETE LATER
        
        while P < x:
                
                P += (abs(self.vector[i+1]))**2      
                i += 1
                print("P,",i, "=",  P)   # For testing DELETE LATER 
                
        return i
            
def main(): # For testing DELETE LATER
 
    y = State(np.array([1/math.sqrt(2), 1/math.sqrt(2)]),np.array([1/math.sqrt(2), 1/math.sqrt(2)]))
    print ("qubits", y.num_qubits)
    print("vector", y.vector)
    
    print(State.measure(y))
       
main()
