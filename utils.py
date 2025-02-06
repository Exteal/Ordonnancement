import sys
from abc import ABC, abstractmethod
from random import randint
from typing import List, Tuple
from copy import deepcopy
from math import sqrt




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


class Task:
    def __init__(self, o : Position, d : Position):  
        self.origin : Position = Position(o.x, o.y)
        self.destination : Position = Position(d.x, d.y)

    def __repr__(self):
        return f"{self.origin} to ({self.destination})"
    

class Taxi:
    def __init__(self, position = Position(0, 0)):
        self.position : Position = deepcopy(position)
        self.tasks : List[Task] = []
        self.id = id(self)

    def computeTasksLength(self):
        acc = 0
        taxi_temp_pos = Position(self.position.x, self.position.y)

        for t in self.tasks:
            acc += taxi_temp_pos.distanceVers(t.origin)
            acc += t.origin.distanceVers(t.destination)
            taxi_temp_pos = t.destination

        return acc

    def __repr__(self):
        #return f"Taxi {self.id}"
        return f"Taxi at {self.position} with tasks len {self.computeTasksLength()} : {self.tasks}"


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
    return 4, 10, 2, "rd", 4, 6

def parse_args():
    

    taxis_ct = int(input("Taxi count : "))
    
    env_size = int(input("Env size : "))
    
    task_freq = int(input("Task freq : "))

    task_method = str(input("Task Method : "))

    tasks_ct = int(input("Task count : "))

    total_time = int(input("Total time : "))

    #args = sys.argv
    #taxis_ct = int(args[1])
    #env_size = int(args[2])
    #task_freq = int(args[3])
    #task_method = args[4]
    #tasks_ct = int(args[5])
    #total_time = int(sys.argv[6])

    return taxis_ct, env_size, task_freq, task_method, tasks_ct, total_time

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




def main(ord, taxis_ct, env_size, task_freq, task_method, tasks_ct, total_time):

    #taxis_ct, env_size, task_freq, task_method, tasks_ct, total_time = kwargs
    
    env, gen = initialize(taxis_ct, env_size, task_freq, task_method, tasks_ct)
    
    ord = ord(env)

    for timestamp in range(total_time):
        if gen.shouldGenerate(timestamp):
            tasks = gen.generate_tasks()
            env.tasks_to_ord = tasks

            ord.ordonnancer()

            #for idx, taxi in enumerate(env.taxis):
            #    print(f"Taches taxi {idx} :" + str(taxi.tasks))


def compare_main(ord1, ord2, taxis_ct, env_size, task_freq, task_method, tasks_ct, total_time):

    env, gen = initialize(taxis_ct, env_size, task_freq, task_method, tasks_ct, random_taxi_location = True)
    env2, _ = initialize(taxis_ct, env_size, task_freq, task_method, tasks_ct, random_taxi_location = True)

    ord1 = ord1(env)
    ord2 = ord2(env2)

    for timestamp in range(total_time):
        if gen.shouldGenerate(timestamp):
            tasks = gen.generate_tasks()
            env.tasks_to_ord = deepcopy(tasks)
            env2.tasks_to_ord = deepcopy(tasks)

            ord1.ordonnancer()
            ord2.ordonnancer()

            
    print(f"\n{ord1}\n")

    for idx, taxi in enumerate(env.taxis):
        print(f"Taxi {idx} : {taxi}")

    print(f"\n{ord2}\n")
    
    for idx, taxi in enumerate(env2.taxis):
        print(f"Taxi {idx} : {taxi}")


#main(ord = OrdonnancementPartieUne)
#main(ord = ordonnancementNego)

