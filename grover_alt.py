import qsimulator as qs
import numpy as np
import random
import time


def construct_problem(q=10):
    numInputs = 2**q
    answers = np.zeros(numInputs)
    answers[np.random.randint(0, numInputs)] = 1

    def f(x):
        return answers[x]

    return f


def grover_algorithm(func, q):
    q1 = qs.State(np.array([1, 1]) / np.sqrt(2))
    q2 = qs.State(np.array([1, -1]) / np.sqrt(2))

    initState = q1**d * q2