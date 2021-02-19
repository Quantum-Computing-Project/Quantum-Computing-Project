
import numpy as np
import math as m
import random 

class Qubit(object):
    
    def __init__(self, alpha, beta, theta, mag):

        self.alpha = alpha
        self.beta = beta
        self.theta = theta
        self.mag = mag

        
        self.norm_alpha = self.alpha/(m.sqrt(alpha**2 + beta**2))
        self.norm_beta = self.beta/(m.sqrt(alpha**2 + beta**2))

    
        self.vector = np.array([self.norm_alpha, self.norm_beta])
        self.vector = np.array([m.cos(self.theta), m.sin(self.theta)])

        self.P_alpha = abs(self.norm_alpha**2)
        self.P_beta = abs(self.norm_beta**2)
        
        

        
    

    def measure(self):

        x = random.random()
        
        if x <= self.P_alpha:
                       measurement = np.array([1, 0])
        

        else:
            measurement = np.array([0,1])

        
        return measurement
    
    


def main():

        a = float(input(print("insert alpha value:")))
        b = float(input(print("insert beta value:")))

        y = Qubit(a, b)

        measurement = Qubit.measure(y)
        print(measurement)
        
main()



        

                    
        
        
