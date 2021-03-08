import qsimulator as qs
import numpy as np
import random
import time


# Grover's algorithm (search)
# Given a boolean function f, Grover's algorithm finds an x such that
# f(x) = 1.
# If there are N values of x, and M possible solutions, it requires
# O(sqrt(N/M)) time.
# Here, we construct a search problem with 1 solution amongst 1024
# possible answers, and find the solution with 25 applications of
# the Grover iteration operator.

def grover_algorithm(numQubits=10):
    numEntries = 2**numQubits

    # Create the initial state, every coefficient is the same
    state = qs.equiprobable(numQubits)

    I = np.identity(numEntries)
    # Random entry in the main diagonal of the matrix is -1, this represents the unknown value of x we are looking for
    randInt = random.randint(0, numEntries)
    print(f"Value of x for which the value of the function is 1 is {randInt}.")
    I[randInt][randInt] = -1

    oracle = qs.QuantumGate(I)

    # Reflection is the second gate we will need, the syntax looks confusing but its just to quickly create the
    # required matrix.
    reflection = qs.QuantumGate(2 * np.ones((numEntries, numEntries))/numEntries - np.identity(numEntries))

    # Finally this is the gate we will use, obtained matrix multiplying oracle and reflection gates
    grover = oracle(reflection)

    numIterations = np.floor(np.pi/4 * np.sqrt(numEntries))  # for some reason this returns a float
    for i in range(int(numIterations)):
        state = grover(state)

    print(f"Measured state is the state number {state.measure()}.")


if __name__ == "__main__":
    time1 = time.time()
    grover_algorithm(10)
    time2 = time.time()
    print(f"Time taken was {time2 - time1} s.")
