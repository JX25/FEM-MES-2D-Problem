from App.grid import Grid
from App.element import Element
from App.node import Node

if __name__ == '__main__':
    mes_grid = Grid()

   #points = [Node(0, 0, 0, 1), Node(0.1, 0, 0, 1), Node(0.1, 0.1, 0, 0), Node(0, 0.1, 0, 0)]
   # element = Element(0, 1, 2, 3, points[0], points[1], points[2], points[3], 25, 700, 7800, 25)
    #element.create_matrix_h_bc()
    #element.create_matrix_h()
    #element.create_matrix_h_with_bc()
  #  print(element.matrix_H)

   # print("===")

    mes_grid.create_global_matrix_h()
    mes_grid.create_global_matrix_c()
    print(mes_grid.global_matrix_c)
    #print(mes_grid.global_matrix_h)

    for element in mes_grid.elements:
        print(element.matrix_c)

    #  element.create_matrix_h_with_bc()
    #  print(element.matrix_H)

    #  element.create_matrix_h()
    #  element.create_matrix_c()
    #  element.create_matrix_h_bc()
    #  print(element.matrix_c)
    #  print(element.matrix_H)
    #  print(element.matrix_h_bc)





