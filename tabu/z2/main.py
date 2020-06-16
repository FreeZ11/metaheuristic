import copy
import time
import sys

#funkcja ktora genruje pierwsze rozwiazanie oraz koszt pierwszego rozwiazania
def first_solution(neighbours_dict):
    cities = list(neighbours_dict.keys()) # klucze ze slownika ktore sa nazwami miast
    start_node = cities[0] #zaczynamy od pierwszego klucza bo nie ma to znaczenia
    end_node = start_node # ustawiany ostatni przystanek na pierwszy po to by wrocic do punktu wyjscia

    first_solution_arr = []

    current = start_node

    distance_of_first_solution = 0

    while current not in first_solution_arr:
        minim = 10000   # liczba dosc duza zeby kazdy element tablicy byl od niej mniejszy w naszych warunkach
        for k in neighbours_dict[current]:
            if int(k[1]) < int(minim) and k[0] not in first_solution_arr:   #petla ktora znajduje najblizsze miejsce i uzjane to za najlepsze do przejscia
                minim = k[1]
                best_node = k[0]

        first_solution_arr.append(current)
        distance_of_first_solution += int(minim)
        current = best_node

    first_solution_arr.append(end_node)

    position = 0
    for k in neighbours_dict[first_solution_arr[-2]]:
        if k[0] == start_node:
            break
        position += 1

    distance_of_first_solution = (distance_of_first_solution + int(neighbours_dict[first_solution_arr[-2]][position][1])-10000)

    return first_solution_arr, distance_of_first_solution


def find_neighborhood(solution, neighbours_dict): #funkcja sluzaca do znajdowania potencjalnych sciezek
    neighborhood_of_solution = []

    for n in solution[1:-1]: # od pierwszego do przedostatniego zeby nie liczyc poczatku 2 razy

        index_1 = solution.index(n)
        for next_n in solution[1:-1]: 

            index_2 = solution.index(next_n)

            if n == next_n:
                continue

            temp = copy.deepcopy(solution) # kopiujemy nasze rozwiazanie by nie operowac bezosrednio na nim tylko na kopii
            temp[index_1] = next_n
            temp[index_2] = n

            total_distance = 0

            for k in temp[:-1]:   # te dwie petle tworza nam liste potencjalnyc sciezek

                next_node = temp[temp.index(k) + 1]
                for i in neighbours_dict[k]:

                    if i[0] == next_node:
                        total_distance += int(i[1])
            temp.append(total_distance)  # do kazdej ze sciezek dodajemy jej dystans/koszt

            if temp not in neighborhood_of_solution:
                neighborhood_of_solution.append(temp)

    index_of_last_place = len(neighborhood_of_solution[0]) - 1

    neighborhood_of_solution.sort(key=lambda x: x[index_of_last_place])   #na koniec sortujemy otrzymana liste wzledem dystansow/kosztow i zwracamy ja
    return neighborhood_of_solution


def tabu_search(first_solution_arr, distance_of_first_solution,neighbours_dic,given_time,size):

    solution = first_solution_arr   #warunki poczatkowe czyli ustawienie naszego pierwszego podejscia na pierwsze
    tabu_list = []
    smallest_cost = distance_of_first_solution
    best_found_solution = solution
    remaining_time = 0

    start_time = time.process_time()
    while remaining_time < given_time:   #glowny warunek dzialania tabusherchu czyli czas narzucony przez nas z gory

        neighborhood = find_neighborhood(solution,neighbours_dic)
        best_solution_index = 0
        best_solution = neighborhood[best_solution_index]
        best_cost_index = len(best_solution) - 1

        found = False
        while found is False:

            iter = 0
            while iter < len(best_solution):

                if best_solution[iter] != solution[iter]:

                    first_to_exchange = best_solution[iter]
                    second_to_exchange = solution[iter]
                    break
                iter +=1

            if [first_to_exchange, second_to_exchange] not in tabu_list and [second_to_exchange, first_to_exchange] not in tabu_list:

                tabu_list.append([first_to_exchange, second_to_exchange])
                found = True
                solution = best_solution[:-1]
                cost = neighborhood[best_solution_index][best_cost_index]

                if cost < smallest_cost:
                    smallest_cost = cost
                    best_found_solution = solution
            else:
                best_solution_index += 1
                best_solution = neighborhood[best_solution_index]

        if len(tabu_list) >= size:

            tabu_list.pop(0)

        tick = time.process_time()
        remaining_time = tick - start_time

    return best_found_solution, smallest_cost


my_args = sys.stdin.readline()
my_args = my_args.split()
timezz = int(my_args[0])
sizezz = int(my_args[1])

distances = {}
i = 1
for line in sys.stdin:
    helper = []
    j = 0
    row = line.split()
    for l in row:
        if l == '0':
            j += 1
            continue
        else:
            j += 1
            helper.append([j, l])
    distances[i] = helper
    i+=1

my_first_solution, distance_of_first = first_solution(distances)

best_sol, best_cost = tabu_search(my_first_solution, distance_of_first, distances, timezz, sizezz)

print(f"Best solution: {best_sol}, with total distance: {best_cost}.")
