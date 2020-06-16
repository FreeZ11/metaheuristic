#!/usr/bin/env python3

import math
import numpy as np
import random
import sys
import time


def happy_cat(x):   #implementacja funkcji happy cat
    norm = pow(np.linalg.norm(x), 2)
    first_bracket = pow(pow(norm - 4, 2), 0.125)

    addition = 0
    for i in range(4):
        addition += x[i]
    second_bracket = ((0.5 * norm) + addition) * 0.25

    return first_bracket + second_bracket + 0.5


def griewank(x):   # implementacja funkcji griewank
    first_half = 0
    second_half = 1
    for i in range(1, 5):
        first_half += (pow(x[i - 1], 2) / 4000)
        second_half *= math.cos(x[i - 1] / math.sqrt(i))

    return 1 + first_half - second_half


# funkcja znajdujaca punkty w otoczeniu danego punktu
def neighbours(x, radius):
    result = [[x[0] + radius, x[1], x[2], x[3]]]
    result += [[x[0] - radius, x[1], x[2], x[3]]]
    result += [[x[0], x[1] + radius, x[2], x[3]]]
    result += [[x[0], x[1] - radius, x[2], x[3]]]
    result += [[x[0], x[1], x[2] + radius, x[3]]]
    result += [[x[0], x[1], x[2] - radius, x[3]]]
    result += [[x[0], x[1], x[2], x[3] + radius]]
    result += [[x[0], x[1], x[2], x[3] - radius]]
    return result


def get_random_val(a, b):
    arr = []
    for i in range(4):
        arr.append(random.uniform(a, b))
    return arr


def minimalizer(g_time, function, arr, base_radius, limit):
    remaining = 0
    radius = base_radius
    minimum = function(arr)
    best_x = arr
    greater = 0
    start_time = time.process_time()

    while remaining < g_time:

        changer = get_random_val(min(best_x), max(best_x))
        if function(changer) < minimum:
            minimum = function(changer)
            best_x = changer

        exes = neighbours(best_x, radius)

        for i in exes:
            curr = function(i)
            if curr < minimum:
                minimum = curr
                best_x = i
                greater += 1

        if greater > 16 and radius > limit:
            radius /= 4
            greater = 0
        elif greater < 8:
            radius = base_radius
        elif radius > limit:
            radius /= 2

        exes.clear()
        tick = time.process_time()
        remaining = tick - start_time
    return best_x, minimum

my_args = sys.stdin.readline()
my_args = my_args.split()
time_1 = int(my_args[0])
which_func = int(my_args[1])

if which_func == 0:
    x = get_random_val(-5, 5)
    print(minimalizer(time_1, happy_cat, x, 2, 0.0001))
if which_func == 1:
    x = get_random_val(-1, 1)
    print(minimalizer(time_1, griewank, x, 0.1, 0.00001))
