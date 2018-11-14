import math

import numpy as np

from App.node import Node


def n1(ksi, eta):
    return 0.25*(1-ksi)*(1-eta)


def n2(ksi, eta):
    return 0.25*(1+ksi)*(1-eta)


def n3(ksi, eta):
    return 0.25*(1+ksi)*(1+eta)


def n4(ksi, eta):
    return 0.25*(1-ksi)*(1+eta)


def n1_d_ksi(eta):
    return -0.25*(1-eta)


def n2_d_ksi(eta):
    return 0.25*(1-eta)


def n3_d_ksi(eta):
    return 0.25*(1+eta)


def n4_d_ksi(eta):
    return -0.25*(1+eta)


def n1_d_eta(ksi):
    return -0.25*(1-ksi)


def n2_d_eta(ksi):
    return -0.25*(1+ksi)


def n3_d_eta(ksi):
    return 0.25*(1+ksi)


def n4_d_eta(ksi):
    return 0.25*(1-ksi)


REV_SQRT3 = 1/math.sqrt(3)
KSI = [-REV_SQRT3, REV_SQRT3, REV_SQRT3, -REV_SQRT3]
ETA = [-REV_SQRT3, -REV_SQRT3, REV_SQRT3, REV_SQRT3]


N1 = []
N2 = []
N3 = []
N4 = []

for i in range(0, 4):
    N1.append(n1(KSI[i], ETA[i]))
    N2.append(n2(KSI[i], ETA[i]))
    N3.append(n3(KSI[i], ETA[i]))
    N4.append(n4(KSI[i], ETA[i]))

N = []
N.append(N1)
N.append(N2)
N.append(N3)
N.append(N4)

# for row in N:
#    print(str(row) + "\n")


N1_d_KSI = []
N2_d_KSI = []
N3_d_KSI = []
N4_d_KSI = []

N1_d_ETA = []
N2_d_ETA = []
N3_d_ETA = []
N4_d_ETA = []

for i in range(0, 4):
    N1_d_KSI.append(n1_d_ksi(ETA[i]))
    N2_d_KSI.append(n2_d_ksi(ETA[i]))
    N3_d_KSI.append(n3_d_ksi(ETA[i]))
    N4_d_KSI.append(n4_d_ksi(ETA[i]))

    N1_d_ETA.append(n1_d_eta(KSI[i]))
    N2_d_ETA.append(n2_d_eta(KSI[i]))
    N3_d_ETA.append(n3_d_eta(KSI[i]))
    N4_d_ETA.append(n4_d_eta(KSI[i]))


N_d_KSI = []
N_d_ETA = []

N_d_KSI.append(N1_d_KSI);
N_d_KSI.append(N2_d_KSI);
N_d_KSI.append(N3_d_KSI);
N_d_KSI.append(N4_d_KSI);
N_d_KSI = np.asmatrix(N_d_KSI)


N_d_ETA.append(N1_d_ETA);
N_d_ETA.append(N2_d_ETA);
N_d_ETA.append(N3_d_ETA);
N_d_ETA.append(N4_d_ETA);
N_d_ETA = np.asmatrix(N_d_ETA)


N_d_KSI_t = np.transpose(N_d_KSI)
N_d_ETA_t = np.transpose(N_d_ETA)

print(N_d_KSI_t)
print(N_d_ETA_t)