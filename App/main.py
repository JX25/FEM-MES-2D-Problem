from App.grid import Grid
from App.element import Element
from App.node import Node

if __name__ == '__main__':
    mes_grid = Grid()
    #mes_grid.solve()
    #mes_grid.print_elements()

#    mes_grid.create_global_matrix_h_bc()
#    for el in mes_grid.elements:
#        print(el.matrix_h_bc)
    mes_grid.solve()

    #print(mes_grid.global_matrix_h)

    #for element in mes_grid.elements:
     #   print(element.vector_p)

    #  element.create_matrix_h_with_bc()
    #  print(element.matrix_H)

    #  element.create_matrix_h()
    #  element.create_matrix_c()
    #  element.create_matrix_h_bc()
    #  print(element.matrix_c)
    #  print(element.matrix_H)
    #  print(element.matrix_h_bc)





