import qsimulator as qs
import numpy as np
import time

"""
Deutsch's algorithm is a special case of the general Deutsch-Jozsa algorithm. 
It checks the condition f(0) = f(1).
Once all the operations are finished, a measurement is made. If the measured state is |0> the function is 
constant (f(0) = f(1)). If the measure state is |1> the function is balanced (f(0) != f(1)).

We use a "quantum implementation" (represented by a matrix in our code) of the function that maps
|x>|y> to |x>|f(x) XOR y>. Unfortunately this matrix has to be brute force computed because of the way our code works.
I don't think this is a problem as any actual implementation (real world implementation) of an oracle is most
definitely going to look nothing like the usual quantum circuit model.
"""


# Constructing random function
def construct_problem():
    answers = np.random.randint(0, 2, size=2)

    def f(x):
        return answers[x]
    return f


def deutsch_algorithm(func):
    qubit1 = qs.State(np.array([1, 1]) / np.sqrt(2))
    qubit2 = qs.State(np.array([1, -1]) / np.sqrt(2))
    
    # Equivalent to initial state |0>|1> passed through Hadamard gate
    initState = qubit1 * qubit2 

    H = qs.hGate()
    I = qs.iGate(1) 

    # Time to create an oracle that we need
    operatorMatrix = np.zeros((4, 4))
    for i in range(4):
        for j in range(4):
            leftBit = j // 2
            rightBit = j % 2
            if 2 * leftBit + (func(leftBit) + rightBit) % 2 == i:
                operatorMatrix[i][j] = 1

    oracle = qs.QuantumGate(operatorMatrix)
    
    # Applying Hadamard gate to first qubit
    finalState = (H * I)(oracle(initState))
    measurement = finalState.measure() // 2  # to get the state of the leftmost bit

    return measurement


if __name__ == "__main__":
    f = construct_problem()
    parity = f(0) == f(1)

    measurement = deutsch_algorithm(f)

    print('f(0): {}, f(1): {}'.format(f(0), f(1)))
    print('f(0) == f(1): {}'.format(parity))
    print('Measurement: {}'.format(measurement))
