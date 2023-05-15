from collections import deque


# Находит из массива ребер такие, что треугольник из них имеет максимальный периметр
def triangle(mas):
    mas.sort()
    a, b, c = mas[-1], mas[-2], mas[-3]
    while mas:
        if b + c > a:
            return a + b + c
        elif len(mas) > 3:
            mas.pop()
            a, b, c = mas[-1], mas[-2], mas[-3]
        else:
            break
    return 0


def max_number_seq(mas: list):
    result = ""

    while len(mas) != 0:
        max_number = -1
        max_index = -1

        for index in range(len(mas)):
            number = mas[index] / 10 ** (len(str(mas[index])) - 1)

            if number > max_number or (number == max_number and len(str(mas[index])) < len(str(mas[max_index]))):
                max_number = number
                max_index = index

        result += str(mas[max_index])
        mas.pop(max_index)

    return result


def sort_diagonals_matrix(matrix):
    m = len(matrix)  # Строки
    n = len(matrix[0])  # Столбцы
    diagonals = n + m - 1  # Количество диагоналей
    i, j = m - 1, 0
    for diagonal in range(diagonals, 0, -1):
        for_sort = [matrix[i][j]]
        while i < m-1 and j < n-1:
            i += 1
            j += 1
            for_sort.append(matrix[i][j])

        for_sort.sort()

        while i >= 0 and j >= 0:
            matrix[i][j] = for_sort[-1]
            for_sort.pop()
            i -= 1
            j -= 1
        else:
            i += 1
            j += 1
        if i > 0:
            i, j = diagonal - m - 2, 0
        else:
            i, j = 0, n - diagonal + 1

    return matrix


if __name__ == '__main__':
    # print(triangle([3, 6, 2, 3]))
    # print(max_number_seq([3,30,34,5,9]))
    m1 = [[3, 3, 1, 1],
          [2, 2, 1, 2],
          [1, 1, 1, 2]]

    m2 = [[11, 25, 66, 1, 69, 7],
          [23, 55, 17, 45, 15, 52],
          [75, 31, 36, 44, 58, 8],
          [22, 27, 33, 25, 68, 4],
          [84, 28, 14, 11, 5, 50]]

    result = sort_diagonals_matrix(m2)
    for i in range(len(result)):
        print(result[i])
