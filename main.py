from utils import main, parse_args, parse_args_default, compare_main, multi_main
from partie1 import testPartie1, OrdonnancementPartieUne
from partie3 import OrdonnancementSSIInsertion, OrdonnancementSSIInsertionRegret, OrdonnancementPSI
from partie2 import OrdonnancementDCOPSimple



def desk():
    
    taxis_ct, env_size, task_freq, task_method, tasks_ct, total_time, taxi_random_location = parse_args_default()


    while True:
    
        print("0 : Paramétrage")
        
        print("2 : Ordonnancement Partie 1")
        
        print("3 : Ordonnancement SSI Insertion")
        print("4 : Ordonnancement SSI Insertion Regret")
        print("5 : Comparaison SSI Insertion vs SSI Insertion Regret")
        print("6 : Ordonnancement PSI")
        print("7 : Comparaison SSI Insertion vs PSI")

        print("8 : Ordonnancement DCOP Simple")

        print("10 : Multi")

        print("9 : Quit")


        value = int(input("Valeur : "))

    

        if value == 0:
            taxis_ct, env_size, task_freq, task_method, tasks_ct, total_time, taxi_random_location = parse_args()
            print(f"values : {taxis_ct} {env_size} {task_freq} {task_method} {taxis_ct} {total_time} {taxi_random_location}")
        
        if value == 1:
            testPartie1()
        
        elif value == 2:
            main(OrdonnancementPartieUne, taxis_ct, env_size, task_freq, task_method, tasks_ct, total_time, taxi_random_location)

        elif value == 3:

            main(OrdonnancementSSIInsertion, taxis_ct, env_size, task_freq, task_method, tasks_ct, total_time, taxi_random_location)

        elif value == 4:
            main(OrdonnancementSSIInsertionRegret, taxis_ct, env_size, task_freq, task_method, tasks_ct, total_time, taxi_random_location)
        

        elif value == 5:
            compare_main(OrdonnancementSSIInsertion, OrdonnancementSSIInsertionRegret, taxis_ct, env_size, task_freq, task_method, tasks_ct, total_time, taxi_random_location)

        elif value == 6:
            main(OrdonnancementPSI, taxis_ct, env_size, task_freq, task_method, tasks_ct, total_time, taxi_random_location)
        
        elif value == 7:
            compare_main(OrdonnancementSSIInsertion, OrdonnancementPSI, taxis_ct, env_size, task_freq, task_method, tasks_ct, total_time, taxi_random_location)
        
        elif value == 8:
            main(OrdonnancementDCOPSimple, taxis_ct, env_size, task_freq, task_method, tasks_ct, total_time, taxi_random_location)

        elif value == 9:
            break

        elif value == 10:
            reps = int(input("Reps : "))

            print("1 : Ordonnancement SSI Insertion")
            print("2 : Ordonnancement SSI Insertion Regret")
            print("3 : Ordonnancement PSI")

            algodx = int(input("Algo : "))
    
            algo = None

            if algodx == 1:
                algo = OrdonnancementSSIInsertion
            elif algodx == 2:
                algo = OrdonnancementSSIInsertionRegret
            elif algodx == 3:
                algo = OrdonnancementPSI
            else:
                print("Error")

            multi_main(reps, algo, taxis_ct, env_size, task_freq, task_method, tasks_ct, total_time, taxi_random_location)

        else:
            print("Valeur incorrecte")


desk()