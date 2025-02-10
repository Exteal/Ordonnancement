from abc import ABC, abstractmethod
from random import randint
from typing import List
from copy import deepcopy
from math import sqrt

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class Insertion:
    def __init__(self, index, value):
        self.index = index
        self.value = value

    def __repr__(self):
        return f"Insertion at {self.index} with value {self.value}"
    

class Position:
    def __init__(self, x : float, y : float):
        self.x = x
        self.y = y

    def distanceVers(self, p):
        return sqrt((p.x - self.x)**2 + (p.y - self.y)**2)

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def dcop_repr(self):
        return f"{self.x}{self.y}"

class Task:
    def __init__(self, o : Position, d : Position):  
        self.origin : Position = Position(o.x, o.y)
        self.destination : Position = Position(d.x, d.y)

    def __repr__(self):
        return f"{self.origin} to ({self.destination})"
    
    def dcop_repr(self):
        return f"task_{self.origin.dcop_repr()}_to_{self.destination.dcop_repr()}"
    

class Taxi:
    def __init__(self, position = Position(0, 0)):
        self.position : Position = deepcopy(position)
        self.tasks : List[Task] = []
        self.currentTask = None
        self.id = id(self)
        self.timer = 0

    def computeTasksLength(self):
        acc = 0
        taxi_temp_pos = Position(self.position.x, self.position.y)

        for t in self.tasks:
            acc += taxi_temp_pos.distanceVers(t.origin)
            acc += t.origin.distanceVers(t.destination)
            taxi_temp_pos = t.destination

        return acc
    
    def computeLengthOfTask(self, t : Task):
        return self.position.distanceVers(t.origin) + t.origin.distanceVers(t.destination)

    
    def endCurrentTask(self):
        """pas de reset timer systématique pour prise en compte du temps perdu sur le timestamp precedent"""

        self.position = self.currentTask.destination
        self.currentTask = None
        
        if len(self.tasks) == 0:
            self.timer = 0

    def startNewTask(self):
        """ajout au timer pour prise en compte du temps perdu sur le timestamp precedent, sinon assigner"""
        if len(self.tasks) > 0:
            new_task = self.tasks.pop(0)
            self.timer += self.computeLengthOfTask(new_task)
            self.currentTask = new_task

    def __str__(self):
        return f"Taxi {self.id} at {self.position} ; current {self.currentTask} timer {self.timer} \n and tasks len {self.computeTasksLength()} : {self.tasks}"


def computeTasksLengthFrom(starting_position, tasks):
    acc = 0
    taxi_temp_pos = starting_position

    for t in tasks:
        acc += taxi_temp_pos.distanceVers(t.origin)
        acc += t.origin.distanceVers(t.destination)
        taxi_temp_pos = t.destination
    return acc


class Environnement:
    def __init__(self, size, taxis):
        self.size : int = size
        self.tasks_to_ord : List[Task] = []
        self.taxis : List[Taxi] = taxis
        
class TaskGenerator(ABC):
    
    def __init__(self, tasks_ct, env, freq):
        super().__init__()
        self.tasks_ct : int = tasks_ct
        self.env : Environnement = env
        self.freq : int = freq
    
    def shouldGenerate(self, timestamp):
        return timestamp % self.freq == 0
    
    @abstractmethod
    def generate_tasks(self):
        pass



class TestGenerator1(TaskGenerator):
    def __init__(self, tasks_ct, env, freq):
        super().__init__(tasks_ct, env, freq)

    def generate_tasks(self):
        tasks = []
        tasks.append(Task(Position(2.2, 2.2), Position(3.3, 3.3)))
        
        tasks.append(Task(Position(9.2, 9.2), Position(9.9, 9.9)))
        tasks.append(Task(Position(1.1, 1.1), Position(9.1, 8.1)))

        self.env.tasks_to_ord = tasks
    
    def __str__(self):
        return f"Test Generator 1 of size {self.env.size} generating {self.tasks_ct} tasks"


class RandomGenerator(TaskGenerator):

    def __init__(self, tasks_ct, env, freq):
        super().__init__(tasks_ct, env, freq)

    def generate_tasks(self):
        tasks = []
        for _ in range(self.tasks_ct):
           o = Position(randint(0, self.env.size), randint(0, self.env.size))
           d = Position(randint(0, self.env.size), randint(0, self.env.size))
    
           t = Task(o, d)
           tasks.append(t)
        
        return tasks
    
    def __str__(self):
        return f"Random Generator of size {self.env.size} generating {self.tasks_ct} tasks"


def createGenerator(gen, tasks_ct, env, freq):
    if gen == "rd":
        return RandomGenerator(tasks_ct, env, freq)
    
    if gen == "test1":
        return TestGenerator1(tasks_ct, env, freq)

    raise NotImplementedError("Unknown Generator Type")



class Ordonnancement(ABC):
    
    def __init__(self, env):
        self.env : Environnement = env
    
    @abstractmethod
    def algo_assign(self):
        pass

    def ordonnancer(self):
        self.algo_assign()
        self.env.tasks_to_ord = []

    def __str__(self):
        return "Ordonnancement "


"""
Tout assigner au premier taxi
"""
class OrdonnancementUn(Ordonnancement):
    def algo_assign(self):
        t = self.env.taxis[0]
        t.tasks = self.env.tasks_to_ord
    
    def __str__(self):
        return super().__str__() + " Un"






def parse_args_default():
    return 3, 10, 20, "rd", 5, 100, True

def parse_args():
    

    taxis_ct = int(input("Taxi count : "))
    
    env_size = int(input("Env size : "))
    
    task_freq = int(input("Task freq : "))

    task_method = str(input("Task Method : "))

    tasks_ct = int(input("Task count : "))

    total_time = int(input("Total time : "))

    taxi_random_location = input("Random taxi location ? (y/n) : ") == "y"
    return taxis_ct, env_size, task_freq, task_method, tasks_ct, total_time, taxi_random_location

def initialize(taxis_ct, env_size, task_freq, task_method, tasks_ct, random_taxi_location = False):
    taxis = []
    
    if random_taxi_location:
        for _ in range(taxis_ct):
            taxis.append(Taxi(Position(randint(0, env_size), randint(0, env_size))))

    else:
        for _ in range(taxis_ct):
            taxis.append(Taxi())

    env = Environnement(env_size, taxis)

    generator = createGenerator(task_method, tasks_ct, env, task_freq)

    return env, generator



def format_legend_labels(x, pos):
    return f"{x:.2f}"


def multi_main(reps, ord, taxis_ct, env_size, task_freq, task_method, tasks_ct, total_time, taxis_random_location = False):
    cumuls = []
    seps = {}


    
    for _ in range(reps):
        sep, cumul = main(ord, taxis_ct, env_size, task_freq, task_method, tasks_ct, total_time, taxis_random_location, plots = False)
        cumuls.append(cumul)
        
        for taxi, values in sep.items():
            if taxi not in seps:
                seps[taxi] = [] 
            seps[taxi].append(values)
    

    fin = {}
    ad = []
    for taxi, vals in seps.items():
        mns = np.mean(vals, axis = 0)
        fin[taxi] = mns
        ad.append(mns)
 


    maxs = np.maximum.reduce(ad)
    plt.title("Moyenne des valeurs pour chaque taxi, maximum des moyennes")
    plt.plot(maxs)
    plt.show()

    means = np.mean(cumuls, axis=0)

        
    plt.plot(means)
    plt.title(f"{ord} average over {reps} runs")
    plt.legend()
    plt.show()

    
    pd.Series(means).round(decimals = 0).value_counts(sort=True).plot(kind='bar')

    plt.title("Frequence d'apparition des durees restantes")

    plt.show()

    
def main(ord, taxis_ct, env_size, task_freq, task_method, tasks_ct, total_time, taxis_random_location = False, plots = True):
    
    env, gen = initialize(taxis_ct, env_size, task_freq, task_method, tasks_ct, taxis_random_location)
    
    ord = ord(env)

    taxis_cumul_ord = []
    by_taxi_ord = {}

    for taxi in env.taxis:
        by_taxi_ord[taxi] = []

    for timestamp in range(total_time):
        
        #print(f"Timestamp : {timestamp}")
        
        if gen.shouldGenerate(timestamp):
            tasks = gen.generate_tasks()
            env.tasks_to_ord = tasks

            ord.ordonnancer()

        acc = 0

        for taxi in env.taxis:
            #print(f"Taxi {taxi.id} with current {taxi.currentTask}, timer {taxi.timer} and scheduled {taxi.tasks}")

            if taxi.currentTask == None:
                taxi.startNewTask()
            else:
                taxi.timer -= 1
                if taxi.timer <= 0:
                    taxi.endCurrentTask()
                    taxi.startNewTask()
            

            tasks_len = taxi.computeTasksLength() 
            acc += tasks_len
            by_taxi_ord[taxi].append(tasks_len)

            #print(taxi)
        
        taxis_cumul_ord.append(acc)
        #print("\n\n")
    
    if plots:
        plt.plot(taxis_cumul_ord, label=f"Cumulé {ord}")
        plt.legend()
        pd.DataFrame(by_taxi_ord).plot()

        plt.show() 

    return by_taxi_ord, taxis_cumul_ord
            #for idx, taxi in enumerate(env.taxis):
            #    print(f"Taches taxi {idx} :" + str(taxi.tasks))


def compare_main(ord1, ord2, taxis_ct, env_size, task_freq, task_method, tasks_ct, total_time, taxi_random_location):

    env, gen = initialize(taxis_ct, env_size, task_freq, task_method, tasks_ct, taxi_random_location)
    env2, _ = initialize(taxis_ct, env_size, task_freq, task_method, tasks_ct, taxi_random_location)

    ord1 = ord1(env)
    ord2 = ord2(env2)

    ## METRICS

    taxis_cumul_dord1 = []
    taxis_cumul_dord2 = []
    by_taxi_ord1 = {}
    by_taxi_ord_2 = {}

    for taxi in env.taxis:
        by_taxi_ord1[taxi] = []
    
    for taxi in env2.taxis:
        by_taxi_ord_2[taxi] = []

    ## ALGO

    for timestamp in range(total_time):
        print(f"Timestamp {timestamp}")
        if gen.shouldGenerate(timestamp):
            tasks = gen.generate_tasks()
            env.tasks_to_ord = deepcopy(tasks)
            env2.tasks_to_ord = deepcopy(tasks)

            ord1.ordonnancer()
            ord2.ordonnancer()

        print(f"\n{ord1}\n")
        acc = 0

        for taxi in env.taxis:
            #print(f"Taxi {taxi.id} with current {taxi.currentTask}, timer {taxi.timer} and scheduled {taxi.tasks}")
            if taxi.currentTask == None:
                taxi.startNewTask()
            else:
                taxi.timer -= 1
                if taxi.timer <= 0:
                    taxi.endCurrentTask()
                    taxi.startNewTask()
                
            tasks_len = taxi.computeTasksLength() 
            acc += tasks_len
            by_taxi_ord1[taxi].append(tasks_len)

            print(taxi)
        
        taxis_cumul_dord1.append(acc)
        
        acc = 0
        
        print(f"\n{ord2}\n")

        for taxi in env2.taxis:
            #print(f"Taxi {taxi.id} with current {taxi.currentTask}, timer {taxi.timer} and scheduled {taxi.tasks}")
            if taxi.currentTask == None:
                taxi.startNewTask()
            else:
                taxi.timer -= 1
                if taxi.timer <= 0:
                    taxi.endCurrentTask()
                    taxi.startNewTask()
            
            tasks_len = taxi.computeTasksLength() 
            acc += tasks_len
            by_taxi_ord_2[taxi].append(tasks_len)

            print(taxi)
        taxis_cumul_dord2.append(acc)
        
        acc = 0
    
    #print("METRICS")

    #print(taxis_cumul_dord1)
    #print(taxis_cumul_dord2)

    #print("BY TAXI")
    #print(by_taxi_ord1)
    #print(by_taxi_ord_2)


    plt.plot(taxis_cumul_dord1, label=f"Cumulé {ord1}")
    plt.plot(taxis_cumul_dord2, label=f"Cumulé {ord2}")

    plt.legend()
    
    pd.DataFrame(by_taxi_ord1).plot() 
    pd.DataFrame(by_taxi_ord_2).plot() 

    plt.show()

