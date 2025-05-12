import numpy as np
from numpy import cos, sin, arctan2, arccos, arcsin, sqrt, pi
from numpy.linalg import norm
from functools import reduce
from utils import ht, ht_inv

def fkine(q, DH):
    T = [ht(q[i] + DH['q_0'][i], DH['d'][i], DH['a'][i], DH['alpha'][i]) for i in range(6)]

    T06 = reduce(np.matmul, T)

    theta = np.zeros((6,))

    R06 = T06[:-1,:-1]
    theta[:3] = T06[:3,3]

    R = R06

    # to Euler angles
    if abs(R[2,2]) < 1:
        theta[3] = arctan2(R[1,2], R[0,2])
        theta[4] = arctan2(sqrt(1 - R[2,2]**2), R[2,2])
        theta[5] = arctan2(R[2,1], -R[2,0])
    elif R[2,2] == 1:
        theta[3] = 0
        theta[4] = 0
        theta[5] = arctan2(R[1,0], R[0,0])
    elif R[2,2] == -1:
        theta[3] = arctan2(-R[0,1], -R[0,0])
        theta[4] = np.pi
        theta[5] = 0

    return theta[:3], theta[3:]