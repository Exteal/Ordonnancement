from utils import main, Ordonnancement, computeTasksLengthFrom, Position
from copy import deepcopy

"""
Ordonnancement SSI, heuristique de l'insertion
"""

class OrdonnancementSSIInsertion(Ordonnancement):
    def algo_assign(self):
        print("Ordonnancement SSI")
        print(f"Taxis : {self.env.taxis}")
        
        nb_taxis = len(self.env.taxis)
        tasks = self.env.tasks_to_ord
        
        for task in tasks: 

            min_offer_taxi = None
            min_offer_value = float('inf')
            min_offer_index = -1

            
            for taxi in self.env.taxis:
                temp_tasks = deepcopy(taxi.tasks)

                inser = len(temp_tasks)

                value = float('inf')
                index = -1
                
                if inser == 0:
                    value = taxi.position.distanceVers(task.origin) + task.origin.distanceVers(task.destination)
                    index = 0
                    
                    if (value < min_offer_value):
                        min_offer_value = value
                        min_offer_taxi = taxi
                        min_offer_index = index
                    
                elif inser == 1:
                    tent1 = deepcopy(taxi.tasks)
                    tent2 = deepcopy(taxi.tasks)

                    tent1.insert(0, task)
                    tent2.insert(1, task)
                    
                    len1 = computeTasksLengthFrom(taxi.position, tent1)
                    len2 = computeTasksLengthFrom(taxi.position, tent2)

                    index, value = (0,len1) if len1 < len2 else (1,len2)
                    
                    if (value < min_offer_value):
                        min_offer_value = value
                        min_offer_taxi = taxi
                        min_offer_index = index

                else :

                    tenta = deepcopy(taxi.tasks)
                    tenta.insert(0, task)

                    index = 0
                    value = computeTasksLengthFrom(taxi.position, tenta)

                    for i in range(len(taxi.tasks)):
                        nth_tent = deepcopy(taxi.tasks)
                        nth_tent.insert(i, task)

                        nth_value = computeTasksLengthFrom(taxi.position, nth_tent)
                        
                        if nth_value < value:
                            tenta = nth_tent
                            index = i
                            value = nth_value
                       

                    if (value < min_offer_value):
                        min_offer_value = value
                        min_offer_taxi = taxi
                        min_offer_index = index

      

            min_offer_taxi.tasks.insert(min_offer_index, task)




class OrdonnancementSSIPrim(Ordonnancement):
    def algo_assign(self):
        print("Ordonnancement SSI")
        print(f"Taxis : {self.env.taxis}")
        
        nb_taxis = len(self.env.taxis)
        tasks = self.env.tasks_to_ord
        
        for task in tasks: 

            min_offer_taxi = None
            min_offer_value = float('inf')
            min_offer_index = -1

            
            for taxi in self.env.taxis:
                temp_tasks = deepcopy(taxi.tasks)

                inser = len(temp_tasks)

                value = float('inf')
                index = -1
                
                if inser == 0:
                    value = taxi.position.distanceVers(task.origin) + task.origin.distanceVers(task.destination)
                    index = 0
                    
                    if (value < min_offer_value):
                        min_offer_value = value
                        min_offer_taxi = taxi
                        min_offer_index = index
                    
                elif inser == 1:
                    tent1 = deepcopy(taxi.tasks)
                    tent2 = deepcopy(taxi.tasks)

                    tent1.insert(0, task)
                    tent2.insert(1, task)
                    
                    len1 = computeTasksLengthFrom(taxi.position, tent1)
                    len2 = computeTasksLengthFrom(taxi.position, tent2)

                    index, value = (0,len1) if len1 < len2 else (1,len2)
                    
                    if (value < min_offer_value):
                        min_offer_value = value
                        min_offer_taxi = taxi
                        min_offer_index = index

                else :

                    tenta = deepcopy(taxi.tasks)
                    tenta.insert(0, task)

                    index = 0
                    value = computeTasksLengthFrom(taxi.position, tenta)

                    for i in range(len(taxi.tasks)):
                        nth_tent = deepcopy(taxi.tasks)
                        nth_tent.insert(i, task)

                        nth_value = computeTasksLengthFrom(taxi.position, nth_tent)
                        
                        if nth_value < value:
                            tenta = nth_tent
                            index = i
                            value = nth_value
                       

                    if (value < min_offer_value):
                        min_offer_value = value
                        min_offer_taxi = taxi
                        min_offer_index = index

      

            min_offer_taxi.tasks.insert(min_offer_index, task)

main(ord = OrdonnancementSSIInsertion)