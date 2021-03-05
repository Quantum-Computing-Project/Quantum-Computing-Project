#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import random
from qsimulator.basic import kronecker_product


class State(object):

    # Initialising state vector and number of qubits
    def __init__(self, stateArray):

        self.vector = stateArray
        self.num_qubits = np.log2(len(self.vector))

    def __str__(self):
        return str(self.vector)

    def __mul__(self, other):
        newState = kronecker_product(self.vector, other.vector)
        return State(newState)

    def measure(self):

        P = 0
        x = random.random()
        i = -1

        while P < x:
            P += (abs(self.vector[i + 1])) ** 2
            i += 1

        return i


if __name__ == "__main__":
    q1 = State(np.array([1/np.sqrt(2), 1/np.sqrt(2)]))
    q2 = State(np.array([1/np.sqrt(2), 1/np.sqrt(2)]))
    y = q1 * q2
    print("qubits", y.num_qubits)
    print("vector", y.vector)

    print(State.measure(y))
