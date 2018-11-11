class Node:
    def __init__(self, x_cord, y_cord, temp):
        self.x = x_cord
        self.y = y_cord
        self.ksi = -1
        self.eta = -1
        self.t = temp

    def __str__(self):
        info = "X: " + str(round(self.x, 4)) + " Y:" + str(round(self.y, 4)) + "\n"
        return info

    def print_transformed(self):
        print("Ksi: " + str(round(self.ksi, 6)) + " Eta:" + str(round(self.eta, 6)) + "\n")