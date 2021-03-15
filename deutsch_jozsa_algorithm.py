import qsimulator as qs
import numpy as np
import random
import time

"""
Given is a Boolean function that is either constant or balanced (i.e., 0 for half of inputs, 1 for the other half).
We make use of interference to determine whether the function is constant or balanced in a single function evaluation.

When doing the observation we are not interested in the rightmost qubit, that one is removed out of the equation.
If the function is constant we should observe the state |0> (|00...000>). If the function is balanced it will yield
any other state.
"""

# Defining function to test
def construct_problem_func(numQubits, problem_type='constant'):
    numInputs = 2 ** numQubits
    answers = np.zeros(numInputs)

    if problem_type == 'constant':
        answers[:] = int(np.random.random() < 0.5)
    else:  # function is balanced
        indices = np.random.choice(numInputs, size=numInputs // 2, replace=False)
        answers[indices] = 1

    def f(x):
        return answers[x]

    return f


def deutsch_josza_algorithm(func, d):
    """
    Implementation of the deutsch-josza algorithm.
    Parameters
    ----------
    func -> function object that is the function we are interested in
    d -> number of qubits to do the simulation with, function is automatically adjusted to accomodate for the
        number of qubits

    Returns
    -------
    integer, state that gets measured
    """

    q1 = qs.State(np.array([1, 1]) / np.sqrt(2))
    q2 = qs.State(np.array([1, -1]) / np.sqrt(2))

    # Equivalent to Hadamard gate applied to d bits in state |0> and final bit in state |1>
    initState = q1**d * q2

    H = qs.hGate()
    I = qs.iGate(1)

    # Create the required oracle
    numStates = 2**(d+1)
    operatorMatrix = np.zeros((numStates, numStates))
    for i in range(numStates):
        for j in range(numStates):
            rightBit = j % 2
            rest = j // 2
            if 2 * rest + (func(rest) + rightBit) % 2 == i:  # 2 * rest still needed, write down if unclear
                operatorMatrix[i][j] = 1
                
    # Creating QuantumGate object
    oracle = qs.QuantumGate(operatorMatrix)
    
    # Applying Hadamard gate to |0> state qubits
    finalState = (H**d * I)(oracle(initState))
    measurements = finalState.measure() // 2  # to remove the rightmost bit
    return measurements


if __name__ == "__main__":
    d = 4
    problemType = random.choice(['constant', 'balanced'])

    f = construct_problem_func(d, problemType)
    time1 = time.time()
    measurement = deutsch_josza_algorithm(f, d)
    time2 = time.time()

    print('Problem type: {}'.format(problemType))
    print('Measurement: {}'.format(measurement))
    print('Time taken is {}s'.format(time2 - time1))
