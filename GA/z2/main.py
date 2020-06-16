import sys

import time

from random import random
from random import randint

DICT = None
words_entity = None


def dict_maker():
    global DICT
    f = open("dict.txt", "r")
    first_letter = "a"
    words = []
    DICT = {}
    for line in f:
        line = line.lower()
        if line[0] == first_letter:
            words.append(line.rstrip("\n"))
        else:
            DICT[first_letter] = words
            first_letter = line[0]
            words = [line.rstrip("\n")]
    f.close()


def get_input():
    letters = []
    weights = []
    words = []
    input_data = []
    my_args = sys.stdin.readline()
    my_args = my_args.split()
    time_1 = int(my_args[0])
    n = int(my_args[1])

    counter = 0
    try:
        for line in sys.stdin:
            line = line.strip().split()

            if counter < n:
                letters.append(line[0])
                weights.append(line[1])
            else:
                if len(line) == 1:
                    words.append(line[0])
                else:
                    raise IndexError

            counter += 1

    except IndexError:
        return -1

    input_data.append(time_1)
    input_data.append(letters)
    input_data.append(weights)
    input_data.append(words)

    return input_data


def can_be_used(word):
    global words_entity
    temp_helper = words_entity.copy()
    temp_helper = temp_helper.fromkeys(temp_helper, 0)
    for a in word:
        if a in temp_helper:
            temp_helper[a] += 1
        else:
            temp_helper[a] = 1
    exit_flag = 1
    for key in words_entity:
        if key in temp_helper and words_entity[key] >= temp_helper[key]:
            exit_flag = 1
        else:
            return False
    if exit_flag == 1:
        return True


def check_if_exists(word):
    global DICT
    f_letter = word[0]
    if word in DICT[f_letter]:
        return True
    else:
        return False


def count_points(letters, weights, word):
    points = 0
    for letter in word:
        index = letters.index(letter)
        points += int(weights[index])

    return points


def recombination(word1, word2):
    if randint(0, 1) == 1:
        helper = word1
    else:
        helper = word2

    index_of_first = randint(0, min(len(word1), len(word2)) - 1)
    index_of_sec = randint(0, min(len(word1), len(word2)) - 1)
    
    result1 = word1[:index_of_first] + word2[index_of_first:]
    result2 = word1[:index_of_first] + word2[index_of_first:index_of_sec] + helper[index_of_sec:]

    return result1, result2


def generate_pairs(population):
    index_list = [i for i in range(len(population))]
    pairs = []
    for i in range(len(population) // 2):
        tmp = []
        for _ in range(2):
            index = randint(0, len(index_list) - 1)
            tmp.append(population[index])
            index_list.pop(index)
            
            if len(index_list) == 0:
                break
                
        pairs.append(tmp)

    return pairs


def genetic_algorithm(time_max, letters, weights, words):
    population = [word for word in words]

    
    maximum_points = 0
    
    result = ""
   
    prob_of_mutating = 0.1
    
    max_population = 200

    rem_time = 0

    clk_start = time.process_time()
    while rem_time < time_max:

        pairs = generate_pairs(population)

        for pair in pairs:
            for word in pair:
                if check_if_exists(word) and can_be_used(word):
                    points = count_points(letters, weights, word)
                    if points > maximum_points:
                        maximum_points = points
                        result = word

            new_word1, new_word2 = recombination(pair[0], pair[1])

            if random() < prob_of_mutating:
                index = randint(0, (len(new_word1) - 1))
                curr = new_word1[index]
                mutation = curr
                while mutation == curr:
                    mutation = letters[randint(0, (len(letters) - 1))]
                    new_word1 = new_word1[:index] + mutation + new_word1[index + 1:]

            if random() < prob_of_mutating:
                index = randint(0, (len(new_word2) - 1))
                curr = new_word2[index]
                mutation = curr
                while mutation == curr:
                    mutation = letters[randint(0, (len(letters) - 1))]
                    new_word2 = new_word2[:index] + mutation + new_word2[index + 1:]

            if new_word1 not in population:
                population.append(new_word1)

            if new_word2 not in population:
                population.append(new_word2)

        if len(population) > max_population:
            for word in population:
                if not check_if_exists(word):
                    population.remove(word)
            if len(population) > max_population:
                population = sorted(population, key=lambda word: count_points(letters, weights, word), reverse=True)
                population = population[:max_population]

        clk_tick = time.process_time()
        rem_time = clk_tick - clk_start
    print(population)
    return [result] + [maximum_points]


def main():
    global words_entity
    dict_maker()
    arguments = get_input()
    if arguments != -1:
        words_entity = {}
        for a in arguments[1]:
            if a in words_entity:
                words_entity[a] += 1
            else:
                words_entity[a] = 1
        result = genetic_algorithm(arguments[0], arguments[1], arguments[2], arguments[3])
        print(result[1])
        sys.stderr.write((result[0] + "\n"))
    else:
        sys.stderr.write("Bad input!\n")


if __name__ == "__main__":
    main()
