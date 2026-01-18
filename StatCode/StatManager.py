import json
class StatManager:
   data = {}
   encounter = []
   def __init__(self):
    try: 
      with open('..\EnemyData\Enemystats.json','r') as file:
        self.data = json.load(file)
      print("Stats loaded from Database!")
    except FileNotFoundError:
      print ('Error: The file was not found, Please try again.')
      return; 
   def printData(self):
     print("data is : ",self.data)
   
   def inputStat(self):
     print("put in data")
   
   def changeEncounter(self):
     print('encounter menu')
    
   def seeEncounter(self):
     print(self.encounter)