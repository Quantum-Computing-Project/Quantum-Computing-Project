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
        raise Exception('Inputed parameters are not numpy matrices!')

    else:
        if len(matrix1.shape) == 1 and len(matrix2.shape) == 1:
            (m,) = matrix1.shape
            n = 1
            (p,) = matrix2.shape
            q = 1
            # Modified algorithm
            return np.array([matrix1[i // p] * matrix2[i % p] for j in range(n*q) for i in range(m*p)])

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


# Do tests here
if __name__ == "__main__":
    a = np.array([0, 1])
    b = np.array([0, 1])

    print(kronecker_product(a, b))

def kronecker_product_multi(matrices):
    matrix_num = len(matrices)
    if matrix_num < 2:
        print("Not enough arguments")

    elif matrix_num == 2:
        return kronecker_product(matrices)

    else:
        hd = matrices[:matrix_num - 2] #head of tuple
        tl = matrices[matrix_num - 2:] #tail of tuple to be replaced with their kronecker product
        print(tl)
        return kronecker_product_multi(hd + (kronecker_product(tl[0],tl[1]),)) #fix error: kronecker_product() missing 1 required positional argument: 'matrix2'

#test
kronecker_product_multi((a,b,a))
