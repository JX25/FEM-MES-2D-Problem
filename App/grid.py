import json
import os
from App.node import Node
from App.element import Element
import numpy as np
from numpy.linalg import inv
from App.func import load_from_json, time_step, temp_start, time


class Properties:
    def __init__(self):
        conf = os.getcwd() + "/config.json"
        data = load_from_json(conf)
        self.H = data["H"]
        self.L = data["L"]
        self.nH = data["nH"]
        self.nL = data["nL"]
        self.K = data["K"]
        self.C = data["C"]
        self.Ro = data["Ro"]
        self.alfa = data["alfa"]


class Grid:
    def __init__(self):
        property = Properties()
        # temperatura startowa, moze sie pojawic w configu!
        starting_tmp = temp_start;
        self.nH = property.nH
        self.nL = property.nL
        delta_H = property.H / property.nH
        delta_L = property.L / property.nL
        self.global_matrix_h = np.zeros((self.nL*self.nH, self.nH*self.nL))
        self.global_matrix_c = np.zeros((self.nL*self.nH, self.nH*self.nL))
        self.global_matrix_h_bc = np.zeros((self.nL*self.nH, self.nH*self.nL))
        self.global_vector_p = np.zeros((self.nL*self.nH, 1))
        self.nodes = []
        i = 0
        x = 0
        while i <= property.nL - 1:
            j = 0
            y = 0
            while j <= property.nH - 1:
                border = self.is_border(i, j, property.nL - 1, property.nH - 1)
                self.nodes.append(Node(x, y, starting_tmp, border))
                y = y + delta_H
                j = j + 1
            x = x + delta_L
            i = i + 1

        self.elements = []

        for i in range(0, property.nL - 1):
            vertex_a = self.nH * i
            vertex_b = self.nH * i + self.nH
            vertex_c = vertex_b + 1
            vertex_d = vertex_a + 1
            for j in range(0, property.nH - 1):
                element = Element(vertex_a, vertex_b, vertex_c, vertex_d, self.nodes[vertex_a], self.nodes[vertex_b],
                                  self.nodes[vertex_c], self.nodes[vertex_d], property.K, property.C, property.Ro,
                                  property.alfa)
                element.create_matrix_h()
                element.create_matrix_c()
                element.create_vector_p()
                self.elements.append(element)
                vertex_a = vertex_d
                vertex_b = vertex_c
                vertex_c = vertex_b + 1
                vertex_d = vertex_a + 1

        #self.print_nodes()
        #print("====")
        #self.print_elements()
    def create_global_matrix_h_bc(self):
        for element in self.elements:
            for i, ii in zip(element.id, range(0, 4)):
                for j, jj in zip(element.id, range(0, 4)):
                    self.global_matrix_h_bc[i, j] += element.matrix_h_bc[ii, jj]

    def create_global_matrix_h(self):
        for element in self.elements:
            for i, ii in zip(element.id, range(0, 4)):
                for j, jj in zip(element.id, range(0, 4)):
                    self.global_matrix_h[i, j] += element.matrix_H[ii, jj]

    def create_global_matrix_c(self):
        for element in self.elements:
            for i, ii in zip(element.id, range(0, 4)):
                for j, jj in zip(element.id, range(0, 4)):
                    self.global_matrix_c[i, j] += element.matrix_c[ii, jj]

    def create_global_vector_p(self):
        for element in self.elements:
            for i, ii in zip(element.id, range(0, 4)):
                    self.global_vector_p[i] += element.vector_p[ii]

    def compute_vector_p(self):
        vector_t = []
        for node in self.nodes:
            vector_t.append(node.t)
        vector_t = np.asarray(vector_t).reshape(self.nH*self.nL, 1)
        result = (self.global_matrix_c/time_step).dot(vector_t)
        self.global_vector_p.fill(0)
        self.create_global_vector_p()
        self.global_vector_p += result.reshape(self.nH*self.nL, 1)

    def compute_matrix_h(self):
        self.global_matrix_h += self.global_matrix_h_bc + self.global_matrix_c/time_step
       # print(self.global_matrix_h)
       # print("sd")

    def update_temp(self):
        temp_vector = []
        for node in self.nodes:
            temp_vector.append(node.t)
        A = np.linalg.inv(self.global_matrix_h)
        new_temp_vector = A.dot(self.global_vector_p)
        i = 0
        for node in self.nodes:
            node.t = new_temp_vector[i, 0]
            i += 1


    def solve(self):
        self.create_global_matrix_c()
        self.create_global_vector_p()
        self.create_global_matrix_h()
        self.create_global_matrix_h_bc()
        self.compute_matrix_h()
        print("Temperatures after: 0sec")
        self.print_nodes_temp()

        _time = time_step
        while _time <= time:
            self.compute_vector_p()
            #self.compute_matrix_h()
            self.update_temp()
            print("Temperatures after: "+str(_time)+"sec")
            self.print_nodes_temp()
            _time += time_step

    def is_border(self, x, y, max_x, max_y):
        if x == max_x or y == max_y or x == 0 or y == 0:
            return 1
        return 0

    def print_nodes_temp(self):
        temps = []
        for node in self.nodes:
            temps.append(node.t)
        temps = np.asarray(temps).reshape(4, 4)
        print(temps)
        _max = np.max(temps)
        _min = np.min(temps)
        print("MIN: "+str(_min) + " MAX: " + str(_max))
        print("===================")



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
