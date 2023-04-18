class Desk:

    def __init__(self, commit_desk, queens, field, now):
        self.commit_desk = commit_desk
        self.queens = queens
        self.length = 64
        self.field = field
        self.now = now

    def refresh(self, index):
        step = 1
        stop_list = [1]*8
        while stop_list.__contains__(1):
            if (index-step) % 8 < 7 and stop_list[0] == 1:  # По горизонтали влево
                self.field[index - step] = Cell(2)
            else:
                stop_list[0] = 0
            if (index+step) % 8 > 0 and stop_list[1] == 1:  # По горизонтали вправо
                self.field[index + step] = Cell(2)
            else:
                stop_list[1] = 0
            if index-step*8 > 0 and stop_list[2] == 1:  # По вертикали вверх
                self.field[index - step * 8] = Cell(2)
            else:
                stop_list[2] = 0
            if index+step*8 < self.length and stop_list[3] == 1:  # По вертикали вниз
                self.field[index + step * 8] = Cell(2)
            else:
                stop_list[3] = 0
            if (index-step*7) % 8 > 0 and index-step*7 > 0 and stop_list[4] == 1:  # По диагонали вправо-вверх
                self.field[index - step * 7] = Cell(2)
            else:
                stop_list[4] = 0
            if (index+step*7) % 8 < 7 and index + step * 7 < len(self.field) and stop_list[5] == 1:  # По диагонали влево-вниз
                self.field[index + step * 7] = Cell(2)
            else:
                stop_list[5] = 0
            if index+step*9 < self.length and (index+step*9) % 8 > 0 and stop_list[6] == 1:  # По диагонали вправо-вниз
                self.field[index + step * 9] = Cell(2)
            else:
                stop_list[6] = 0
            if index-step*9 >= 0 and (index-step*9) % 8 < 7 and stop_list[7] == 1:  # По диагонали влево-вверх
                self.field[index - step * 9] = Cell(2)
            else:
                stop_list[7] = 0

            step += 1

    def print_desk(self):
        for i in range(8):
            print("")
            for j in range(8):
                if self.field[j + i * 8].get_value() == 2:
                    print(".", end="  ")
                else:
                    print(1, end="  ")


class Cell:

    def __init__(self, value=0):
        self.value = value  # Значение клетки: 1 - королева, 2 - под боем, 0 - пустая

    def get_value(self):
        return self.value
