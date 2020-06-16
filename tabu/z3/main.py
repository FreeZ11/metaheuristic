import sys
import time
from numpy.random import randint


def first_case(board, starting_point):   # funkcja sluzaca do stworzenia pierwszego rozwiazania
    path = []
    agent = starting_point
    exit = 1

    last_move = ""
    while exit != 8:   # pierwsze rozwiazanie wyglada tak ze caly czas ide w jedna strone dopuki nie spotkam przeszkody

        if board[agent[0] - 1][agent[1]] == '8':
            path.append('U')
            exit = 8

        elif board[agent[0]][agent[1] + 1] == '8':
            path.append('R')
            exit = 8

        elif board[agent[0]][agent[1] - 1] == '8':
            path.append('L')
            exit = 8

        elif board[agent[0] + 1][agent[1]] == '8':
            path.append('D')
            exit = 8

        elif board[agent[0] - 1][agent[1]] == '0' and last_move != 'D':
            path.append('U')
            last_move = 'U'
            agent = [agent[0] - 1, agent[1]]

        elif board[agent[0]][agent[1] + 1] == '0' and last_move != 'L':
            path.append('R')
            last_move = 'R'
            agent = [agent[0], agent[1] + 1]

        elif board[agent[0] + 1][agent[1]] == '0' and last_move != 'U':
            path.append('D')
            last_move = 'D'
            agent = [agent[0] + 1, agent[1]]

        elif board[agent[0]][agent[1] - 1] == '0' and last_move != 'R':
            path.append('L')
            last_move = 'L'
            agent = [agent[0], agent[1] - 1]

    return path


def path_checker(board, path, starting_position):   #funkcja ktora sprawdza czy dana sciezka dala nam chciany rezultat czyli wyjscie
    x = starting_position[0]
    y = starting_position[1]
    finish_flag = False
    length = 0
    board_copy = board.copy()

    for i in range(len(path)):
        length += 1

        if path[i] == 'U':
            x -= 1

        elif path[i] == 'D':
            x += 1

        elif path[i] == 'R':
            y += 1

        elif path[i] == 'L':
            y -= 1

        if board_copy[x][y] == '8':
            finish_flag = True
            break

        if board_copy[x][y] == '1':
            break

    return [finish_flag, length]


def swap(path, tabu):
    path_copy = path.copy()
    result = []
    counter = 0

    for i in range(len(path)):

        for j in range(i + 1, len(path)):

            if counter > len(tabu):
                break

            else:
                new_i = randint(i, len(path))
                new_j = randint(j, len(path))
                path_copy[new_i], path_copy[new_j] = path_copy[new_j], path_copy[new_i]

                if path_copy not in tabu:
                    counter += 1
                    result.append(path_copy)

    return result


def tabu_search(board, m, n, starting_position, given_time): #implementacja tabu search dla zadanego problemu
    tabu = []
    tabu_limit = len(board) // 2
    road = first_case(board, starting_position)
    tabu.append(road)

    remining_time = 0
    clk_start = time.process_time()

    while remining_time < given_time:
        neighbour = swap(road, tabu)
        print(tabu)

        for el in neighbour:
            helper = path_checker(board, el, starting_position)

            if helper[0]:
                if helper[1] < len(road):
                    road = el[:helper[1]]

                    if len(tabu) >= tabu_limit:
                        tabu.pop(0)

                    tabu.append(road)

        clk_tick = time.process_time()
        remining_time = clk_tick - clk_start

    return road


my_args = sys.stdin.readline()
my_args = my_args.split()
timezz = int(my_args[0])
n = int(my_args[1])
m = int(my_args[2])
board = []
starting_point = []

for line in sys.stdin:
    board.append(line.rstrip())
for row in board:
    if '5' in row:
        starting_point = [board.index(row), row.find('5')]

road = tabu_search(board, m, n, starting_point, timezz)
length = len(road)

print("road: ", road)
print("length: ", length)

