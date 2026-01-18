
from StatManager import StatManager
# Defining main function
def main():
    EnemyData= StatManager()
    while(True):
        param = input('''What would you like to do?
                      1: get stat data
                      2: put in stat data (Tedious)
                      3: change encounter
                      4: see Encounter
                      5: change HP Values
                      6: leave''')
        if param == '1':
            EnemyData.printData() 
        elif param == '2':
            EnemyData.inputStat()
        elif param == '3':
            EnemyData.changeEncounter
               
    


# Using the special variable 
# __name__
if __name__=="__main__":
    main()