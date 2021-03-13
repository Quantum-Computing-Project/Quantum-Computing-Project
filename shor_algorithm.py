import qsimulator as qs
import numpy as np
import random
import time

"""
Shor's algorithm. It solves the following problem: given an integer N, find its prime factors.
On a quantum computer Shor's algorithm runs in polynomial time (the time taken is polynomial in log N, the size of 
the integer given as input.

Procedure
---------
Given a composite number N, find a non-trivial divisor of N.
We need N to be odd (otherwise 2 is a divisor) and not to be any power of a prime, check that there
are no integer roots sqrt(N, k) for 2 =< k =< log(N) base 3.

Classical part
    1. Pick a random number 1 < a < N
    2. Compute gcd(a, N). This may be done using the Euclidean algorithm
    3. If gcd(a, N) /= 1, then this number is a nontrivial factor of N, so we are done.
    4. Otherwise, use the quantum period-finding subroutine to find r, which denotes the period of the following
        function: f(x) = a^x mod N. 
    5. If r is odd, go back to step 1.
    6. If a^{r/2} = -1 (mod N) go back to step 1.
    7. Otherwise, both gcd(a^{r/2} + 1, N) and gcd(a^{r/2} - 1, N) are nontrivial factors of N.
    
Quantum subroutine
    1. Given N, find Q = 2^q such that N^2 =< Q < 2N^2. Input and output qubit register need to have q qubits.
    2. Initialize the input register to an equiprobable state and the output register to all 0s.
    3. Construct and apply 'the oracle' of the function f(x) (mentioned above).
    4. Apply the inverse quantum fourier transform to the input register (combine with the identity
        operator for the output register to create a big enough matrix).
    5. Perform the measurement.
    6. We get some outcome y in the input register.
    7. yr/Q is now close to some integer c, the known value y/Q is close to the unknown value c/r. Performing 
        classical fraction expansion on y/Q allows us to find approximations d/s of it that satisfy two conditions:
            A. s < N
            B. abs(y/Q - d/s) < 1/2Q
        Given the these multiple conditions (and assuming d/s is irreducible), s is very likely to be the appropriate
        period r, or at least a factor of it.
    8. Check (classically) if f(x) = f(x+s) which is equivalent to checking a**s = 1 (mod N). If so then done.
    9. Else, obtain more candidates for r by using multiples of s, or by using other s with d/s near y/Q. If any 
        candidate works, then we are done.
    10. Otherwise, try again starting from step 1 of this subroutine.
"""


def construct_function(a, N):
    def func(x):
        return a**x % N
    return func


def continued_fraction_representation(N):



def quantum_subroutine(a, N):
    q = np.floor(1 + 2*np.log(N)/np.log(2))  # from the inequality 2log_2(N) =< q < 1 + 2log_2(N)
    numStates = 2**q

    inputReg = qs.equiprobable(numStates)
    outputReg = qs.zeros(q)

    # We need an operator that maps |a>|0>**q state to |a>|x**a mod N>**q state
    crtState = inputReg * outputReg
    f = construct_function(a, N)
    size = len(crtState.vector)
    operatorMatrix = np.zeros((size, size))
    half = int(len(size / 2))  # used to quickly extract left bits from right bits1
    for i in range(size):
        for j in range(size):
            binj = str(qs.decimal_to_binary(j))  # Need to manually add 0 bits to the left if j is small
            if len(binj) != q:
                binj = '0' * (q - len(binj)) + binj
            inputRegBits = binj[:half]
            outputRegBits = binj[half:]
            inputRegNumber = qs.binary_to_decimal(inputRegBits)
            functionMapBin = qs.decimal_to_binary(f(inputRegNumber))
            if qs.binary_to_decimal(str(inputRegBits) + str(functionMapBin)) == i:
                operatorMatrix[i][j] = 1

    # Is it called an oracle??
    oracle = qs.QuantumGate(operatorMatrix)
    crtState = oracle(crtState)

    # Now apply inverse QFT to the input register (combine with I gate for the output register)
    crtState = (qs.inverse_QFT_operator(q) * qs.iGate(q))(crtState)

    # Perform the measurement now
    measurement = crtState.measure()
    # Extract the measurement of the leftmost half bits
    y = qs.binary_to_decimal(qs.decimal_to_binary(measurement)[:half])



def shor_algorithm(N):
    if N % 2 == 0:
        raise ValueError("Number is even.")

    for k in range(2, round(np.log(N) / np.log(3)) + 1):
        possibleFactor = N**(1/k)
        if possibleFactor.is_integer():
            return possibleFactor

    flag = 1

    while flag != 0:
        a = np.random.randint(2, N)  # low is inclusive, high is exclusive

        gcd = np.gcd(a, N)

        if gcd != 1:
            return gcd
        else:
            quantum_subroutine(a, N)
