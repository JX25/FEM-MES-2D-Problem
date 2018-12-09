import math
import numpy as np


def n1_1d(ksi):
    return 0.5*(1-ksi)


def n2_1d(ksi):
    return 0.5*(1+ksi)


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


def check_border_cond(node1, node2):
    if node1.br == node2.br == 1:
        return True
    return False


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


N1xN1 = np.outer(N1, N1)
N2xN2 = np.outer(N2, N2)
N3xN3 = np.outer(N3, N3)
N4xN4 = np.outer(N4, N4)

Nx_x_Nx = [N1xN1, N2xN2, N3xN3, N4xN4]

print(N1xN1)

N = [N1, N2, N3, N4]

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

N_d_KSI.append(N1_d_KSI)
N_d_KSI.append(N2_d_KSI)
N_d_KSI.append(N3_d_KSI)
N_d_KSI.append(N4_d_KSI)
N_d_KSI = np.asmatrix(N_d_KSI)

N_d_ETA.append(N1_d_ETA)
N_d_ETA.append(N2_d_ETA)
N_d_ETA.append(N3_d_ETA)
N_d_ETA.append(N4_d_ETA)
N_d_ETA = np.asmatrix(N_d_ETA)

N_d_KSI_t = np.transpose(N_d_KSI)
N_d_ETA_t = np.transpose(N_d_ETA)

#print(N_d_KSI_t)
#print(N_d_ETA_t)

# print(N_d_ETA)
# print(N_d_KSI)
# print(str(KSI))
# print(str(ETA))
# print("\n")
# print(str(N1))
# print(str(N2))
# print(str(N3))
# print(str(N4))
# print("\n")
# print(str(N1_d_KSI))
# print(str(N2_d_KSI))
# print(str(N3_d_KSI))
# print(str(N4_d_KSI))
# print("\n")
# print(str(N1_d_ETA))
# print(str(N2_d_ETA))
# print(str(N3_d_ETA))
# print(str(N4_d_ETA))
# print("\n")
# for N in N_d_ETA:
#    print(str(N))
#    print("\n")

