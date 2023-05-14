import csv
import random
import pandas
import copy
from Lab_4.maps.map_rehash import MapReHash


def quick_sort(mas, left, right=None):
    if right is None:
        right = len(mas)-1
    # Критерий для остановки рекурсии.
    if left >= right:
        return
    # Индекс начала.
    i = left
    # Индекс конца.
    j = right
    # Опорный элемент. Индексы начала и конца будут идти до него.
    pivot = mas[random.randint(left, right)]

    # Ищем числа, стоящие не на своём месте. Меняем их, сместив индексы.
    while i <= j:
        while mas[i] < pivot: i += 1
        while mas[j] > pivot: j -= 1

        if i <= j:
            mas[j], mas[i] = mas[i], mas[j]
            i += 1
            j -= 1

    # Выполняем те же операции, только с уменьшенным массивом. Идём с начала до j.
    quick_sort(mas, left, j)
    # Выполняем те же операции, только с уменьшенным массивом. Идём с i до конца.
    quick_sort(mas, i, right)

    return mas


def sum_revenue():
    all_sum = 0
    for i in range(len(revenue)-1):
        all_sum += revenue[i]
    return all_sum


if __name__ == '__main__':
    strings = []  # Хранит все строки исходного файла
    revenue = []  # Хранит общую выручку товаров
    sale_count = []  # Хранит количество продаж товаров

    goods = ['Магазин']  # Хранит названия товаров

    with open("table.csv", encoding='utf-8', newline='') as r_file:
        # Создаем объект DictReader, указываем символ-разделитель ";"
        file_reader = csv.DictReader(r_file, delimiter=";")
        support_reader = list(file_reader)

        find_revenue = MapReHash(len(support_reader)-1)  # Классы для поиска максимального значения в массиве
        find_sale_count = MapReHash(len(support_reader)-1)

        for row in support_reader:
            strings.append(row)
            revenue.append(int(row["Общая стоимость"]))
            sale_count.append(int(row["Количество продаж"]))
            find_revenue.put(row["Название товара"], int(row["Общая стоимость"]))
            find_sale_count.put(row["Название товара"], int(row["Количество продаж"]))

            goods.append(row["Название товара"])

    all_sum_revenue = sum_revenue()
    print("Общая выручка: ", all_sum_revenue, "\n")
    max1 = quick_sort(copy.deepcopy(revenue), 0)
    print("Отсортированный массив выручки: ", max1)
    print("Самый прибыльный товар: ", find_revenue.get(max1[-1]), ' - ', max1[-1], "\n")

    max2 = quick_sort(copy.deepcopy(sale_count), 0)
    print("Отсортированный массив количества продаж: ", max2)
    print("Самый продаваемый товар: ", end='')
    print(find_sale_count.get(max2[-1], with_delete=True), ' - ', max2[-1], end="")
    while find_sale_count.get(max2[-1]) is not None:
        print(", ", find_sale_count.get(max2[-1], with_delete=True), ' - ', max2[-1], end="")
    else:
        print("\n")

    part_of_all = []
    for i in range(len(revenue)):
        part_of_all.append(revenue[i]/all_sum_revenue)
    revenue.insert(0, '-')
    sale_count.insert(0, '-')
    part_of_all.insert(0, '-')

    data = {
        "Название товара": goods,
        "Общая выручка": revenue,
        "Количество ": sale_count,
        "Доля ": part_of_all
    }
    pandas.set_option('display.width', 1000)
    pandas.set_option('display.max_columns', None)
    df = pandas.DataFrame(data)
    print(df)
