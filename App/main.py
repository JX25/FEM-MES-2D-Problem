from App.grid import Grid
from App.element import Element
from App.node import Node

if __name__ == '__main__':
    mes_grid = Grid()

    points = [Node(0, 0, 0, 1), Node(0.025, 0, 0, 1), Node(0.025, 0.025, 0, 1), Node(0, 0.025, 0, 1)]
    element = Element(0, 1, 2, 3, points[0], points[1], points[2], points[3], 30, 700, 7800)

    element.create_matrix_h()
    element.create_matrix_c()

    print(element.matrix_H)





