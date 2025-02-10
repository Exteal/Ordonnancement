from utils import Ordonnancement, computeTasksLengthFrom, Task
from copy import deepcopy

class OrdonnancementDCOPSimple(Ordonnancement):
    """
    Ordonnancement DCOP, par distance au point initial
    """
    
    def algo_assign(self):
        tasks = deepcopy(self.env.tasks_to_ord)
        costs = {}

        
        
        for task in tasks:
            costs[task] = {}
            for taxi in self.env.taxis:
                costs[task][taxi] = computeTasksLengthFrom(taxi.position, [task])
        

        print(f"costs : " + str(costs))

        self.write_pydcop_file(costs)

        print("pydcop file written") 


    def write_pydcop_file(self, costs):

        with open("pydcop_file.yaml", "w") as f:
            f.write("name: taxi assignment\n")
            f.write("objective: min\n")
            
            f.write("\n\n")

            f.write("domains:\n")
            f.write("  assignement:\n")
            f.write(f"    values: {[taxi.id for taxi in self.env.taxis]}\n")
            f.write("    type: non_semantic\n")

            f.write("\n\n")
            
            f.write("variables:\n")
            
            for task, _ in costs.items():
                f.write(f"  {task.dcop_repr()}:\n")
                f.write("    domain: assignement\n")
                f.write("\n")

            f.write("\n\n")

            f.write("constraints:\n")

            for task, values in costs.items():
                
                f.write(f"  {task.dcop_repr()}_length:\n")
                f.write(f"    type: intention\n")
                f.write(f"    function: |\n")
                for taxi, cost in values.items():
                    f.write(f"      if {task.dcop_repr()} == {taxi.id}:\n")
                    f.write(f"        return {cost}\n")
                    f.write("\n")

            f.write("\n\n")
            f.write(f"agents: { [f"ag_{i}"for i in range(len(costs))]} \n")

            
            #for i in range(len(costs)):
            #    f.write(f"  ag_{i}:\n")


