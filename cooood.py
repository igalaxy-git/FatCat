labyrint = [[0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1],
            [0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1],
            [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1],
            [0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1],
            [0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0],
            [0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]]

y_start, x_start = [int(i) for i in input().split()]
y_search, x_search = [int(i) for i in input().split()]


def search_path(data, x, y, short_path={}, full_path={}, count=0):
    full_path[(x, y)] = count
    if x == x_search and y == y_search:
        return full_path, short_path
    walks = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # up,left, down, right,
    for walk_X, walk_Y in walks:
        if data[x + walk_X][y + walk_Y] == 0 and (0 < x + walk_X < 11 and 0 < y + walk_Y < 11):  # Если ячейка свободна
            check = full_path.get((x + walk_X, y + walk_Y))  # Смотрим на точку, куда хотим пойти и сколько до неё шагов
            # Если check=None, значит в точке ещё не были
            if check != None and check > count:  # Если мы были уже в этой точке и расстояние до неё больше, чем номер шага
                # на данном этапе
                full_path[
                    (x + walk_X, y + walk_Y)] = count  # Перезаписываем full_path, т.к нашли более короткую дистанцию
                short_path[(x + walk_X, y + walk_Y)] = (x, y)  # Пепрезаписываем short_path, потому что нашли точку, из
                # которой в данную можно попасть короче
                search_path(data, x + walk_X, y + walk_Y, short_path, full_path,
                            count + 1)  # Увеличиваем шаг и запускаем
                # рекурсивно функцию
            else:
                if (x + walk_X, y + walk_Y) not in full_path.keys():  # Если в точке, куда собираемся пойти еще не были
                    short_path[(x + walk_X, y + walk_Y)] = (x, y)  # записываем {куда идём:откуда идём}
                    search_path(data, x + walk_X, y + walk_Y, short_path, full_path, count + 1)  # запускаем рекурсию
                    # с шагом +1
    return full_path, short_path


def short_path(data, path=[], start=(x_start, y_start), end=(x_search, y_search)):  # Сюда прилетает short_path из search_path, когда нашли выход
    # data=short_path, start - координата точки входа, end - выхода
    # path - короткий путь в виде списка координат из лабиринта
    """Здесь мы рекурсивно пробегаемся из конечной точки в начальную, восстанавливая путь по лабиринту:
    берём {точка, куда пришли(допустим А) : точка откуда пришли (в точку А) - Б}"""
    print(11)
    print(data, path, start, end)
    if len(path) == 0:
        path.append(end)
    path.append(data[end])
    if data[end] == start:
        return path
    else:
        short_path(data, path, start, data[end])
    return path


p = search_path(labyrint, x_start, y_start)
print(p)
print(p[1])
print(short_path(p[1]))
if p is None:
    print('No Exit!!!')
else:
    short = short_path(p[1])
    short.reverse()
    print(short)
    for walk in short:
        labyrint[walk[0]][walk[1]] = 3  # Здесь мы просто указываем в графе путь к выходу цифрой 3
    for see in labyrint:
        print(see)
