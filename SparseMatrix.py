import numpy as np


class SparseMatrix:
    """
    A container class for a representation of a sparse matrix. Matrix is assumed to be a numpy array type.
    I am implementing a so called CSR format of sparse matrices. Wikipedia page on sparse matrices provides
    a nice introduction to the method and provides some nice examples.

    Parameters
    ----------
    matrix: numpy complex128 twodimensional array that represents the matrix you want to save as a sparse one.
    """

    def __init__(self, matrix):
        if not isinstance(matrix, np.ndarray):
            raise TypeError('Inputed parameter is not a numpy array!')

        else:
            self._values = []
            self._col_index = []
            self._row_index = []

            (m, n) = matrix.shape  # Extract the shape of the matrix
            self._shape = (m, n)

            for i in range(m):  # loop over rows
                for j in range(n):  # collumn index
                    if matrix[i][j] != 0:
                        self._values.append(matrix[i][j])
                        self._col_index.append(j)
                        self._row_index.append(i)

            self._row_index.append(m)  # no plus 1 because matrix.shape counts from 1 and not from 0

    def __str__(self):
        output = ''
        for i in range(len(self._values)):
            output += f'( {self._row_index[i]}, {self._col_index[i]} ) : {self._values[i]} \n'
        return output

    def unsparse(self):
        full_matrix = np.zeros(shape=self._shape, dtype=np.complex128)
        for i in range(len(self._values)):
            row = self._row_index[i]
            collumn = self._col_index[i]
            full_matrix[row][collumn] += self._values[i]

        return full_matrix


if __name__ == '__main__':
    testMatrix = SparseMatrix(np.array([[1 + 1j, 0], [0, 2]]))
    print(testMatrix)
    print(testMatrix.unsparse())
