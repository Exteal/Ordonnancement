from utils import main, Ordonnancement, computeTasksLengthFrom, Position, Insertion
from copy import deepcopy

"""
Ordonnancement SSI, heuristique de l'insertion
"""

class OrdonnancementSSIInsertion(Ordonnancement):
    """
    Ordonnancement SSI
    """

     
    def algo_assign(self):
        #print("Ordonnancement SSI")
        #print(f"Taxis : {self.env.taxis}")
        
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

    def __str__(self): 
        return super().__str__() + "SSI Insertion "



class OrdonnancementSSIInsertionRegret(OrdonnancementSSIInsertion):
    """
    Ordonnancement SSI Regret
    """

    
    def algo_assign(self):
        #print("Ordonnancement SSI Regret")

        tasks = deepcopy(self.env.tasks_to_ord)


        for loop in range(len(self.env.tasks_to_ord)):

            #print(f"Loop : {loop}")
            #print(f"Tasks : {tasks}")

            #print(f"Taxis : {self.env.taxis}\n")



            regrets = {}
            offers = {}

            for index, task in enumerate(tasks): 


                #min_offer_taxi = None
                #min_offer_value = float('inf')
                #min_offer_index = -1
                
                
                offers[index] = {}
                
                for taxi in self.env.taxis:
                    temp_tasks = deepcopy(taxi.tasks)

                    inser = len(temp_tasks)

                    
                    if inser == 0:
                        value = taxi.position.distanceVers(task.origin) + task.origin.distanceVers(task.destination)
                        
                        offers[index][taxi] = Insertion(0, value)


                    elif inser == 1:
                        tent1 = deepcopy(taxi.tasks)
                        tent2 = deepcopy(taxi.tasks)

                        tent1.insert(0, task)
                        tent2.insert(1, task)
                        
                        len1 = computeTasksLengthFrom(taxi.position, tent1)
                        len2 = computeTasksLengthFrom(taxi.position, tent2)

                        index_inser, value = (0,len1) if len1 < len2 else (1,len2)
                        offers[index][taxi] = Insertion(index_inser, value)
                        

                    else :

                        tenta = deepcopy(taxi.tasks)
                        tenta.insert(0, task)

                        index_inser = 0
                        value = computeTasksLengthFrom(taxi.position, tenta)

                        for i in range(len(taxi.tasks)):
                            nth_tent = deepcopy(taxi.tasks)
                            nth_tent.insert(i, task)

                            nth_value = computeTasksLengthFrom(taxi.position, nth_tent)
                            
                            if nth_value < value:
                                tenta = nth_tent
                                index_inser = i
                                value = nth_value
                        

                        offers[index][taxi] = Insertion(index_inser, value)

        

            
            min_offers_taxi = {}
            for task_index, taxis_offers in offers.items():
                values = set(list(taxis_offers.values()))


                min_offer : Insertion = sorted(values, key= lambda insertion : insertion.value)[0]
                second_offer : Insertion = sorted(values, key= lambda insertion : insertion.value)[1]

                regrets[task_index] = abs(min_offer.value - second_offer.value)
                min_offers_taxi[task_index] = list(taxis_offers.keys())[list(taxis_offers.values()).index(min_offer)]




            #print(f"Offers : {offers}")
            #print(f"Regrets : {regrets}")

            #print(f"Min offers : {min_offers_taxi}\n")

            max_regret_task_index = max(regrets, key=regrets.get)
            max_regret_task = tasks[max_regret_task_index]
            

            best_taxi = min_offers_taxi[max_regret_task_index]

            best_taxi.tasks.insert(offers[max_regret_task_index][best_taxi].index, max_regret_task)
            tasks.remove(max_regret_task)


    def __str__(self):
        return super().__str__() + "Regret"
    



class OrdonnancementPSI(Ordonnancement):
    """
    Ordonnancement PSI
    """

    def algo_assign(self):
        tasks = deepcopy(self.env.tasks_to_ord)

        for task in tasks:

            min_offer_taxi = self.env.taxis[0]
            min_offer_value = self.env.taxis[0].position.distanceVers(task.origin) + task.origin.distanceVers(task.destination)
            
            for taxi in self.env.taxis:
                value = taxi.position.distanceVers(task.origin) + task.origin.distanceVers(task.destination)
                if value < min_offer_value:
                    min_offer_value = value
                    min_offer_taxi = taxi
        
            min_offer_taxi.tasks.append(task)
            


    def __str__(self):
        return super().__str__() + "PSI"