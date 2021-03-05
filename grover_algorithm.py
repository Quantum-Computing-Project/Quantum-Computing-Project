import qsimulator as qs
import numpy as np
import random


# Grover's algorithm (search)
# Given a boolean function f, Grover's algorithm finds an x such that
# f(x) = 1.
# If there are N values of x, and M possible solutions, it requires
# O(sqrt(N/M)) time.

def grover_algorithm():
    q1 = qs.State(np.array([1 / np.sqrt(2), 1 / np.sqrt(2)]))
    state = q1 * q1 * q1

    # Let's create an oracle with the desired state being |101>
    I = np.identity(2 ** 3)
    I[2][2] = -1
    oracle = qs.QuantumGate(I)
    reflection = qs.QuantumGate(2 * np.ones((8, 8))/8 - np.identity(8))
    grover = oracle(reflection)

    for i in range(50):
        state = grover(state)
        print(state)

    print(state.measure())


if __name__ == "__main__":
    grover_algorithm()
