import numpy as np

# Define single-qubit H gate as gh
gh = (2**(-0.5))*np.array([[1,1],[1,-1]])

# Define tensor product function for 2 matrices
# Need to write vectors as np.array([[v1,v2,...]]) for tp to work
def tp(m1, m2):
    (a,b) = m1.shape
    (c,d) = m2.shape
    pm = np.zeros((a*c,b*d))
    i = 0
    j = 0
    for i in range(a):
        for j in range(b):
            for k in range(c):
                for l in range(d):
                    pm[i*c+k,j*d+l] = m1[i,j]*m2[k,l]
    print(pm)

a = np.array([[1,2]])
b = np.array([[0,0,1]])
tp(a,b)
