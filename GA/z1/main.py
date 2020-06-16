import sys
import numpy as np
import time

class Genetic(object):

    def __init__(self, f, x, theta, time_1, pop_size=100, n_variables=5):
        self.f = f
        self.theta = theta
        self.x = x
        self.time_1 = time_1
        self.minim = -5.0
        self.maxim = 5.0
        self.pop_size = pop_size
        self.n_variables = n_variables
        self.population = self.initializePopulation(self.x)
        self.evaluatePopulation()

    def initializePopulation(self, x):
        pop = [np.random.uniform(self.minim, self.maxim, size=(self.n_variables))
                           for i in range(self.pop_size)]
        pop.append(np.array(x))
        return pop

    def evaluatePopulation(self):
        return [self.f(i, self.theta) for i in self.population]


    def nextGen(self):
        results = self.evaluatePopulation()
        children = []
        best = self.population[np.argmin(results)]

        while len(children) < self.pop_size:
            # Tournament selection (probably)
            randA, randB = np.random.randint(0, self.pop_size), \
                           np.random.randint(0, self.pop_size)
            if results[randA] < results[randB]:
                p1 = self.population[randA]
            else:
                p1 = self.population[randB]

            randA, randB = np.random.randint(0, self.pop_size), \
                           np.random.randint(0, self.pop_size)
            if results[randA] < results[randB]:
                p2 = self.population[randA]
            else:
                p2 = self.population[randB]

            rate = 0    
            if (np.random.random()) > rate:
                crossPoint = np.random.randint(0,4)
                child_1 = np.hstack((p1[:crossPoint],p2[crossPoint:]))
                child_2 = np.hstack((p2[:crossPoint],p1[crossPoint:]))
            else:
                crossPoint = np.random.randint(0,4)
                child_1 = np.hstack((p1[:crossPoint],p2[crossPoint:]))
                child_2 = np.hstack((p2[:crossPoint],p1[crossPoint:]))

            for gene in range(5):
                if np.random.random() > rate:
                    child_1[gene] += np.random.uniform(-0.1, 0.1)
                    child_2[gene] += np.random.uniform(-0.1, 0.1)
            children.append(child_1)
            children.append(child_2)

        self.population = children

    def run(self):
        remaining = 0
        start_time = time.process_time()
        while remaining < self.time_1:
            
            self.nextGen()
            tick = time.process_time()
            remaining = tick - start_time
        return self.population[0]

def yang_func(x, theta):
    result = 0.0
    for i in range(1,6):
        result += theta[i-1]*pow(abs(x[i-1]),i)
    return result



my_args = sys.stdin.readline()
my_args = my_args.split()
time_1 = int(my_args[0])
x= [float(i) for i in my_args[1:6]]
theta = [float(i) for i in my_args[6:len(my_args)]]

gen = Genetic(yang_func, x, theta, time_1)
minim = gen.run()
print(minim, yang_func(minim,theta))

