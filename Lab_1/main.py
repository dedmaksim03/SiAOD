import random
import time
import sorts
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
import numpy as np


# Создает рандомную квадратную матрицу
# k - размер матрицы. pt - надо ли выводить ее
def make_matrix(k, pt=False):
    user_n = user_m = k
    user_min_limit, user_max_limit = 0, random.randint(1, 100)
    matrix = []
    for i in range(user_n):
        matrix.append([0] * user_m)
    for i in range(user_n):
        for j in range(user_m):
            matrix[i][j] = random.randint(user_min_limit, user_max_limit)
    if pt:
        sorts.print_matrix(matrix)
    return matrix


# Делает тест функций сортировок
def make_test(list_fun, start, stop, step, k_spline=1, big_test=False):
    stop = stop  # Конечная позиция
    k_spline = k_spline  # Коэффициент плавности графика (Нельзя делать очень большим)
    step = step  # Шаг в цикле
    for fun in list_fun:
        n = start  # Начальная позиция
        time_list = []  # Координата y
        n_list = []  # Координата x. Размер матрицы
        if big_test:
            if fun.__name__ == 'sort_put' or fun.__name__ == 'sort_bubble' or fun.__name__ == 'sort_choice':
                stop -= stop // 2
                k_spline = 2
                step = 50
        print(fun.__name__, ':', end=' ')
        while n <= stop:
            print(n, end=' ')
            start_time = time.time()
            fun(make_matrix(n))
            t = (time.time() - start_time) * 1000
            time_list.append(t)
            n_list.append(n)
            n += step
        print()
        x = np.array(n_list)  # Вспомогательные массивы
        y = np.array(time_list)
        x_new = np.linspace(x.min(), x.max(), 200)
        spl = make_interp_spline(x, y, k=k_spline)  # Вспомогательная функция для плавности графика
        y_smooth = spl(x_new)  # Переменная для плавности графика
        plt.plot(x_new, y_smooth, label=fun.__name__)  # Строим кривую (label - подпись где какая кривая)
        plt.legend(fontsize=6)  # Шрифт легенды
        plt.scatter(n_list, time_list)  # Сетка

    # Строим график
    plt.axis([0, stop + 50, 0, 17000])
    plt.grid()
    plt.show()


if __name__ == '__main__':
    list_fun = [
        sorts.sort_bubble,
        sorts.sort_choice,
        sorts.sort_put,
        sorts.sort_fast,
        sorts.sort_shell,
        sorts.sort_tournament
    ]
    make_test(list_fun,
              start=2,
              stop=452,
              step=50,
              k_spline=2,
              big_test=False)
