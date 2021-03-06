"""
This module is envisioned to contain the implementation of the tensor product and all related functions.
"""

import numpy as np


# Define Kronecker product function for 2 matrices
def kronecker_product(matrix1: np.ndarray, matrix2: np.ndarray) -> np.ndarray:
    """
    This function takes in two matrices (or vectors) and returns a Kronecker product of the two.

    Parameters
    ----------
    matrix1 -> left operand, numpy complex128 array
    matrix2 -> right operand, numpy complex128 array

    Returns
    -------
    matrix, kronecker product of the inputted matrices, numpy complex128 array
    """
    if not isinstance(matrix1, np.ndarray) or not isinstance(matrix2, np.ndarray):
        raise TypeError('Inputted parameters are not numpy matrices!')

    else:
        if len(matrix1.shape) == 1 and len(matrix2.shape) == 1:
            (m,) = matrix1.shape  # matrix1 is a vector, extract the length
            n = 1
            (p,) = matrix2.shape  # matrix 2 is a vector, extract the length
            q = 1
            # Found the algorithm online, wiki page of the kronecker product
            # It is modified to reflect the fact that we have a vector here
            return np.array([matrix1[i // p] * matrix2[i % p] for _ in range(n * q) for i in range(m * p)],
                            dtype=np.complex128)

        elif len(matrix1.shape) == 1:
            (m,) = matrix1.shape  # matrix1 is a vector, extract the length
            n = 1  # Second dimension is just 1
            (p, q) = matrix2.shape
            # Modified algorithm
            return np.array([[matrix1[i // p] * matrix2[i % p][j % q] for j in range(n * q)] for i in range(m * p)],
                            dtype=np.complex128)

        elif len(matrix2.shape) == 1:
            (m, n) = matrix1.shape
            (p,) = matrix2.shape
            q = 1
            # Modified algorithm again
            return np.array([[matrix1[i // p][j // q] * matrix2[i % p] for j in range(n * q)] for i in range(m * p)],
                            dtype=np.complex128)

        else:
            (m, n) = matrix1.shape
            (p, q) = matrix2.shape
            # Original algorithm
            return np.array(
                [[matrix1[i // p][j // q] * matrix2[i % p][j % q] for j in range(n * q)] for i in range(m * p)],
                dtype=np.complex128)


def kronecker_product_multi(*matrices):
    """
    Kronecker product implemented on an arbitrary number of matrices (or vectors). Make sure the matrices are
    inputted in order in which you want to have them kronecker producted. For example A * B * C would be called as
    kronecker_product_multi(A, B, C)

    Parameters
    ----------
    matrices -> matrices that are to be kronecker producted, numpy complex128 arrays

    Returns
    -------
    matrix -> result of the operation, numpy complex128 array
    """
    if len(matrices) < 2:
        raise SyntaxError('Only one matrix was given, at least two are needed.')
    else:
        result = np.array([1])
        for matrix in matrices:
            result = kronecker_product(result, matrix)
        return result


def kronecker_product_power(matrix, power):
    """
    A function that does the kronecker product on a matrix with itself a given amount of times.

    Parameters
    ----------
    matrix -> matrix that is to be raised to a certain "kronecker" power
    power -> integer, specifies the "kronecker power" the matrix is to be raised to

    Returns
    -------
    matrix -> result of the operation, numpy complex128 array
    """
    if power < 1 or not isinstance(power, int):
        raise SyntaxError('Power input invalid')
    else:
        result = np.array([1])
        for i in range(power):
            result = kronecker_product(result, matrix)
        return result


# Do tests here
if __name__ == "__main__":
    a = np.array([0, 1, 2])
    b = np.array([0, 1])

    print(kronecker_product(a, b))
    print(kronecker_product_multi(a, b, b))
    print(kronecker_product_multi(a, a, a))
    print(kronecker_product_power(a, 3))
