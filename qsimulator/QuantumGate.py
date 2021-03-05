"""
This module contains the quantum gates
"""

# Quantum gates
# 0.3


# Some of this may have to be reworked later
# The np.matmul function may have to be replaced but idk.
# The CX and CZ gates may be slightly restrictive and/or fiddly. You probably
# won't have a nice time using them.


import numpy as np
from qsimulator.basic import kronecker_product, kronecker_product_power
from qsimulator.QuantumRegister import State
from qsimulator.qubit import Qubit

# ----------------------------------Constants-----------------------------------

I = np.array([[1, 0],
              [0, 1]])
# Identity Gate

X = np.array([[0, 1],
              [1, 0]])
# NOT Gate

Y = np.array([[0, -1j],
              [1j, 0]])
# Y Gate

Z = np.array([[0, -1j],
              [1j, 0]])
# Z Gate

H = (1 / np.sqrt(2)) * np.array([[1, 1],
                                 [1, -1]])
# Hadamard Gate

S = np.array([[1, 0],
              [0, 1j]])
# Phase Gate

CX = np.array([[1, 0, 0, 0],
               [0, 1, 0, 0],
               [0, 0, 0, 1],
               [0, 0, 1, 0]])
# Controlled NOT Gate

CZ = np.array([[1, 0, 0, 0],
               [0, 1, 0, 0],
               [0, 0, 1, 0],
               [0, 0, 0, -1]])
# Controlled X Gate

SWAP = np.array([[1, 0, 0, 0],
                 [0, 0, 1, 0],
                 [0, 1, 0, 0],
                 [0, 0, 0, 1]])
# SWAP Gate

CCX = np.array([[1, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 1, 0]])


# Toffoli Gate

# ---------------------------------Base Class-----------------------------------

class QuantumGate(object):
    """
    Base quantum gate class
    
    Parameters
    ----------
    matrix: array
        matrix representing quantum gate
    """

    def __init__(self, matrix):
        if isinstance(matrix, np.ndarray):
            self.matrix = matrix
            self.shape = matrix.shape
        else:
            raise Exception("Input is not a numpy array.")

    def __mul__(self, x):
        """
        Tensor product for quantum gates. It is called using the * operator
        
        Parameters
        ----------
        x: QuantumGate
            Other quantum gate to perform kronecker product with
        """
        if isinstance(x, QuantumGate):
            newGate = kronecker_product(self.matrix, x.matrix)
            return QuantumGate(newGate)
        elif isinstance(x, (int, float, np.complex128)):
            return QuantumGate(self.matrix * x)

    def __rmul__(self, other):
        if isinstance(other, QuantumGate):
            newGate = kronecker_product(self.matrix, other.matrix)
            return QuantumGate(newGate)
        elif isinstance(other, (int, float, np.complex128)):
            return QuantumGate(self.matrix * other)

    def __pow__(self, power, modulo=None):
        return QuantumGate(kronecker_product_power(self.matrix, power))

    def __str__(self):
        return str(self.matrix)

    def __add__(self, other):
        if self.shape == other.shape:
            newMatrix = self.matrix + other.matrix
            return QuantumGate(newMatrix)
        else:
            raise Exception("Two matrices are not of the same shape.")

    def __sub__(self, other):
        if self.shape == other.shape:
            newMatrix = self.matrix - other.matrix
            return QuantumGate(newMatrix)
        else:
            raise Exception("Two matrices are not of the same shape.")

    # TODO: implement __truediv__

    def __call__(self, statevector):
        """
        Applies gate to qubit(s)
        
        Parameters
        ----------
        statevector: array, State, Qubit
            State of quantum bit or register
        """

        # Is the gate acting on the qubit class?
        if isinstance(statevector, Qubit):
            output = np.matmul(self.matrix, statevector.vector)
            return State(output)
        # Is the gate acting on the quantum register?
        elif isinstance(statevector, State):
            output = np.matmul(self.matrix, statevector.vector)
            return State(output)
        elif isinstance(statevector, QuantumGate):
            output = np.matmul(self.matrix, statevector.matrix)
            return QuantumGate(output)
        else:
            raise Exception("What the hell are you trying to multiply?")




# ------------------------------Gate Construction-------------------------------

def iGate(d):
    """
    Creates an Identity gate object when called.
    Parameters
    ----------
    d -> number of qubits

    Returns
    -------
    QuantumGate
        An Identity gate
    """

    return QuantumGate(np.identity(2**d))


def xGate():
    """
    Creates a NOT gate object when called.
    
    Returns
    -------
    QuantumGate
        An X gate
    """

    return QuantumGate(X)


def yGate():
    """
    Creates a Y gate object when called.
    
    Returns
    -------
    QuantumGate
        A Y gate
    """

    return QuantumGate(Y)


def zGate():
    """
    Creates a Z gate object when called.
    
    Returns
    -------
    QuantumGate
        A Z gate
    """

    return QuantumGate(Z)


def hGate():
    """
    Creates a Hadamard gate object when called.
    
    Returns
    -------
    QuantumGate
        A Hadamard gate
    """

    return QuantumGate(H)


def sGate():
    """
    Returns a Phase gate object when called.

    Returns
    -------
    QuantumGate
        A Phase gate

    """
    return QuantumGate(S)


# Still trying to figure out how these ones should work with the new implementation
# ||                                                                          ||
# \/                                                                          \/

# If you want to call these ones, you'll want to make sure that you have a
# statevector containing both of the qubits you're using
# (or all three in the case of the Toffoli Gate)
# Also, make sure they're in the right order

def swapGate():
    """
    Creates a SWAP gate object when called.

    Returns
    -------
    QuantumGate
        A SWAP gate

    """
    return QuantumGate(SWAP)


def cxGate():
    """
    Creates a Controlled NOT gate object when called.
    
    Returns
    -------
    QuantumGate
        A CNOT gate
    """

    return QuantumGate(CX)


def czGate():
    """
    Creates a Controlled Z gate object when called.
    
    Returns
    -------
    QuantumGate
        A CZ gate
    """

    return QuantumGate(CZ)


def toffGate():
    """
    Creates a Toffoli Gate object when called.
    
    Returns
    -------
    QuantumGate
        A Toffoli Gate
    """

    return QuantumGate(CCX)


if __name__ == "__main__":
    gate1 = QuantumGate(np.array([[0,1],[2,3]]))
    gate2 = QuantumGate(np.array([[0,1],[2,3]]))

    print(gate1**2)
