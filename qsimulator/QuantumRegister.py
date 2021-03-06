#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module contains the State class that is used to represent a state of a quantum system.
"""

import numpy as np
import random
import qsimulator as qs
from qsimulator.basic import kronecker_product, kronecker_product_power


class State(object):

    def __init__(self, stateArray):
        """
        Base class that represents the state of a quantum system. Input to the __init__ constructor is a numpy
        array that represents the coefficients of the corresponding basis state.

        Example: inputting [1, 0, 0, 0] means the state looks like "1*|0> + 0*|1> + 0*|2> + 0*|3>".

        Whether the length of the array is an exponent of 2 is not checked, giving a lot of freedom to the user,
        keep in mind that the QuantumGates probably won't work. (The actual implementation of a quantum computer
        will only work with 2**n states, where n is the number of qubits. This whole system is designed
        in the same way.)

        Parameters
        ----------
        stateArray -> np.ndarray, represents the coefficients
        """
        self.vector = stateArray
        self.num_qubits = int(np.log2(len(self.vector)))

    def __str__(self):
        """
        Defines the behaviour when print(State) is invoked.
        """
        return str(self.vector)

    def __mul__(self, other):
        """
        Defines the behaviour when * operator is invoked.

        If the second operand is another instance of State object, kronecker_product is invoked.
        If the second operand is (int, float, np.complex128) instance, regular element-wise multiplication
        is invoked.

        Parameters
        ----------
        other -> either State instance, or (int, float, np.complex128)

        Returns
        -------
        State object instance.
        """
        if isinstance(other, State):
            newState = kronecker_product(self.vector, other.vector)
            return State(newState)
        elif isinstance(other, (int, float, np.complex128)):
            return State(self.vector * other)
        else:
            raise Exception("Unsupported type of object.")

    def __rmul__(self, other):
        """
        This is invoked when the State instance is the right operand of the * operator.
        See State.__mul__ for implementation.
        """
        if isinstance(other, State):
            newState = kronecker_product(other.vector, self.vector)
            return State(newState)
        elif isinstance(other, (int, float, np.complex128)):
            return State(self.vector * other)
        else:
            raise Exception("Unsupported type of object.")

    def __pow__(self, power, modulo=None):
        """
        This method is invoked when the State is raised to a certain exponent.
        The State is kronecker-producted with itself "power" number of times.
        Parameters
        ----------
        power -> integer
        modulo

        Returns
        -------
        State object instance.
        """
        return State(kronecker_product_power(self.vector, power))

    def __truediv__(self, other):
        """
        Defines the behaviour when the / operator is invoked. Only supports dividing by integers, floats,
        or np.complex128 number type.
        Returns the State object with division implemented element-wise.
        """
        if isinstance(other, (float, int, np.complex128)):
            return State(self.vector / other)
        else:
            raise Exception("Unsupported type of object.")

    def measure(self):
        """
        Measures the State and returns a number corresponding to what was measure. It doesn't collapse the state
        and further operations are possible but this shouldn't happen in Quantum Computers.

        Returns
        -------
        int
        """
        P = 0
        x = random.random()
        i = -1

        while P < x:
            P += (abs(self.vector[i + 1])) ** 2
            i += 1

        return i

    def collapse_qubits(self, numQubits):
        """
        Measure the state for a given number of qubits. Measures the "rightmost" qubits. For example, if the register
        consists of 5 qubits and the parameter numQubits is assigned the number 3, 3 rightmost qubits are measured
        and the state of the remaining 2 qubit system is returned as a State object.

        Parameters
        ----------
        numQubits -> int

        Returns
        -------
        State object
        """
        if numQubits > self.num_qubits:
            raise Exception("Can't measure more qubits than there are qubits in the register.")
        else:
            P = 0
            x = random.random()
            i = -1

            while P < x:
                P += (abs(self.vector[i + 1])) ** 2
                i += 1

            ibin = str(qs.decimal_to_binary(i))  # binary representation of i

            #  Manually add 0s to the left of the binary representation
            if len(ibin) != self.num_qubits:
                ibin = '0' * (self.num_qubits - len(ibin)) + ibin

            measuredQubits = ibin[len(ibin)-numQubits:]
            newState = []

            for j in range(len(self.vector)):  # Find states which correspond to the measured state
                binj = str(qs.decimal_to_binary(j))

                if len(binj) != self.num_qubits:  # Manual addition of 0s again
                    binj = '0' * (self.num_qubits - len(binj)) + binj

                if binj[len(binj)-numQubits:] == measuredQubits:  # Save the new states
                    newState.append(self.vector[j])

            normalized = newState / np.linalg.norm(newState)
            return State(normalized)


def ones(numQubits):
    """
    This function initializes a quantum system in which every qubit is in the state |1>.

    Parameters
    ----------
    numQubits -> integer

    Returns
    -------
    State object
    """
    stateVector = np.zeros(2 ** numQubits)
    stateVector[-1] = 1
    return State(stateVector)


def zeros(numQubits):
    """
    This function initializes a quantum system in which every qubit is in the state |0>.

    Parameters
    ----------
    numQubits -> integer

    Returns
    -------
    State object
    """
    stateVector = np.zeros(2 ** numQubits)
    stateVector[0] = 1
    return State(stateVector)


def equiprobable(numQubits):
    """
    This function initializes a Quantum system in which every state is equally probable.

    Parameters
    ----------
    numQubits -> integer

    Returns
    -------
    State object
    """

    # The same can be done using Hadamard gates, I see no reason in doing so because this is a simulation
    # after all.
    qubit = State(np.array([1 / np.sqrt(2), 1 / np.sqrt(2)]))
    return qubit ** numQubits


if __name__ == "__main__":
    q1 = State(np.array([1, 0, 1, 1, 0, 0, 0, 0]) / np.sqrt(3))
    state = q1.collapse_qubits(2)
    print(state)
