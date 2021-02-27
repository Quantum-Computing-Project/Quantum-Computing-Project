
#Quantum gates


#Most of this is going to have to be reworked later
#I doubt these will work with the Qubit class right now.
#The np.matmul function may have to be replaced but idk.
#If you want to use multiple gates simultaneously, you'll have to do it 
#manually with the help of the matrices below. We probably don't want to have 
#to do that.


import numpy as np
from basic import kronecker_product

#----------------------------------Constants-----------------------------------

I = np.array([[1,0], [0,1]])
#Identity Gate

X = np.array([[0,1], [1,0]])
#NOT Gate

Y = np.array([[0,-1j], [1j,0]])
#Y Gate

Z = np.array([[0,-1j], [1j,0]])
#Z Gate

H = (1/np.sqrt(2)) * np.array([[1,1], [1,-1]])
#Hadamard Gate

S = np.array([[1,0], [0,1j]])
#Phase Gate

CX = np.array([[1,0,0,0], [0,1,0,0], [0,0,0,1], [0,0,1,0]])
#Controlled NOT Gate

CZ = np.array([[1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,-1]])
#Controlled X Gate

#----------------------------------Functions-----------------------------------

def iGate(state):
    """
    Identity gate
    
    Parameters
    ----------
    state: array
        state of quantum bit to be operated on
    """
    
    return np.matmul(I, state)

def xGate(state):
    """
    NOT gate, single qubit operation
    
    Parameters
    ----------
    state: array
        state of quantum bit to be operated on
    """
    
    return np.matmul(X, state)  #not sure if we're allowed to use this

def yGate(state):
    """
    Y gate

    Parameters
    ----------
    state: array
        state of quantum bit to be operated on
    """
    
    return np.matmul(Y, state)
    
def zGate(state):
    """
    Z gate
    
    Parameters
    ----------
    state: array
        state of quantum bit to be operated on
    """
    
    return np.matmul(Z, state)
    
def hGate(state):
    """
    Hadamard gate
    
    Parameters
    ----------
    state: array
        state of quantum bit to be operated on
    """
    
    return np.matmul(H, state) 

def cxGate(state, control):
    """
    Controlled NOT gate
    
    Parameters
    ----------
    state: array
        state of quantum bit to be operated on
    control: array
        state of quantum bit to be used as a control
    """
    
    statevector = kronecker_product(control, state)
    return np.matmul(CX, statevector)

def czGate(state, control):
    """
    Controlled Z gate
    
    Parameters
    ----------
    state: array
        state of quantum bit to be operated on
    control: array
        state of quantum bit to be used as a control
    """
    
    statevector = kronecker_product(control, state)
    return np.matmul(CZ, statevector)