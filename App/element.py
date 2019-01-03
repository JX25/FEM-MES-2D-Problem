import numpy as np
import App.node
import App.func
import App.const


class Element:
    def __init__(self, a, b, c, d, vertex1, vertex2, vertex3, vertex4):
        # initialize nodes, vertexes
        self.nodes = [vertex1, vertex2, vertex3, vertex4]
        self.id = [a, b, c, d]
        self.dets = []
        # matrices needed to compute matrix H
        self.matrix_d_ksi_d_eta = []
        self.matrix = []
        self.dn_dx = []
        self.dn_dy = []
        self.points_matrices = []
        self.dndx_dndxt = []
        self.dndy_dndyt = []
        self.dndx_dndxt_det = []
        self.dndy_dndyt_det = []
        self.sum_point_matrices = []
        self.multiply_sum_matrix = []
        # matrix h, h with bc
        self.matrix_h = []
        self.matrix_h_bc = []
        # matrix c for nodes, matrix c for element
        self.matrices_points_c = []
        self.matrix_c = []
        # load vector p
        self.vector_p = []

    def transform_points(self):  # transformation of (x,y) to (ksi, eta) coordinates
        for i in range(0, 4):
            new_x = 0
            new_y = 0
            for j in range(0, 4):
                new_x = new_x + self.nodes[j].x * App.func.N[i][j]
                new_y = new_y + self.nodes[j].y * App.func.N[i][j]
            self.nodes[i].ksi = new_x
            self.nodes[i].eta = new_y

    def create_matrix_d_ksi_d_eta(self):  # create matrix  dksi deta
        row = []  # first row X and dKSI
        for i in range(0, 4):
            value = 0
            j = 0
            for node in self.nodes:
                value = value + node.x * App.func.N_d_KSI[j, i]
                j = j + 1
            row.append(value)
        self.matrix_d_ksi_d_eta.append(row)
        row = []  # second row Y and dKSI
        for i in range(0, 4):
            value = 0
            j = 0
            for node in self.nodes:
                value = value + node.y * App.func.N_d_KSI[j, i]
                j = j + 1
            row.append(value)
        self.matrix_d_ksi_d_eta.append(row)
        row = []  # third row X and dETA
        for i in range(0, 4):
            value = 0
            j = 0
            for node in self.nodes:
                value = value + node.x * App.func.N_d_ETA[j, i]
                j = j + 1
            row.append(value)
        self.matrix_d_ksi_d_eta.append(row)
        row = []  # fourth row Y and dETA
        for i in range(0, 4):
            value = 0
            j = 0
            for node in self.nodes:
                value = value + node.y * App.func.N_d_ETA[j, i]
                j = j + 1
            row.append(value)
        self.matrix_d_ksi_d_eta.append(row)
        self.matrix_d_ksi_d_eta = np.asmatrix(np.array(self.matrix_d_ksi_d_eta))

    def count_dets(self):  # Compute determinantes from matrix dksi deta
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

    def div_matrix(self):
        """ Divide column of matrix dksi deta by determinants
            1col<->4det 4col<->1det 2col<->-2det 3col<->3det """
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

    def create_matrix_dn_dx(self):  # Create matrix dN/dx
        self.dn_dx = np.zeros((4, 4))
        for i in range(0, 4):
            for j in range(0, 4):
                self.dn_dx[i, j] = self.matrix[0, i] * App.func.N_d_KSI_t[i, j] + self.matrix[1, i] * \
                                   App.func.N_d_ETA_t[i, j]
        # print(self.dn_dx)

    def create_matrix_dn_dy(self):  # Create matrix dN/dy
        self.dn_dy = np.zeros((4, 4))
        for i in range(0, 4):
            for j in range(0, 4):
                self.dn_dy[i, j] = self.matrix[2, i] * App.func.N_d_KSI_t[i, j] + self.matrix[3, i] * \
                                   App.func.N_d_ETA_t[i, j]
        # print(dn_dy)

    def create_point_matrixes(self):  # Create points for matrix
        for row in self.dn_dx:        # for every of points
            row = np.array(row)       # {dN/dx} x {dN/dx}^T
            col = row                 # and
            result = np.outer(row, col)  # {dN/dy} x {dN/dy}^T
            self.dndx_dndxt.append(result)
        for row in self.dn_dy:
            row = np.array(row)
            col = row
            result = np.outer(row, col)
            self.dndy_dndyt.append(result)

    def point_matrices_det(self):
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

    def sum_four_point_matrices(self):
        for matrix_dx, matrix_dy in zip(self.dndx_dndxt_det, self.dndy_dndyt_det):
            _sum = np.add(matrix_dx, matrix_dy)
            self.sum_point_matrices.append(_sum)

    def multiply_sum_matrices(self):
        for matrix in self.sum_point_matrices:
            result = matrix * App.const.K
            self.multiply_sum_matrix.append(result)

    def add_multiply_sum_matrices(self):
        self.matrix_h = np.zeros((4, 4))
        for matrix in self.multiply_sum_matrix:
            self.matrix_h = np.add(self.matrix_h, matrix)

    def create_matrix_h(self):
        self.transform_points()
        self.create_matrix_d_ksi_d_eta()
        self.count_dets()
        self.div_matrix()
        self.create_matrix_dn_dx()
        self.create_matrix_dn_dy()
        self.create_point_matrixes()
        self.point_matrices_det()
        self.sum_four_point_matrices()
        self.multiply_sum_matrices()
        self.add_multiply_sum_matrices()
        self.create_matrix_h_bc()

    def create_matrix_h_bc(self):
        matrix_h_bc = np.zeros((4, 4))
        if abs((self.nodes[1].x - self.nodes[0].x) / 2.0) != 0:
            det = abs((self.nodes[1].x - self.nodes[0].x) / 2.0)
        else:
            det = abs((self.nodes[1].y - self.nodes[0].y) / 2.0)
        matrix = np.outer(App.func.N_1_1d, App.func.N_1_1d) + np.outer(App.func.N_2_1d, App.func.N_2_1d)
        matrix *= App.const.alfa
        # first wall
        if App.func.check_border_cond(self.nodes[0], self.nodes[1]):
            matrix_h_bc[0:2, 0:2] = matrix_h_bc[0:2, 0:2] + matrix * det
        # second wall
        if App.func.check_border_cond(self.nodes[1], self.nodes[2]):
            matrix_h_bc[1:3, 1:3] = matrix_h_bc[1:3, 1:3] + matrix * det
        # third wall
        if App.func.check_border_cond(self.nodes[2], self.nodes[3]):
            matrix_h_bc[2:4, 2:4] = matrix_h_bc[2:4, 2:4] + matrix * det
        # fourth wall
        if App.func.check_border_cond(self.nodes[3], self.nodes[0]):
            matrix_h_bc[0, 0] = matrix_h_bc[0, 0] + matrix[0, 0] * det
            matrix_h_bc[0, 3] = matrix_h_bc[0, 3] + matrix[0, 1] * det
            matrix_h_bc[3, 0] = matrix_h_bc[3, 0] + matrix[1, 0] * det
            matrix_h_bc[3, 3] = matrix_h_bc[3, 3] + matrix[1, 1] * det
        self.matrix_h_bc = matrix_h_bc

    def multiply_points_matrix_c(self):
        for i in range(0, 4):
            self.matrices_points_c.append(np.array(App.func.Nx_x_Nx[i]) * App.const.Ro * App.const.C * self.dets[i])

    def add_points_matrix_c(self):
        self.matrix_c = np.zeros((4, 4))
        for matrix in self.matrices_points_c:
            self.matrix_c = np.add(self.matrix_c, matrix)

    def create_matrix_c(self):
        self.multiply_points_matrix_c()
        self.add_points_matrix_c()
        self.matrix_c = self.matrix_c

    def create_vector_p(self):
        self.vector_p = np.zeros((4, 1))
        det = abs(self.nodes[0].x - self.nodes[1].x)
        for i in range(0, 2):
            for j in range(0, 4):
                if App.func.check_border_cond(self.nodes[j], self.nodes[(j + 1) % 4]):
                    self.vector_p[j] += App.func.N1_1d[i][j] + App.func.N2_1d[i][j]

        self.vector_p *= App.const.amb_temp * App.const.alfa * det

    def print_matrix(self):
        print(self.matrix)

    def print_transformed_points(self):
        for node in self.nodes:
            node.print_transformed()

    def print_matrix_d_ksi_d_eta(self):
        for row in self.matrix_d_ksi_d_eta:
            print(str(row))
