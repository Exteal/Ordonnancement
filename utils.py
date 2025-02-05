import sys
from abc import ABC, abstractmethod
from random import randint
from typing import List, Tuple
from copy import deepcopy
from math import sqrt

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


class Task:
    def __init__(self, o : Position, d : Position):  
        self.origin : Position = Position(o.x, o.y)
        self.destination : Position = Position(d.x, d.y)

    def __repr__(self):
        return f"{self.origin} to ({self.destination})"
    

class Taxi:
    def __init__(self, position = Position(0, 0)):
        self.position : position = deepcopy(position)
        self.tasks : List[Task] = []

    def computeTasksLength(self):
        acc = 0
        taxi_temp_pos = Position(self.position.x, self.position.y)

        #print(f"Taxi tasks : {self.tasks}")
        for t in self.tasks:
            acc += taxi_temp_pos.distanceVers(t.origin)
            acc += t.origin.distanceVers(t.destination)
            taxi_temp_pos = t.destination

        return acc

    def __repr__(self):
        return f"Taxi at {self.position} with tasks len {self.computeTasksLength()}"


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
        
        self.env.tasks_to_ord = tasks
    
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


"""
Tout assigner au premier taxi
"""
class OrdonnancementUn(Ordonnancement):
    def algo_assign(self):
        t = self.env.taxis[0]
        t.tasks = self.env.tasks_to_ord





def parse_args():
    args = sys.argv

    taxis_ct = int(args[1])
    env_size = int(args[2])
    task_freq = int(args[3])
    task_method = args[4]
    tasks_ct = int(args[5])
    total_time = int(sys.argv[6])

    return taxis_ct, env_size, task_freq, task_method, tasks_ct, total_time

def initialize(taxis_ct, env_size, task_freq, task_method, tasks_ct):
    taxis = []
    for _ in range(taxis_ct):
        taxis.append(Taxi())

    env = Environnement(env_size, taxis)

    generator = createGenerator(task_method, tasks_ct, env, task_freq)

    return env, generator



def main(ord):

    taxis_ct, env_size, task_freq, task_method, tasks_ct, total_time = parse_args()
    env, gen = initialize(taxis_ct, env_size, task_freq, task_method, tasks_ct)
    
    ord = ord(env)
    total_time = int(sys.argv[6])

    for timestamp in range(total_time):
        if gen.shouldGenerate(timestamp):
            gen.generate_tasks()

            ord.ordonnancer()

            #for idx, taxi in enumerate(env.taxis):
            #    print(f"Taches taxi {idx} :" + str(taxi.tasks))



#main(ord = OrdonnancementPartieUne)
#main(ord = ordonnancementNego)

