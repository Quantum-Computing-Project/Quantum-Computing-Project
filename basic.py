"""
This module is envisioned to contain the implementation of the tensor product and all related functions.
"""

import numpy as np


# Define Kronecker product function for 2 matrices
def kronecker_product(matrix1, matrix2):
    """
    This function takes in two matrices (or vectors) and returns a Kronecker product of the two.
    :param matrix1: left operand
    :param matrix2: right operand
    :return: Kronecker product
    """
    if not isinstance(matrix1, np.ndarray) or not isinstance(matrix2, np.ndarray):
        raise TypeError('Inputed parameters are not numpy matrices!')

    else:
        if len(matrix1.shape) == 1 and len(matrix2.shape) == 1:
            (m,) = matrix1.shape
            n = 1
            (p,) = matrix2.shape
            q = 1
            # Modified algorithm
            return np.array([matrix1[i // p] * matrix2[i % p] for _ in range(n*q) for i in range(m*p)])
            # Might need to add dtype=np.complex128 to avoid losing the complex part, check later if it
            # doesn't work correctly

        elif len(matrix1.shape) == 1:
            (m,) = matrix1.shape  # matrix1 is a vector, extract the length
            n = 1  # Second dimension is just 1
            (p, q) = matrix2.shape
            # Found the algorithm online, wiki page of the kronecker product
            # It is modified to reflect the fact that we have a vector here
            return np.array([[matrix1[i // p] * matrix2[i % p][j % q] for j in range(n*q)] for i in range(m*p)])

        elif len(matrix2.shape) == 1:
            (m, n) = matrix1.shape
            (p,) = matrix2.shape
            q = 1
            # Modified algorithm again
            return np.array([[matrix1[i // p][j // q] * matrix2[i % p] for j in range(n*q)] for i in range(m*p)])

        else:
            (m, n) = matrix1.shape
            (p, q) = matrix2.shape
            # Original algorithm
            return np.array([[matrix1[i // p][j // q] * matrix2[i % p][j % q] for j in range(n*q)] for i in range(m*p)])


def kronecker_product_multi(*matrices):
    """
    Kronecker product implemented on an arbitrary number of matrices (or vectors). Make sure the matrices are
    inputed in order in which you want to have them kronecker producted. For example A * B * C would be called as
    kronecker_product_multi(A, B, C)
    :param matrices:
    :return: matrix
    """
    if len(matrices) < 2:
        raise SyntaxError('Only one matrix was given, at least two are needed.')
    else:
        result = np.array([1])
        for matrix in matrices:
            result = kronecker_product(result, matrix)
        return result

def kronecker_product_power(matrix, power):
    if power < 1:
        raise SyntaxError('Power input invalid')
    elif power == 1:
        return matrix
    else:
        i = 2
        result = kronecker_product(matrix, matrix)
        while i < power:
            result = kronecker_product(result, matrix)
            i = i + 1
        return result

# Do tests here
if __name__ == "__main__":
    a = np.array([0, 1, 2])
    b = np.array([0, 1])

    print(kronecker_product(a, b))
    print(kronecker_product_multi(a, b, b))
    print(kronecker_product_multi(a, a, a))
    print(kronecker_product_power(a,3))
