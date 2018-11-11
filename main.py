from App.grid import Grid
# =================================
from App.element import Element
from App.node import Node


if __name__ == '__main__':
    mes_grid = Grid()
    print("================\n")

    points = []
    points.append(Node(0, 0, 0))
    points.append(Node(0.025, 0, 0))
    points.append(Node(0.025, 0.025, 0))
    points.append(Node(0, 0.025, 0))
    element = Element(0, 1, 2, 3, points[0], points[1], points[2], points[3])
    element.create_matrix()
    print(element.matrix)
    print(element.matrix_d_ksi_d_eta)
    print(element.dets)

    element.create_matrix_dn_dx()
    element.create_matrix_dn_dy()
    element.create_point_matrixes()


