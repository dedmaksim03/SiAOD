import time


def deikstra(graph):
    paths = [[0, 0]] * len(graph)  # Список точек и путей
    process = []  # Список непосещенных точек
    done = [0]  # Список посещенных точек
    now = 0  # Точка, на которой мы сейчас находимся

    # Заполняем path, вставляем бесконечные пути во все точки кроме нулевой
    for i in range(1, len(graph)):
        paths[i] = [i, 2147483648]  # [прошлая точка; путь из прошлой точки в эту точку]

    # Добавляет в process точки, с которыми соединена node точка
    def append_nodes(node):
        for i in range(len(graph[node])):
            if graph[node][i] != 0 and done.count(i) == 0:
                process.append(i)

    append_nodes(0)  # Первая инициализация process: добавляем точки, с которыми соединена точка 0

    while process:  # Пока process не опустеет, гоняем наш алгоритм

        # Обновляем paths
        for i in process:  # Проходимся по всем точкам в process
            if graph[now][i] != 0:  # Если есть путь из now до этой точки
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
        print('paths: ', paths, '\n', 'process: ', process, 'min_node: ', min_node, '\n', 'done: ', done, '\n')


if __name__ == '__main__':
    graph = [
        [0, 3, 0, 0, 0, 0, 0],
        [0, 0, 5, 7, 0, 42, 0],
        [7, 0, 0, 0, 7, 0, 0],
        [0, 0, 1, 0, 0, 0, 0],
        [3, 0, 0, 11, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0],
    ]

    deikstra(graph)
