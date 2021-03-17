import qsimulator as qs
import numpy as np
import time
from fractions import Fraction

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


def quantum_subroutine(a, N):
    inputRegQubitsNum = int(np.floor(1 + 2*np.log(N)/np.log(2)))  # from the inequality 2log_2(N) =< q < 1 + 2log_2(N)
    numStates = 2**inputRegQubitsNum

    inputReg = qs.equiprobable(inputRegQubitsNum)

    outputRegQubitsNum = int(np.ceil(np.log(N)/np.log(2)))
    outputReg = qs.zeros(outputRegQubitsNum)

    # We need an operator that maps |a>|0>**q state to |a>|x**a mod N>**q state
    crtState = inputReg * outputReg
    f = construct_function(a, N)
    size = len(crtState.vector)
    operatorMatrix = np.zeros((size, size))
    totalQubits = inputRegQubitsNum + outputRegQubitsNum

    # In order to optimize calculation times we ignore any entry in the matrix for which
    # current state is 0, meaning we can skip a lot of calculations
    time1 = time.time()
    for i in range(size):
        for j in range(0, size, 2**outputRegQubitsNum):
            binj = str(qs.decimal_to_binary(j))  # Need to manually add 0 bits to the left if j is small
            if len(binj) != totalQubits:
                binj = '0' * (totalQubits - len(binj)) + binj
            inputRegBits = binj[:inputRegQubitsNum]
            inputRegNumber = qs.binary_to_decimal(inputRegBits)
            functionMapBin = str(qs.decimal_to_binary(f(inputRegNumber)))
            if len(functionMapBin) != outputRegQubitsNum:
                functionMapBin = '0' * (outputRegQubitsNum - len(functionMapBin)) + functionMapBin
            if qs.binary_to_decimal(str(inputRegBits) + str(functionMapBin)) == i:
                operatorMatrix[i][j] = 1
    time2 = time.time()
    print("Time to construct the oracle matrix was {} s.".format(time2 - time1))

    # Is it called an oracle??
    oracle = qs.QuantumGate(operatorMatrix)
    crtState = oracle(crtState)
    time3 = time.time()
    print("Time to apply the matrix was {} s.".format(time3 - time2))

    # Measure the output register
    crtState = crtState.collapse_qubits(outputRegQubitsNum)

    # Apply QFT
    crtState = qs.QFT_operator(inputRegQubitsNum)(crtState)
    time4 = time.time()
    print("Time to apply the QFT was {} s.".format(time4 - time3))

    # Make measurement
    y = crtState.measure()
    print("Measured state is state number {}.".format(y))

    # Get the closest fraction to y/Q
    for i in range(3, N):
        frac = Fraction(y/numStates).limit_denominator(i)

        if frac.numerator == 0:
            return -1

        s = frac.denominator
        print("Guess for s is {}.".format(s))
        if abs(y/numStates - frac) < 1/(2*numStates):
            if a**s % N == 1:
                return s
            elif a**(2*s) % N == 1:
                return 2*s
            elif a**(3*s) % N == 1:
                return 3*s
            elif a**(4*s) % N == 1:
                return 4*s
            elif a**(5*s) % N == 1:
                return 5*s
    return -1


def shor_algorithm(N):
    if N % 2 == 0:
        raise ValueError("Number is even.")

    for k in range(2, round(np.log(N) / np.log(3)) + 1):
        possibleFactor = N**(1/k)
        if possibleFactor.is_integer() and N % possibleFactor == 0:
            return possibleFactor

    for _ in range(20):  # do some number of guesses
        a = np.random.randint(2, N)  # low is inclusive, high is exclusive
        print("Random guessed number is {}".format(a))

        gcd = np.gcd(a, N)

        if gcd != 1:
            return gcd
        else:
            for _ in range(4):  # do some number of subroutine tries
                print("-------------------")
                r = quantum_subroutine(a, N)
                if r != -1:
                    if r % 2 == 1 or a**(r/2) % N == N - 1:
                        pass
                    else:
                        return np.gcd(int(a ** (r / 2) + 1), N)  # equivalently return gcd(a**(r/2)-1,N)
    return None


if __name__ == "__main__":
    N = 15
    time1 = time.time()
    factor = shor_algorithm(N)
    time2 = time.time()
    print("One factor of the number {} is {}.".format(N, factor))
    print("Time taken for the whole algorithm to run was {} s.".format(time2 - time1))
