import random
import time
import pandas as pd
from binary_tree import BinarySearchTree
from Lab_4.maps.map_rehash import MapReHash
from Lab_4.maps.map_chain import MapChain


def get_random_seq(lenght, n):  # Рандомная последовательность длины length и числами от 0 до n
    seq = []
    for i in range(lenght):
        seq.append(random.randint(0, n))
    return seq


def python_find(mas: list, number):
    return mas.index(number)


def binary_find(mas, number):
    left, right = 0, len(mas)-1  # Указатели границ, внутри которых мы смотрим средний элемент
    while right >= left:
        middle = left + (right-left) // 2  # Находим середину в промежутке между left и right
        if mas[middle] == number:
            return middle
        elif mas[middle] < number:
            if left != middle:  # Добавочное условие для нахождения крайних элементов
                left = middle
            else:
                left += 1
        elif mas[middle] > number:
            if right != middle:
                right = middle
            else:
                right -= 1
    return None


def interpolating_find(mas, number):
    left, right = 0, len(mas) - 1  # Указатели границ, внутри которых мы смотрим средний элемент
    while mas[left] < number < mas[right]:
        middle = left + (number - mas[left])*(right-left)//(mas[right]-mas[left])  # Находим новую точку сравнения
        if mas[middle] == number:
            return middle
        elif mas[middle] < number:
            left = middle + 1
        elif mas[middle] > number:
            right = middle - 1
    if mas[left] == number:
        return left
    elif mas[right] == number:
        return right
    return None


def fibonacci(n):
    fib_seq = [1, 1]
    while len(fib_seq) < n:
        fib_seq.append(fib_seq[-1] + fib_seq[-2])
    return fib_seq


def fibonacci_find(mas, number, fib_seq):
    fib_m = fib_seq[-1]  # Крайний правый член Фибоначчи
    fib_m_1 = fib_seq[-2]  # Первый влево
    fib_m_2 = fib_seq[-3]  # Второй влево
    index = -1  # Левый край блока, где мы ищем number
    while fib_m > 1:
        i = min(index + fib_m_2, (len(mas) - 1))  # Находим предполагаемый индекс
        if mas[i] < number:  # Если элемент по нему меньше чем number
            fib_m = fib_m_1  # То смещаем крайний правый член Фибоначчи на 1 влево
            fib_m_1 = fib_m_2
            fib_m_2 = fib_m - fib_m_1
            index = i  # Перемещаем индекс (По факту двигаем его вправо)
        elif mas[i] > number:  # Если элемент больше чем number
            fib_m = fib_m_2  # То сдвигаем числа Фибоначчи вправо на 2 (По факту двигаем правую границу)
            fib_m_1 = fib_m_1 - fib_m_2
            fib_m_2 = fib_m - fib_m_1
        else:
            return i
    if fib_m_1 and index < (len(mas) - 1) and mas[index + 1] == number:
        return index + 1
    return None


def make_test(list_fun, list_classes):
    size_mas = [100, 200, 300, 400]  # Набор длин массивов для теста
    s = get_random_seq(size_mas[-1], 10000)  # Генерируем одну длинную последовательность для дальнейшего использования
    s.sort()  # Сортируем
    results = {}  # Список результатов тестирования для вывода

    for fun in list_fun:  # Проходимся по всем функциям поиска
        results[fun] = []  # Для конкретной функции создаем список ее результатов
        for i in size_mas:  # Будем менять длину тестируемой последовательности
            new_s = s[:i]  # Берем кусок нужной длины, из нашей начальной длинной последовательности
            find = random.randint(0, len(new_s) - 1)  # Индекс для поиска (можно поставить любую цифру < len(new_s)

            if fun == fibonacci_find:  # Отдельно тестируем фибоначчи
                fib_seq = fibonacci(len(new_s))  # Делаем предврарительную последовательность фибоначчи
                start = time.time()
                for j in range(10000):  # Вызываем много раз функцию (иначе результат 0, сильно быстро работают)
                    fun(new_s, new_s[find], fib_seq)
                results[fun].append((time.time() - start) * 1000)  # Записываем результат
            else:
                start = time.time()
                for j in range(10000):
                    fun(new_s, new_s[find])
                results[fun].append((time.time() - start) * 1000)

    for cls in list_classes:  # Проходимся по всем классам для поиска, и проделываем то же самое, что и выше
        results[cls] = []
        for i in size_mas:
            new_s = s[:i]
            find = random.randint(0, len(new_s) - 1)

            if cls == BinarySearchTree:  # Отдельно сделаем для бинарного дерева из-за косяка
                ex_cls = cls()
                for i in range(len(new_s)):
                    ex_cls.put(new_s[i], i)  # Косяк в этом: вставка происходит фактически (val, key), а не (key, val)
            else:
                ex_cls = cls(len(new_s))
                for i in range(len(new_s)):
                    ex_cls.put(i, new_s[i])
            start = time.time()
            for j in range(10000):
                ex_cls.get(new_s[find])
            results[cls].append((time.time() - start) * 1000)

    # создаем таблицу с названием и сложностью каждого алгоритма
    data = {
        "Размер": size_mas,
        "Python поиск": results[python_find],
        "Бинарный поиск": results[binary_find],
        "Интерполяционный поиск": results[interpolating_find],
        "Фибоначчиев поиск": results[fibonacci_find],
        "Бинарное дерево": results[BinarySearchTree],
        "Рехэширование": results[MapReHash],
        "Метод цепочек": results[MapChain]
    }
    pd.set_option('display.width', 10000)
    # Сброс ограничений на число столбцов
    pd.set_option('display.max_columns', None)
    df = pd.DataFrame(data)

    # выводим таблицу
    print(df)


if __name__ == '__main__':
    list_fun = [
        python_find,
        binary_find,
        interpolating_find,
        fibonacci_find
    ]
    list_cls = [
        BinarySearchTree,
        MapChain,
        MapReHash
    ]

    make_test(list_fun, list_cls)



