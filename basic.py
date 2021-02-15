"""
This module is envisioned to contain the implementation of the tensor product and all related functions.
"""

import numpy as np


# Define Kronecker product function for 2 matrices
def kronecker_product(matrix1, matrix2):
    if not isinstance(matrix1, np.ndarray) or not isinstance(matrix2, np.ndarray):
        raise Exception('Inputed parameters are not numpy matrices!')

    else:
        if len(matrix1.shape) == 1:
            (m,) = matrix1.shape  # matrix1 is a vector, extract the length
            n = 1  # Second dimension is just 1
            (p, q) = matrix2.shape
            # Found the algorithm online, wiki page of the kronecker product
            # It is modified to reflect the fact that we have a vector here
            return [[matrix1[i // p] * matrix2[i % p][j % q] for j in range(n*q)] for i in range(m*p)]

        elif len(matrix2.shape) == 1:
            (m, n) = matrix1.shape
            (p,) = matrix2.shape
            q = 1
            # Modified algorithm again
            return [[matrix1[i // p][j // q] * matrix2[i % p] for j in range(n*q)] for i in range(m*p)]

        else:
            (m, n) = matrix1.shape
            (p, q) = matrix2.shape
            # Original algorithm
            return [[matrix1[i // p][j // q] * matrix2[i % p][j % q] for j in range(n*q)] for i in range(m*p)]


# Do tests here
if __name__ == "__main__":
    a = np.array([[0, 1], [2, 3], [4, 5]])
    b = np.array([[0, 1], [2, 3]])

    print(kronecker_product(a, b))
