import numpy as np

import App.node
import App.func


class Element:
    def __init__(self, a, b, c, d, vertex1, vertex2, vertex3, vertex4):
        self.nodes = [vertex1, vertex2, vertex3, vertex4]
        self.id = [a, b, c, d]
        self.matrix_d_ksi_d_eta = []
        self.dets = []
        self.matrix = []
        self.dn_dx = []
        self.dn_dy = []
        self.points_matrixes = []
        self.four_points_matrixes = []
        self.matrix_H = []

    def __getitem__(self, index):
        return self.id[index]

    def __setitem__(self, index, value):
        self.id[index] = value

    def transform_points(self):
        for i in range(0, 4):
            new_x = 0
            new_y = 0
            for j in range(0, 4):
                new_x = new_x + self.nodes[j].x * App.func.N[i][j]
                new_y = new_y + self.nodes[j].y * App.func.N[i][j]
            self.nodes[i].ksi = new_x
            self.nodes[i].eta = new_y

    def print_transformed_points(self):
        for node in self.nodes:
            node.print_transformed()

    def print_matrix_d_ksi_d_eta(self):
        for row in self.matrix_d_ksi_d_eta:
            print(str(row))

    def create_matrix_d_ksi_d_eta(self):
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

    def count_dets(self):
        self.dets.append(self.matrix_d_ksi_d_eta[0, 0] * self.matrix_d_ksi_d_eta[3, 0] - self.matrix_d_ksi_d_eta[1, 0] * self.matrix_d_ksi_d_eta[2, 0])
        self.dets.append(self.matrix_d_ksi_d_eta[0, 1] * self.matrix_d_ksi_d_eta[3, 1] - self.matrix_d_ksi_d_eta[1, 1] * self.matrix_d_ksi_d_eta[2, 1])
        self.dets.append(self.matrix_d_ksi_d_eta[0, 2] * self.matrix_d_ksi_d_eta[3, 2] - self.matrix_d_ksi_d_eta[1, 2] * self.matrix_d_ksi_d_eta[2, 2])
        self.dets.append(self.matrix_d_ksi_d_eta[0, 3] * self.matrix_d_ksi_d_eta[3, 3] - self.matrix_d_ksi_d_eta[1, 3] * self.matrix_d_ksi_d_eta[2, 3])
        self.dets = np.array(self.dets)

    def print_dets(self):
        print(str(self.dets))

    def div_matrix(self):
        m = np.asmatrix([[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]])
        for i in range(0, 4):
            for j in range(0, 4):
                m[j, i] = (self.matrix_d_ksi_d_eta[j, i] / self.dets[i])
            self.matrix = m

    def create_matrix(self):
        self.transform_points()
        self.create_matrix_d_ksi_d_eta()
        self.count_dets()
        self.div_matrix()

    def print_matrix(self):
        print(self.matrix)

    def create_matrix_dn_dx(self):
        self.dn_dx = np.zeros((4, 4))
        for i in range(0, 4):
            for j in range(0, 4):
                self.dn_dx[i, j] = self.matrix[0, i] * App.func.N_d_KSI_t[i, j] + self.matrix[1, i] * App.func.N_d_ETA_t[i, j]
        # print(self.dn_dx)

    def create_matrix_dn_dy(self):
        self.dn_dy = np.zeros((4, 4))
        for i in range(0, 4):
            for j in range(0, 4):
                self.dn_dy[i, j] = self.matrix[2, i] * App.func.N_d_KSI_t[i, j] + self.matrix[3, i] * App.func.N_d_ETA_t[i, j]
        # print(dn_dy)

    def create_point_matrixes(self):
        for row in self.dn_dx:
            row = np.array(row)
            col = row
            result = np.outer(row, col)
            self.points_matrixes.append(result)
        for row in self.dn_dy:
            row = np.array(row)
            col = row
            result = np.outer(row, col)
            self.points_matrixes.append(result)


    def point_matrixes_det(self):
        for i in range(0,4):
            self.points_matrixes[i] = self.points_matrixes[i] * self.dets[i]
            self.points_matrixes[i+4] = self.points_matrixes[i + 4] * self.dets[i]

    def merge_two_matrixes(self, K):
        for i in range(0, 4):
            self.four_points_matrixes.append(np.add(self.points_matrixes[i], self.points_matrixes[i + 4]))
            self.four_points_matrixes[i] = self.four_points_matrixes[i] * K

    def create_matrix_h(self):
        self.matrix_H = np.zeros((4, 4))
        for matrix in self.four_points_matrixes:
            self.matrix_H = self.matrix_H + matrix
