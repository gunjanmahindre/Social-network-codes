from dimredu.eRPCAviaADMMFast import eRPCA as eRPCASparse
from dimredu.sRPCAviaADMMFast import sRPCA as sRPCASparse
import numpy as np


def denseToSparse(M, E):
    assert M.shape == E.shape, 'shape mismatch'
    m = M.shape[0]
    n = M.shape[1]

    u = np.empty([m * n])
    v = np.empty([m * n])
    vecM = np.empty([m * n])
    vecE = np.empty([m * n])

    k = 0
    for i in range(m):
        for j in range(n):
            u[k] = i
            v[k] = j
            vecM[k] = M[i, j]
            vecE[k] = E[i, j]
            k += 1

    return m, n, u, v, vecM, vecE


def eRPCA(M, E, **kw):
    m, n, u, v, vecM, vecE = denseToSparse(M, E)
    maxRank = np.min(M.shape)
    return eRPCASparse(m, n, u, v, vecM, vecE, maxRank, **kw)


def MCWithBounds(U, L, **kw):
    M = (U+L)/2
    E = (U-L)/2
    m, n, u, v, vecM, vecE = denseToSparse(M, E)
    maxRank = np.min(M.shape)
    U, E, VT, S, B = sRPCASparse(m, n, u, v, vecM, vecE, maxRank,
                                 SOff=True, **kw)
    return U, E, VT


def test_eRPCA():
    X = np.random.random(size=[5, 15])
    E = np.ones(X.shape)*1e-6
    eRPCA(X, E)


def test_MCWithBounds():
    Lower = np.random.random(size=[5, 15])
    Upper = Lower+1
    U, E, VT = MCWithBounds(Upper, Lower)
    M = U*np.diag(E)*VT
    assert np.all((Lower-(1e-3)) <= M), "Bound not satisfied"
    assert np.all(M <= (Upper+(1e-3))), "Bound not satisfied"
    assert (np.linalg.norm(M, 'nuc') <=
            np.linalg.norm(Lower, 'nuc')), "not optimal"
    assert (np.linalg.norm(M, 'nuc') <=
            np.linalg.norm(Upper, 'nuc')), "not optimal"


if __name__ == '__main__':
    test_eRPCA()
    test_MCWithBounds()
