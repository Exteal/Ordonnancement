from utils import main, Ordonnancement, computeTasksLengthFrom, Position, initialize
from copy import deepcopy
"""
Assignation optimale selon la distance, un seul taxi
"""
class OrdonnancementPartieUne(Ordonnancement):
    def algo_assign(self):

        print("Ordonnancement Partie Une")
        print(f"Taxis : {self.env.taxis}")
        
        nb_taxis = len(self.env.taxis)

        tasks = self.env.tasks_to_ord
        
        
        for task in tasks:
            for taxi in self.env.taxis:
                #inser = range(len(taxi.tasks)):
                inser = len(taxi.tasks)
                    
                if inser == 0:
                    taxi.tasks = [task]
                    continue                
    
                elif inser == 1:
                    tent1 = deepcopy(taxi.tasks)
                    tent2 = deepcopy(taxi.tasks)

                    tent1.insert(0, task)
                    tent2.insert(1, task)
                    
                    taxi.tasks = tent1 if computeTasksLengthFrom(taxi.position, tent1) < computeTasksLengthFrom(taxi.position, tent2) else tent2
                    continue

                else :
                    tent_base = deepcopy(taxi.tasks)
                    tent_base.insert(0, task)

                    for i in range(len(taxi.tasks)):
                        tentN = deepcopy(taxi.tasks)
                        tentN.insert(i, task)

                        if computeTasksLengthFrom(taxi.position, tentN) < computeTasksLengthFrom(taxi.position, tent_base):
                            tent_base = tentN
                    
                    
                    taxi.tasks = tent_base
                    





def testPartie1():
   
    taxis_ct = 1
    env_size = 10
    task_freq = 15
    task_method = "test1"
    task_ct = 5
    total_time = 20
    
    env, gen = initialize(taxis_ct, env_size, task_freq, task_method, task_ct)
    ord = OrdonnancementPartieUne(env)

    tasks = []

    gen.generate_tasks()
    ord.ordonnancer()

    for idx, taxi in enumerate(env.taxis):
        print(f"Taxi : {idx} : " + str(taxi.tasks))
        print(f"Distance : " + str(taxi.computeTasksLength()))


testPartie1()