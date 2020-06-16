import sys
import time
import numpy as np



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

    return [finish_flag, length, path]


def geneticAlgorithm(board, m, n, starting_position, roads, given_time, max_population):
    

    paths = roads.copy()
    remining_time = 0
    directions = {0:'U',1:'D',2:'L',3:'R'}
    clk_start = time.process_time()
    new_paths = []
    shortest_path ='D'*1000

    while remining_time < given_time:
        

        for path in paths:

            new_path = path
            index = np.random.randint(0, len(path)-1)
            new_path = new_path[:index] + new_path[index+1:]
            
                

            if np.random.random_sample() < 0.4:
                index = np.random.randint(0,len(path)-1)
                curr = path[index]
                
                mutation = curr
                while mutation == curr:
                    mutation = directions[np.random.randint(0,4)]
               
                new_path = new_path[:index] + mutation + new_path[index+1:]
                
                    

            result = path_checker(board,new_path,starting_position)
            if result[0] == True:
                if new_path not in paths and len(new_path) < len(shortest_path):
                    paths.append(new_path)
                    shortest_path = new_path


        clk_tick = time.process_time()
        remining_time = clk_tick - clk_start

    print(len(paths))
    print(paths)    
    return min(paths, key=len)


def ReadLines(n):
    return [sys.stdin.readline().strip() for _ in range(n)]

my_args = sys.stdin.readline()
my_args = my_args.split()
timezz = int(my_args[0])
n = int(my_args[1])
m = int(my_args[2])
solutions = int(my_args[3])
max_population = int(my_args[4])
board = ReadLines(n)
roads = ReadLines(solutions)
starting_point = []

for row in board:
    if '5' in row:
        starting_point = [board.index(row), row.find('5')]
res = geneticAlgorithm(board,m,n,starting_point,roads,timezz, max_population)
print("trasa: ", res)
print("długość: ", len(res))import sys
import time
import numpy as np



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

    return [finish_flag, length, path]


def geneticAlgorithm(board, m, n, starting_position, roads, given_time, max_population):
    

    paths = roads.copy()
    remining_time = 0
    directions = {0:'U',1:'D',2:'L',3:'R'}
    clk_start = time.process_time()
    new_paths = []
    shortest_path ='D'*1000

    while remining_time < given_time:
        

        for path in paths:

            new_path = path
            index = np.random.randint(0, len(path)-1)
            new_path = new_path[:index] + new_path[index+1:]
            
                

            if np.random.random_sample() < 0.4:
                index = np.random.randint(0,len(path)-1)
                curr = path[index]
                
                mutation = curr
                while mutation == curr:
                    mutation = directions[np.random.randint(0,4)]
               
                new_path = new_path[:index] + mutation + new_path[index+1:]
                
                    

            result = path_checker(board,new_path,starting_position)
            if result[0] == True:
                if new_path not in paths and len(new_path) < len(shortest_path):
                    paths.append(new_path)
                    shortest_path = new_path


        clk_tick = time.process_time()
        remining_time = clk_tick - clk_start

    print(len(paths))
    print(paths)    
    return min(paths, key=len)


def ReadLines(n):
    return [sys.stdin.readline().strip() for _ in range(n)]

my_args = sys.stdin.readline()
my_args = my_args.split()
timezz = int(my_args[0])
n = int(my_args[1])
m = int(my_args[2])
solutions = int(my_args[3])
max_population = int(my_args[4])
board = ReadLines(n)
roads = ReadLines(solutions)
starting_point = []

for row in board:
    if '5' in row:
        starting_point = [board.index(row), row.find('5')]
res = geneticAlgorithm(board,m,n,starting_point,roads,timezz, max_population)
print("trasa: ", res)
print("długość: ", len(res))
