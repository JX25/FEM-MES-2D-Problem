from App.node import Node
from App.element import Element
import numpy as np
from numpy.linalg import inv
import App.func
import App.const
from App.const import nH, nL, H, L, time_step, time


class Grid:
    def __init__(self):
        starting_tmp = App.const.temp_start
        delta_h = H / (nH-1)
        delta_l = L / (nL-1)
        self.global_matrix_h = np.zeros((nL * nH, nH * nL))
        self.global_matrix_c = np.zeros((nL * nH, nH * nL))
        self.global_matrix_h_bc = np.zeros((nL * nH, nH * nL))
        self.global_vector_p = np.zeros((nL * nH, 1))
        self.nodes = []
        i = 0
        x = 0
        while i <= nL - 1:
            j = 0
            y = 0
            while j <= nH - 1:
                border = App.func.is_border(i, j, nL - 1, nH - 1)
                self.nodes.append(Node(x, y, starting_tmp, border))
                y = y + delta_h
                j = j + 1
            x = x + delta_l
            i = i + 1

        self.elements = []

        for i in range(0, nL - 1):
            vertex_a = nH * i
            vertex_b = nH * i + nH
            vertex_c = vertex_b + 1
            vertex_d = vertex_a + 1
            for j in range(0, nH - 1):
                element = Element(vertex_a, vertex_b, vertex_c, vertex_d, self.nodes[vertex_a], self.nodes[vertex_b],
                                  self.nodes[vertex_c], self.nodes[vertex_d])
                element.create_matrix_h()
                element.create_matrix_c()
                element.create_vector_p()
                self.elements.append(element)
                vertex_a = vertex_d
                vertex_b = vertex_c
                vertex_c = vertex_b + 1
                vertex_d = vertex_a + 1

    def create_global_matrix_h_bc(self):
        self.global_matrix_h_bc.fill(0)
        for element in self.elements:
            for i, ii in zip(element.id, range(0, 4)):
                for j, jj in zip(element.id, range(0, 4)):
                    self.global_matrix_h_bc[i, j] += element.matrix_h_bc[ii, jj]

    def create_global_matrix_h(self):
        self.global_matrix_h.fill(0)
        for element in self.elements:
            for i, ii in zip(element.id, range(0, 4)):
                for j, jj in zip(element.id, range(0, 4)):
                    self.global_matrix_h[i, j] += element.matrix_h[ii, jj]

    def create_global_matrix_c(self):
        self.global_matrix_c.fill(0)
        for element in self.elements:
            for i, ii in zip(element.id, range(0, 4)):
                for j, jj in zip(element.id, range(0, 4)):
                    self.global_matrix_c[i, j] += element.matrix_c[ii, jj]

    def create_global_vector_p(self):
        self.global_vector_p.fill(0)
        for element in self.elements:
            for i, ii in zip(element.id, range(0, 4)):
                    self.global_vector_p[i] += element.vector_p[ii]

    def compute_vector_p(self):
        vector_t = []
        for node in self.nodes:
            vector_t.append(node.t)
        vector_t = np.asarray(vector_t).reshape(nH*nL, 1)
        result = (self.global_matrix_c/time_step).dot(vector_t)
        self.create_global_vector_p()
        self.global_vector_p += result.reshape(nH*nL, 1)

    def compute_matrix_h(self):
        self.global_matrix_h += self.global_matrix_h_bc + self.global_matrix_c/time_step

    def update_temp(self):
        temp_vector = []
        for node in self.nodes:
            temp_vector.append(node.t)
        matrix_a = np.linalg.inv(self.global_matrix_h)
        new_temp_vector = matrix_a.dot(self.global_vector_p)
        i = 0
        for node in self.nodes:
            node.t = new_temp_vector[i, 0]
            i += 1

    def solve(self):

        print("Temperatures after: 0sec")
        self.print_nodes_temp()

        _time = time_step
        while _time <= time:
            self.create_global_matrix_c()
            self.create_global_vector_p()
            self.create_global_matrix_h()
            self.create_global_matrix_h_bc()
            self.compute_matrix_h()
            self.compute_vector_p()
            self.update_temp()
            print("Temperatures after: "+str(_time)+"sec")
            self.print_nodes_temp()
            _time += time_step

    def print_nodes_temp(self):
        temps = []
        for node in self.nodes:
            temps.append(node.t)
        temps = np.asarray(temps).reshape(4, 4)
        print(temps)
        _max = np.max(temps)
        _min = np.min(temps)
        print("MIN: "+str(round(_min, 3)) + " MAX: " + str(round(_max, 3))+"\n\n")

    def print_grid(self):
        for node in self.nodes:
            print(str(node.br))

    def print_nodes(self):
        for node in self.nodes:
            print(node)

    def print_elements(self):
        i = 0
        for element in self.elements:
            print(
                str(i) + "\t\t" + str(element.id[0]) + " " + str(element.id[1]) + " " + str(element.id[2]) + " " + str(
                    element.id[3]))
            i += 1
        return
