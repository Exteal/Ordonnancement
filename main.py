from utils import main, parse_args, parse_args_default, compare_main
from partie1 import testPartie1, OrdonnancementPartieUne
from partie3 import OrdonnancementSSIInsertion, OrdonnancementSSIInsertionRegret, OrdonnancementPSI




def desk():
    
    taxis_ct, env_size, task_freq, task_method, tasks_ct, total_time = parse_args_default()


    while True:
    
        print("0 : Paramétrage")
        print("2 : Ordonnancement Partie 1")
        print("3 : Ordonnancement SSI Insertion")
        print("4 : Ordonnancement SSI Insertion Regret")
        print("5 : Comparaison SSI Insertion vs SSI Insertion Regret")
        print("6 : Ordonnancement PSI")
        print("7 : Comparaison SSI Insertion vs PSI")


        print("9 : Quit")

        value = int(input("Valeur : "))

    

        if value == 0:
            taxis_ct, env_size, task_freq, task_method, tasks_ct, total_time = parse_args()
            print(f"values : {taxis_ct} {env_size} {task_freq} {task_method} {taxis_ct} {total_time}")
        
        if value == 1:
            testPartie1()
        
        elif value == 2:
            main(OrdonnancementPartieUne, taxis_ct, env_size, task_freq, task_method, tasks_ct, total_time)

        elif value == 3:

            main(OrdonnancementSSIInsertion, taxis_ct, env_size, task_freq, task_method, tasks_ct, total_time)

        elif value == 4:
            main(OrdonnancementSSIInsertionRegret, taxis_ct, env_size, task_freq, task_method, tasks_ct, total_time)
        

        elif value == 5:
            compare_main(OrdonnancementSSIInsertion, OrdonnancementSSIInsertionRegret, taxis_ct, env_size, task_freq, task_method, tasks_ct, total_time)

        elif value == 6:
            main(OrdonnancementPSI, taxis_ct, env_size, task_freq, task_method, tasks_ct, total_time)
        
        elif value == 7:
            compare_main(OrdonnancementSSIInsertion, OrdonnancementPSI, taxis_ct, env_size, task_freq, task_method, tasks_ct, total_time)
        
        elif value == 9:
            break


desk()