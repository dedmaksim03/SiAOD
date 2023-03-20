import copy
import math


def print_matrix(matrix):
    for user_n in matrix:
        print(' '.join(list(map(str, user_n))))
    print(' ')


''' Сортировка выбором '''


# Сортировка выбором.
# Берётся срез массива, в котором минимальный элемент переносят в самый левый угол,
# после чего срез уменьшается и цикл повторяется.
def sort_choice(matrix_old):
    matrix = copy.deepcopy(matrix_old)
    for line in range(len(matrix)):  # Перебираем строки
        for column in range(len(matrix[line])):  # Перебираем столбцы
            min = matrix[line][column]
            min_coord = column
            for i in range(column, len(matrix[line])):  # Перебор строки - каждый раз перебираем с нового числа (+1)
                if matrix[line][i] < min:
                    min = matrix[line][i]
                    min_coord = i
            matrix[line][column], matrix[line][min_coord] = matrix[line][min_coord], matrix[line][column]


''' Сортировка вставкой '''


# Сортировка вставкой. Перебираем каждый элемент
# Отдельно выбранный элемент, перемещаем влево до тех пор, пока он не станет больше числа, которое находится левее него
def sort_put(matrix_old):
    matrix = copy.deepcopy(matrix_old)
    for line in range(len(matrix)):  # Перебираем строки
        for i in range(1, len(matrix[line])):  # Перебираем столбцы
            k = i
            while k > 0:
                if matrix[line][k] < matrix[line][k - 1]:
                    matrix[line][k], matrix[line][k - 1] = matrix[line][k - 1], matrix[line][k]
                else:
                    break
                k -= 1


''' Сортировка пузырьком '''


# Сортировка пузырьком
# Проходимся по массиву много раз, и, останавливаясь на числе, сравниваем его со следующим. Если надо меняем местами
def sort_bubble(matrix_old):
    matrix = copy.deepcopy(matrix_old)
    for line in range(len(matrix)):  # Перебираем строки
        while True:
            stop = True  # Проверка на то, есть ли неотсортированные числа
            for j in range(len(matrix[line]) - 1):
                if matrix[line][j] > matrix[line][j + 1]:
                    matrix[line][j], matrix[line][j + 1] = matrix[line][j + 1], matrix[line][j]
                    stop = False
            if stop:
                break


''' Быстрая сортировка '''


# Использует сортировку quick_sort
def sort_fast(matrix_old):
    # Разделяет массив на две части: одна больше числа pivot, другая - меньше
    # Возращает pivot, который является неким разделителем
    def partition(array, begin, end):
        pivot = begin  # Индекс вспомогательной точки
        for i in range(begin + 1, end + 1):
            if array[i] <= array[begin]:  # Сравнение с первым числом списка
                pivot += 1
                array[i], array[pivot] = array[pivot], array[i]
        array[pivot], array[begin] = array[begin], array[pivot]
        return pivot

    # Разделяет массив на две части с помощью вспомогательной функции partition
    # Рекурсивно вызывается для каждой новой половинки, тем самым сортируя весь массив
    def quick_sort(array, begin=0, end=None):
        if end is None:  # Первая инициализация end
            end = len(array) - 1

        def _quicksort(array, begin, end):
            if begin >= end:
                return
            pivot = partition(array, begin, end)
            _quicksort(array, begin, pivot - 1)  # Для левой части
            _quicksort(array, pivot + 1, end)  # Для правой части

        return _quicksort(array, begin, end)

    matrix = copy.deepcopy(matrix_old)
    for line in range(len(matrix)):  # Перебираем строки
        quick_sort(matrix[line])


'''Турнирная сортировка'''


def sort_tournament(matrix_old):
    # Получает минимальный элемент из кучи
    def get_min(heap: list):
        result = heap[0]
        heap[0] = heap[len(heap) - 1]  # На место убранного элемента ставим последний элемент
        heap.pop(len(heap) - 1)  # Удаление последнего элемента
        return result

    # Восстанавливает основное свойство кучи для дерева с корнем в i-ой вершине
    def heapify(i, heap: list):
        while True:
            left_child = 2 * i + 1  # Левая вершина
            right_child = 2 * i + 2  # Правая вершина
            smallest_child = i  # Наименьший элемент
            if left_child < len(heap):  # Проверка, чтобы не выйти за пределы массива
                if heap[left_child] < heap[smallest_child]:  # Если найден новый мин. элемент - меняем индекс
                    smallest_child = left_child
            if right_child < len(heap):
                if heap[right_child] < heap[smallest_child]:
                    smallest_child = right_child
            if smallest_child == i:  # Заканчиваем, когда меньшего элемента не нашлось
                break
            heap[i], heap[smallest_child] = heap[smallest_child], heap[i]  # Меняем местами прежний и нынешний мин. эл.
            i = smallest_child  # Новый индекс для нового минимального элемента

    matrix = copy.deepcopy(matrix_old)
    for line in range(len(matrix)):  # Перебираем строки
        heap = copy.deepcopy(matrix[line])  # Куча
        new_list = []  # Отсортированный массив
        for i in range(len(matrix[line]) // 2, -1, -1):  # Создаем кучу из всех элементов изначального массива
            heapify(i, heap)
        for i in range(0, len(heap) - 1):  # Проходимся количество раз, равное длине кучи
            new_list.append(get_min(heap))  # Добавляем минимальный элемент в массив с минимальными элементами
            heapify(0, heap)  # "Обновляем" кучу, начиная с первого элемента
        new_list.append(heap[0])
        matrix[line] = new_list


'''Сортировка Шелла'''


# Улучшенный вариант сортировки вставками
# Сравниваются не только элементы стоящие рядом, но и на определенном расстоянии
def sort_shell(matrix_old):
    matrix = copy.deepcopy(matrix_old)
    for line in range(len(matrix)):  # Перебираем строки
        n = len(matrix[line])  # Длина массива
        k = int(math.log2(n))  # Используется что бы вычислить интервал
        interval = 2 ** k - 1  # Интервал сравнения
        while interval > 0:  # Минимальное значение интервала: 1
            for i in range(interval, n):  # Перебираем массив, но не с начала, а с вычесленного интервала
                temp = matrix[line][i]  # Элемент, с которым будем сравнивать
                j = i
                while j >= interval and matrix[line][j - interval] > temp:
                    matrix[line][j] = matrix[line][j - interval]
                    j -= interval
                matrix[line][j] = temp
            k -= 1
            interval = 2 ** k - 1
