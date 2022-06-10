#writen by Dr. Ardiansyah (ardi.plj@gmail.com) in 2022 for Hydrology Analysis
#don't delete this first two lines

import numpy as np

def unitHydrograph(N, M, P, Q):
    #create P matrix N x (N-M+1)
    Pmat = np.zeros(N*(N-M+1))
    Pmat = Pmat.reshape(N,(N-M+1))
    #fill P matrix with rainfall data
    for row in range(N):
        for col in range(N-M+1):
            Pidx = row-col
            if (Pidx > (M-1)) or (Pidx < 0):
                Pmat[row, col] = 0
            else:
                Pmat[row, col] = P[Pidx]

    Pmat_tr = Pmat.transpose()
    Pmat1 = np.dot(Pmat_tr, Pmat)
    Pmat2 = np.linalg.inv(Pmat1)
    Pmat3 = np.dot(Pmat2, Pmat_tr)
    UH = np.dot(Pmat3, Q)
    return UH #array


def runoffDischarge(N, M, P, UH):
    #create P matrix N x (N-M+1)
    Pmat = np.zeros(N*(N-M+1))
    Pmat = Pmat.reshape(N,(N-M+1))
    #fill P matrix with rainfall data
    for row in range(N):
        for col in range(N-M+1):
            Pidx = row-col
            if (Pidx > (M-1)) or (Pidx < 0):
                Pmat[row, col] = 0
            else:
                Pmat[row, col] = P[Pidx]

    Q = np.dot(Pmat,UH)
    return Q #array


if __name__ == "__main__": #make this module can be run independently for testing
    import sys

    #example of UH and Eff Rainfall data
    P = np.array([5, 25, 10, 3])
    M = 4
    UH = np.array([2, 6, 8, 22, 108, 32, 16, 6, 5, 4, 2])
    U = 11
    N = U+M-1


    Q = runoffDischarge(N, M, P, UH)
    print (Q)
