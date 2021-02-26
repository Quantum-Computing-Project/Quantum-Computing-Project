import numpy as np


class SparseMatrix:
    """
    A container class for a representation of a sparse matrix. Matrix is assumed to be a numpy array type.
    I am implementing a so called CSR format of sparse matrices. Wikipedia page on sparse matrices provides
    a nice introduction to the method and provides some nice examples.

    Parameters
    ----------
    matrix: numpy complex128 two-dimensional array that represents the matrix you want to save as a sparse one.
    """

    def __init__(self, matrix):
        if not isinstance(matrix, np.ndarray):
            raise TypeError('Inputted parameter is not a numpy array!')

        else:
            self._values = []
            self._colIndex = []
            self._rowIndex = []

            (m, n) = matrix.shape  # Extract the shape of the matrix
            self._shape = (m, n)

            for i in range(m):  # loop over rows
                for j in range(n):  # collumn index
                    if matrix[i][j] != 0:
                        self._values.append(matrix[i][j])
                        self._colIndex.append(j)
                        self._rowIndex.append(i)

    def __str__(self):
        output = ''
        for i in range(len(self._values)):
            output += f'({self._rowIndex[i]}, {self._colIndex[i]}) : {self._values[i]} \n'
        return output

    @property
    def shape(self):
        return self._shape

    @property
    def values(self):
        return self._values

    @property
    def column_indices(self):
        return self._colIndex

    @property
    def row_indices(self):
        return self._rowIndex

    def unsparse(self):
        full_matrix = np.zeros(shape=self._shape, dtype=np.complex128)
        for i in range(len(self._values)):
            row = self._rowIndex[i]
            column = self._colIndex[i]
            full_matrix[row][column] += self._values[i]

        return full_matrix


def sparse_kronecker_product(matrix1, matrix2):
    """
    Implementation of the kronecker product on two sparse matrices (our custom created class).
    :param matrix1: SparseMatrix instance
    :param matrix2: SparseMatrix instance
    :return: SparseMatrix instance
    """
    if not isinstance(matrix1, SparseMatrix):
        raise TypeError('First parameter is not a sparse matrix!')
    elif not isinstance(matrix2, SparseMatrix):
        raise TypeError('Second parameter is not a sparse matrix!')
    else:
        (m, n) = matrix1.shape
        (p, q) = matrix2.shape

        result = np.zeros((p * m, q * n))

        # (i, j) \td (k, l) = (i*p + k, j*q + l)
        for a in range(len(matrix1.values)):
            for b in range(len(matrix2.values)):
                i = matrix1.row_indices[a]
                j = matrix1.column_indices[a]
                value1 = matrix1.values[a]

                k = matrix2.row_indices[b]
                l = matrix2.column_indices[b]
                value2 = matrix2.values[b]

                result[i * p + k][j * q + l] = value1 * value2
        return SparseMatrix(result)


if __name__ == '__main__':
    testMatrix = SparseMatrix(np.array([[1, 0], [0, 2]]))
    testMatrix2 = SparseMatrix(np.array([[1, 0], [0, 2]]))
    print(sparse_kronecker_product(testMatrix, testMatrix2))