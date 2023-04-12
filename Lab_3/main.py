import time
import io

import pandas as pd
from pyvis.network import Network
import networkx as nx
import copy
from Lab_2.deque import Deque
from collections import deque
import random


def find_min_paths(path, only_path=False):
    min_path = [len(path) - 1]
    while min_path[0] != 0:
        min_path.insert(0, path[min_path[0]][0])
    if only_path:
        return min_path
    return [min_path, path[-1][1]]


def make_matrix_with_inf(graph):
    mas = copy.deepcopy(graph)  # Массив с длинами путей, будем менять значения в ходе алгоритма
    for i in range(len(mas)):  # Заменяем нули бесконечностью
        for j in range(len(mas)):
            if (i != j) and (mas[i][j] == 0):
                mas[i][j] = float('inf')
    return mas


def deikstra(input_graph):
    """Работает быстрее обычного перебора, но не работает с отрицательными весами"""
    graph = copy.deepcopy(input_graph)
    paths = [[0, 0]] * len(graph)  # Список точек и путей
    process = []  # Список не посещенных точек
    done = [0]  # Список посещенных точек
    now = 0  # Точка, на которой мы сейчас находимся

    # Заполняем path, вставляем бесконечные пути во все точки кроме нулевой
    for i in range(1, len(graph)):
        paths[i] = [i, float('inf')]  # [прошлая точка; путь из прошлой точки в эту точку]

    # Добавляет в process точки, с которыми соединена node точка
    def append_nodes(node):
        for i in range(len(graph[node])):
            # Если есть путь от node до точки и если в done и process нет этой точки
            if graph[node][i] != float('inf') and done.count(i) == 0 and process.count(i) == 0:
                process.append(i)

    append_nodes(0)  # Первая инициализация process: добавляем точки, с которыми соединена точка 0

    while process:  # Пока process не опустеет, гоняем наш алгоритм

        # Обновляем paths
        for i in process:  # Проходимся по всем точкам в process
            if graph[now][i] != float('inf'):  # Если есть путь из now до этой точки
                if paths[now][1]+graph[now][i] < paths[i][1]:  # Если путь из now к этой точке короче чем было
                    paths[i][1] = paths[now][1] + graph[now][i]  # То обновляем
                    paths[i][0] = now

        min_path = paths[process[0]][1]  # Минимальный путь от now до следующей точки
        min_node = process[0]  # Точка, до которой идет минимальный путь

        # Проходимся по точкам в process и находим точку с минимальным путем до нее
        for i in process:
            if paths[i][1] < min_path:
                min_path = paths[i][1]
                min_node = i

        done.append(min_node)  # Добавляем минимальную точку в список посещенных точек
        process.remove(min_node)  # Удаляем минимальную точку из process
        append_nodes(min_node)  # Обновляем список process
        now = min_node  # Переходим в новую точку

    return paths


def floyd_warshell(input_graph):
    """ Фишка: находит общее решение, т. е. расстояния до всех вершнин от всех вершин"""
    graph = copy.deepcopy(input_graph)  # Массив, показывающий расстояния
    paths = [[0 for j in range(len(graph))] for i in range(len(graph))]  # Массив, показывающий пути

    for k in range(len(graph)):  # Итерациями проходимся по массиву
        for i in range(len(graph)):
            for j in range(len(graph)):
                if graph[i][k] + graph[k][j] < graph[i][j]:
                    graph[i][j] = graph[i][k] + graph[k][j]  # Обновление массива длин путей
                    paths[i][j] = k  # Обновление массива путей

    output_paths = [[0, 0]] * len(graph)  # Для вывода путей из всех точек в 0
    for i in range(len(graph)):
        output_paths[i] = [paths[0][i], graph[0][i]]
    return output_paths


def bellman_ford(input_graph):
    """Фишка: может работать с отрицательными весами"""
    graph = copy.deepcopy(input_graph)
    paths = [[0, float('inf')]] * len(graph)  # [предыдущая точка, расстояние от предыдущей точки до этой]
    paths[0] = [0, 0]

    for k in range(1, len(graph)):
        for i in range(len(graph)):
            for j in range(len(graph)):
                if paths[j][1] > paths[i][1] + graph[i][j]:
                    paths[j] = [i, paths[i][1] + graph[i][j]]
                if paths[j][1] > paths[i][1] + graph[i][j]:
                    print("Ошибка")
                    break

    return paths


def johnson(input_graph):
    """ Убирает из графа отрицательные веса, а затем запускает алгоритм Дейкстры"""
    graph = copy.deepcopy(input_graph)

    # Добавляем дополнительную точку, соединенную с другими точками путем 0
    graph.insert(0, [0] * (len(input_graph) + 1))
    for i in range(1, len(graph)):  # Добавляем в каждую точку столбец с бесконечным путем
        graph[i].insert(0, float('inf'))

    paths = bellman_ford(graph)  # Ищем все пути от дополнительной точки до всех остальных точек
    paths.pop(0)  # Удаляем из списка путей нашу точку

    graph = make_matrix_with_inf(input_graph)  # Пересоздадим graph, чтобы избавиться от дополнительной точки

    for i in range(len(graph)):
        for j in range(len(graph)):
            graph[i][j] = graph[i][j] + paths[i][1] - paths[j][1]  # Обновим пути в соответствии с формулой

    return deikstra(graph)  # Запускаем дейкстру с массивом без отрицательных путей


def levite(graph):
    """Фишка: работает с отрицательными весами, реализуя собственный алгоритм (без Дейкстры)"""
    dist = [float('inf')]*len(graph)  # Хранит расстояния
    dist[0] = 0
    paths = [0]*len(graph)  # Хранит маршруты
    m_0 = []  # Вершины, расстояние до которых уже вычислено (но, возможно, не окончательно)
    m_1 = Deque()  # Вершины, расстояние до которых вычисляется
    m_1.add_left(0)
    m_2 = [i for i in range(1, len(graph))]  # Вершины, расстояние до которых ещё не вычислено

    while not m_1.is_empty():  # Пока есть вычисляемые точки
        v = m_1.remove_left()  # Выбираем первую в очереди точку из списка вычисляемых точек
        m_0.append(v)

        for i in range(len(graph)):  # Проходимся по вершинам графа
            if graph[v][i] != float('inf') and v != i:  # Находим вершины, с которыми соединена v
                t, l = i, graph[v][i]  # t - вершина, с которой соединена v, l - путь до нее
                # Рассмотрим три случая
                if t in m_2:  # Если t еще не вычислена
                    m_1.add_right(t)  # то добавляем в очередь вычисляемых
                    m_2.remove(t)
                    dist[t] = dist[v] + l  # Вычисляем путь
                    paths[t] = v
                elif m_1.has(t):  # Если t уже в очереди вычисляемых
                    if dist[t] > dist[v] + l:  # То при необходимости обновляем путь до нее
                        dist[t] = dist[v] + l
                        paths[t] = v
                elif t in m_0 and dist[t]>dist[v]+l:  # Если t в списке уже вычисленных, но есть более оптимальный путь
                    dist[t] = dist[v]+l  # Обновляем путь у t
                    paths[t] = v
                    m_1.add_left(t)  # Добавляем ее в список выполняемых точек
                    m_0.remove(t)

    new_paths = []
    for i in range(len(dist)):  # Приводим результат к стандарту
        new_paths.append([paths[i], dist[i]])
    return new_paths


# Надо переделать
# Нужно фиксировать пройденный путь, проверять, есь ли еще пути и, если что, делать break
def yen(input_graph, k=2):
    """ Фишка: находит сразу несколько оптимальных путей по возрастанию длины"""

    graph = copy.deepcopy(input_graph)  # Создаем копию графа, чтобы первоначальный не повредить
    min_paths = [find_min_paths(deikstra(graph))]  # Итоговый список минимальных путей
    canditate = []  # Список кандидатов на следующий минимальный путь
    possible_paths = []  # Список точек, которые ведут в последнюю точку
    for i in range(len(graph)):
        if graph[i][len(graph)-1] != float('inf') and graph[i][len(graph)-1] != 0:
            possible_paths.append(i)

    for way in range(1, k):  # Каждый новый цикл - новый минимальный путь
        min_len = float('inf')  # Вспомогательные переменные для определения минимального пути
        min_p = []  # Маршрут, который занесем в итоговый список минимальных путей

        graph = copy.deepcopy(input_graph)
        possible_p = copy.deepcopy(possible_paths)

        for i in range(len(min_paths[0][0])-1):
            for t in range(len(min_paths)):
                if len(min_paths[t][0]) > i+1:
                    # Убираем следующее ребро в маршруте
                    graph[min_paths[t][0][i]][min_paths[t][0][i + 1]] = float('inf')
                    if min_paths[t][0][i + 1] == len(graph)-1 and min_paths[t][0][i] in possible_p:
                        possible_p.remove(min_paths[t][0][i])
            if possible_p:
                mp = find_min_paths(deikstra(graph))  # Новый путь с убранным ребром
            else:
                break
            if mp not in canditate:
                canditate.append(mp)
            if mp[1] < min_len:
                min_len = mp[1]
                min_p = mp
            for j in range(len(graph)):  # Уберем все возможные пути назад, чтобы алгоритм не возвращался
                graph[j][0] = float('inf')
            for t in range(len(min_paths)):  # Возвращаем убранные ребра
                if len(min_paths[t][0]) > i+2:
                    graph[min_paths[t][0][i]][min_paths[t][0][i + 1]] = \
                        input_graph[min_paths[t][0][i]][min_paths[t][0][i + 1]]

        min_paths.append(min_p)  # Добавляем новый минимальный путь в итоговый список
        canditate.remove(min_p)
    return min_paths[k-1]


def visualize_network(graph, paths, yen):
    g = nx.DiGraph()
    nt = Network(notebook=True, directed=True)
    min_path = []
    if yen:
        min_path = paths
    else:
        min_path = find_min_paths(paths, only_path=True)

    # Заполняем граф
    for i in range(len(graph)):
        g.add_node(i, label=f"Node {i}")
    for i in range(len(graph)):
        for j in range(len(graph)):
            if graph[i][j] != 0 and graph[i][j] != float('inf'):
                g.add_edge(i, j)

    # Обрисовываем путь
    for i in range(len(min_path)-1):
        g[min_path[i]][min_path[i+1]]['color'] = "red"

    nt.from_nx(g)  # Передаем наш граф для визуализации
    nt.show_buttons(filter_=['physics'])  # Отключается гравитация-физика
    nt.write_html("basic.html", open_browser=True)


def make_test(algorithm, graph):
    copy_graph = copy.deepcopy(graph)  # Создаем копию графа, чтобы первоначальный не повредить
    start = time.time()
    algorithm(copy_graph)
    result = (time.time() - start) * 1000

    return result


def get_graph(name_file):
    file = io.open(name_file, encoding='utf-8')
    graphs_string = file.read().split('\n\n')
    graphs = []
    for graph_string in graphs_string:
        graph = []
        string_of_graph = []
        number = ''
        for i in range(1, len(graph_string)):
            if graph_string[i].isdigit():
                number += graph_string[i]
            elif number != '':
                string_of_graph.append(int(number))
                number = ''
                if graph_string[i] == ']':
                    graph.append(string_of_graph)
                    string_of_graph = []
        graphs.append(make_matrix_with_inf(graph))


    '''for i in range(len(graphs)):
        print('\n')
        for j in range(len(graphs[i])):
            print(graphs[i][j])'''

    return graphs


def generate_adjacency_matrix(num_nodes, chance_of_edge):
    # Создаем пустую матрицу смежности.
    matrix = [[0] * num_nodes for _ in range(num_nodes)]
    # Создаем список, чтобы отслеживать посещенные узлы при поиске в ширину.
    visited = [False] * num_nodes

    # Создаем список ребер.
    edges = []
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            # Генерируем случайное число и, если оно меньше или равно
            # заданному шансу на создание ребра, добавляем ребро в список.
            if random.randint(1, 100) <= chance_of_edge:
                weight = random.randint(1, 10)
                edges.append((i, j, weight))

    # Добавляем новые ребра, чтобы связать несвязанные узлы.
    def bfs(start):
        # Помечаем начальный узел как посещенный и добавляем его в очередь.
        visited[start] = True
        q = deque([start])
        while q:
            # Извлекаем узел из очереди и ищем его непосещенных соседей.
            node = q.popleft()
            for neighbor in range(num_nodes):
                if not visited[neighbor] and matrix[node][neighbor] != 0:
                    # Если сосед еще не посещен и между узлами есть ребро,
                    # помечаем его как посещенный и добавляем в очередь.
                    visited[neighbor] = True
                    q.append(neighbor)

    # Запускаем поиск в ширину из первого узла.
    bfs(0)
    # Если есть непосещенные узлы, значит, граф не связный.
    for i in range(num_nodes):
        if not visited[i]:
            # Выбираем случайный узел из несвязанной компоненты и
            # связываем его со случайным узлом из связанной компоненты.
            j = random.randint(0, i - 1)
            weight = random.randint(1, 10)
            matrix[i][j] = matrix[j][i] = weight

    # Заполняем матрицу смежности существующими ребрами.
    for edge in edges:
        matrix[edge[0]][edge[1]] = edge[2]

    # Возвращаем готовую матрицу смежности.
    return make_matrix_with_inf(matrix)


if __name__ == '__main__':
    results_floyd_warshall = []
    results_dijkstra = []
    bellman_ford_results = []
    results_johnson = []
    results_levit = []
    results_yen_k_shortest_paths = []

    graphs = get_graph('graphs.txt')
    # print(len(graphs))
    for i in [30, 50, 90, 100, 120, 150]:
        results_dijkstra.append(make_test(deikstra, generate_adjacency_matrix(i, 50)))
        results_floyd_warshall.append(make_test(floyd_warshell, generate_adjacency_matrix(i, 50)))
        bellman_ford_results.append(make_test(bellman_ford, generate_adjacency_matrix(i, 50)))
        results_johnson.append(make_test(johnson, generate_adjacency_matrix(i, 50)))
        results_levit.append(make_test(levite, generate_adjacency_matrix(i, 50)))
        results_yen_k_shortest_paths.append(make_test(yen, generate_adjacency_matrix(i, 50)))

    # make_test(lm, get_graph('graphs.txt'))
    # создаем таблицу с названием и сложностью каждого алгоритма
    data = {
        "Узлов": [30, 50, 90, 100, 120, 150],
        "Флойда-Уоршелла": results_floyd_warshall,
        "Дейкстры": results_dijkstra,
        "Беллмана-Форда": bellman_ford_results,
        "Джонсона": results_johnson,
        "Левита": results_levit,
        "Йена": results_yen_k_shortest_paths
    }
    pd.set_option('display.width', 1000)
    df = pd.DataFrame(data)

    # выводим таблицу
    print(df)

    # graph = get_graph('graphs.txt')[0]
    # make_matrix_with_inf(graph)
    # visualize_network(graph, deikstra(graph))




