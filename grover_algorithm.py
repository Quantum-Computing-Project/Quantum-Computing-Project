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

# TODO: after implementing all the __add__, __mul__ and so on methods modify the algorithm to reflect that

def grover_algorithm(numQubits=10):
    numEntries = 2**numQubits

    q1 = qs.State(np.array([1 / np.sqrt(2), 1 / np.sqrt(2)]))
    state = q1**numQubits

    # Let's create an oracle with the desired state being |101>
    I = np.identity(numEntries)

    randInt = random.randint(0, numEntries)
    print(randInt)
    I[randInt][randInt] = -1

    oracle = qs.QuantumGate(I)
    reflection = qs.QuantumGate(2 * np.ones((numEntries, numEntries))/numEntries - np.identity(numEntries))
    grover = oracle(reflection)

    numIterations = np.floor(np.pi/4 * np.sqrt(numEntries))  # for some reason this returns a float
    for i in range(int(numIterations)):
        state = grover(state)

    print(state.measure())


if __name__ == "__main__":
    time1 = time.time()
    grover_algorithm(10)
    time2 = time.time()
    print(f"Time taken was {time2 - time1} s.")
