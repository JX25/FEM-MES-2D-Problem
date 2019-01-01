import numpy as np
import App.node
import App.func


class Element:
    def __init__(self, a, b, c, d, vertex1, vertex2, vertex3, vertex4, K, C, Ro, alfa):
        # initialize nodes, vertexes,
        self.nodes = [vertex1, vertex2, vertex3, vertex4]
        self.id = [a, b, c, d]
        # material properties
        self.K = K
        self.C = C
        self.Ro = Ro
        self.alfa = alfa
        # matrix
        self.matrix_d_ksi_d_eta = []
        self.dets = []
        self.matrix = []
        self.dn_dx = []
        self.dn_dy = []
        self.points_matrixes = []
        self.dndx_dndxt = []
        self.dndy_dndyt = []
        self.dndx_dndxt_det = []
        self.dndy_dndyt_det = []
        # matrix h
        self.sum_point_matrix = []
        self.multiply_sum_matrix = []
        self.matrix_H = []
        # matrix c
        self.matrixs_points_c = []
        self.matrix_c = []
        # matrix hbc
        self.matrix_h_bc = []
        #vector p
        self.vector_p = []


    def __getitem__(self, index):
        return self.id[index]

    def __setitem__(self, index, value):
        self.id[index] = value

    def transform_points(self):  # transformacja punktow
        for i in range(0, 4):
            new_x = 0
            new_y = 0
            for j in range(0, 4):
                new_x = new_x + self.nodes[j].x * App.func.N[i][j]
                new_y = new_y + self.nodes[j].y * App.func.N[i][j]
            self.nodes[i].ksi = new_x
            self.nodes[i].eta = new_y

    def create_matrix_d_ksi_d_eta(self):  # stworzenie macierzy dksi deta
        row = [] # first row X and dKSI
        for i in range(0, 4):
            value = 0
            j = 0
            for node in self.nodes:
                value = value + node.x * App.func.N_d_KSI[j, i]
                j = j + 1
            row.append(value)
        self.matrix_d_ksi_d_eta.append(row)
        row = [] # second row Y and dKSI
        for i in range(0, 4):
            value = 0
            j = 0
            for node in self.nodes:
                value = value + node.y * App.func.N_d_KSI[j, i]
                j = j + 1
            row.append(value)
        self.matrix_d_ksi_d_eta.append(row)
        row = [] # third row X and dETA
        for i in range(0, 4):
            value = 0
            j = 0
            for node in self.nodes:
                value = value + node.x * App.func.N_d_ETA[j, i]
                j = j + 1
            row.append(value)
        self.matrix_d_ksi_d_eta.append(row)
        row = [] # fourth row Y and dETA
        for i in range(0, 4):
            value = 0
            j = 0
            for node in self.nodes:
                value = value + node.y * App.func.N_d_ETA[j, i]
                j = j + 1
            row.append(value)
        self.matrix_d_ksi_d_eta.append(row)
        self.matrix_d_ksi_d_eta = np.asmatrix(np.array(self.matrix_d_ksi_d_eta))

    def count_dets(self):  # Obliczenie wyznacznikow z macierzy dksi deta
        self.dets.append(self.matrix_d_ksi_d_eta[0, 0] * self.matrix_d_ksi_d_eta[3, 0] - self.matrix_d_ksi_d_eta[1, 0] *
                         self.matrix_d_ksi_d_eta[2, 0])

        self.dets.append(self.matrix_d_ksi_d_eta[0, 1] * self.matrix_d_ksi_d_eta[3, 1] - self.matrix_d_ksi_d_eta[1, 1] *
                         self.matrix_d_ksi_d_eta[2, 1])

        self.dets.append(self.matrix_d_ksi_d_eta[0, 2] * self.matrix_d_ksi_d_eta[3, 2] - self.matrix_d_ksi_d_eta[1, 2] *
                         self.matrix_d_ksi_d_eta[2, 2])

        self.dets.append(self.matrix_d_ksi_d_eta[0, 3] * self.matrix_d_ksi_d_eta[3, 3] - self.matrix_d_ksi_d_eta[1, 3] *
                         self.matrix_d_ksi_d_eta[2, 3])

        self.dets = np.array(self.dets)

    def print_dets(self):
        print(str(self.dets))

    def div_matrix(self):       # Dzieli kolumny macierzy dksi deta przez wyznaczniki 1<->4 4<->1 2<->-2 3<->3
        m = np.zeros((4, 4))
        for i in range(0, 4):
            for j in range(0, 4):
                if j == 0:
                    m[3, i] = (self.matrix_d_ksi_d_eta[j, i] / self.dets[i])
                elif j == 3:
                    m[0, i] = (self.matrix_d_ksi_d_eta[j, i] / self.dets[i])
                else:
                    m[j, i] = (self.matrix_d_ksi_d_eta[j, i] / self.dets[i])
                    if j == 1:
                        m[j, i] = m[j, i] * (-1)
            self.matrix = m

    def create_matrix_dn_dx(self):      # Tworzy macierz dN/dx
        self.dn_dx = np.zeros((4, 4))
        for i in range(0, 4):
            for j in range(0, 4):
                self.dn_dx[i, j] = self.matrix[0, i] * App.func.N_d_KSI_t[i, j] + self.matrix[1, i] * App.func.N_d_ETA_t[i, j]
        # print(self.dn_dx)

    def create_matrix_dn_dy(self):      #Tworzy macierz dN/dy
        self.dn_dy = np.zeros((4, 4))
        for i in range(0, 4):
            for j in range(0, 4):
                self.dn_dy[i, j] = self.matrix[2, i] * App.func.N_d_KSI_t[i, j] + self.matrix[3, i] * App.func.N_d_ETA_t[i, j]
        # print(dn_dy)

    def create_point_matrixes(self):                # Tworzy punkty dla macierzy
        for row in self.dn_dx:                      # dla kazdego z punktow
            row = np.array(row)                     # {dN/dx} x {dN/dx}^T
            col = row                               # oraz
            result = np.outer(row, col)             # {dN/dy} x {dN/dy}^T
            self.dndx_dndxt.append(result)          #
        for row in self.dn_dy:                      #
            row = np.array(row)                     #
            col = row                               #
            result = np.outer(row, col)             #
            self.dndy_dndyt.append(result)          #

    def point_matrixes_det(self):
        i = 0
        for matrix in self.dndx_dndxt:
            matrix = matrix * self.dets[i]
            self.dndx_dndxt_det.append(matrix)
            i = i + 1
        i = 0
        for matrix in self.dndy_dndyt:
            matrix = matrix * self.dets[i]
            self.dndy_dndyt_det.append(matrix)
            i = i + 1

    def sum_point_matrixes(self):
        for matrixdx, matrixdy in zip(self.dndx_dndxt_det, self.dndy_dndyt_det):
            sum = np.add(matrixdx, matrixdy)
            self.sum_point_matrix.append(sum)

    def multiply_sum_matrixes(self):
        for matrix in self.sum_point_matrix:
            result = matrix * self.K
            self.multiply_sum_matrix.append(result)

    def add_multiply_sum_matrixes(self):
        self.matrix_H = np.zeros((4, 4))
        for matrix in self.multiply_sum_matrix:
            self.matrix_H = np.add(self.matrix_H, matrix)

    def create_matrix_h(self):
        self.transform_points()
        self.create_matrix_d_ksi_d_eta()
        self.count_dets()
        self.div_matrix()
        self.create_matrix_dn_dx()
        self.create_matrix_dn_dy()
        self.create_point_matrixes()
        self.point_matrixes_det()
        self.sum_point_matrixes()
        self.multiply_sum_matrixes()
        self.add_multiply_sum_matrixes()
        # uwzglednienie warunkow brzegowych funkcja create_matrix_h_bc

    def create_matrix_h_bc(self):
        matrix_h_bc = np.zeros((4, 4))
        matrix = np.outer(App.func.N_1_1d, App.func.N_1_1d) * self.alfa + np.outer(App.func.N_2_1d,
                                                                                     App.func.N_2_1d) * self.alfa
        # first wall
        if App.func.check_border_cond(self.nodes[0], self.nodes[1]):
            det = abs((self.nodes[1].x - self.nodes[0].x)/2.0)
            matrix_h_bc[0:2, 0:2] = matrix_h_bc[0:2, 0:2] + matrix * det
        # second wall
        if App.func.check_border_cond(self.nodes[1], self.nodes[2]):
            det = abs((self.nodes[2].y - self.nodes[1].y)/2.0)
            matrix_h_bc[1:3, 1:3] = matrix_h_bc[1:3, 1:3] + matrix * det
        # third wall
        if App.func.check_border_cond(self.nodes[2], self.nodes[3]):
            det = abs((self.nodes[3].x - self.nodes[2].x)/2.0)
            matrix_h_bc[2:4, 2:4] = matrix_h_bc[2:4, 2:4] + matrix * det
        # fourth wall
        if App.func.check_border_cond(self.nodes[3], self.nodes[0]):
            det = abs((self.nodes[3].y - self.nodes[0].y)/2.0)
            matrix_h_bc[0, 0] = matrix_h_bc[0, 0] + matrix[0, 0] * det
            matrix_h_bc[0, 3] = matrix_h_bc[0, 3] + matrix[0, 1] * det
            matrix_h_bc[3, 0] = matrix_h_bc[3, 0] + matrix[1, 0] * det
            matrix_h_bc[3, 3] = matrix_h_bc[3, 3] + matrix[1, 1] * det
        #print(matrix_h_bc)
        self.matrix_h_bc = matrix_h_bc

    def create_matrix_h_with_bc(self):
        self.create_matrix_h()
        self.create_matrix_h_bc()
        #self.matrix_H = np.add(self.matrix_h, self.matrix_h_bc) #  self.matrix_H[i, j] + self.matrix_h_bc[i, j]


    def multiply_points_matrix_c(self):
        #  self.matrixs_points_c
        for i in range(0, 4):
            self.matrixs_points_c.append(np.array(App.func.Nx_x_Nx[i]) * self.Ro * self.C * self.dets[i])

    def add_points_matrix_c(self):
        self.matrix_c = np.zeros((4, 4))
        for matrix in self.matrixs_points_c:
            self.matrix_c = np.add(self.matrix_c, matrix)

    def create_matrix_c(self):
        self.multiply_points_matrix_c()
        self.add_points_matrix_c()
        self.matrix_c = self.matrix_c / 0.5625


    def create_vector_p(self):
        self.vector_p = np.zeros((4, 1))
        for i in (4):
            self.vector_p = self.vector_p + App.func.alfa*np.asarray(App.func.N[i]).reshape(4,1)*App.func.amb_temp*self.dets[i]


# print output

    def print_matrix(self):
        print(self.matrix)

    def print_transformed_points(self):
        for node in self.nodes:
            node.print_transformed()

    def print_matrix_d_ksi_d_eta(self):
        for row in self.matrix_d_ksi_d_eta:
            print(str(row))


