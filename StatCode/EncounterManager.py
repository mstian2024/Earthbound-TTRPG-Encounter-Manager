
from PyQt6.QtCore import  Qt
from PyQt6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QPushButton, QLabel, QStackedLayout, QGridLayout, QListWidget
from BattleManager import BattleManager
class EncounterManager(QWidget):
   data = {}
   EnemyDb = {}
   encounter = []
   def __init__(self):
       super().__init__()
       self.tabLayout = QStackedLayout()
       self.beforeLayout = QWidget()
       self.afterLayout = QStackedWidget()
       self.encScreen = QWidget()
       button1 =QPushButton("Change Encounter")
       button1.clicked.connect(self.changeEncounter)
       self.battleManager = BattleManager()
       simulate =QPushButton("Simulate Encounter")
       simulate.clicked.connect(self.battleSim)

       label = QLabel("Please Load in JSON Data first.", alignment=Qt.AlignmentFlag.AlignCenter)
       self.beforeLayout.setLayout(QVBoxLayout())
       self.beforeLayout.layout().addWidget(label)
       self.encScreen.setLayout(QVBoxLayout())
       self.encScreen.layout().addWidget(button1)
       self.encScreen.layout().addWidget(simulate)
       self.afterLayout.addWidget(self.encScreen)
       self.encounterMaker = QWidget()
       self.enemyBox = QGridLayout()
       self.encounterMaker.setLayout(self.enemyBox)
       self.enemyTabs = QListWidget()
       self.addedBox = QListWidget()

       appendButton = QPushButton("<-- Add Enemy", self)
       appendButton.clicked.connect(self.addToEncounter)

       removeButton = QPushButton("Remove Enemy -->", self)
       removeButton.clicked.connect(self.removeFromEncounter)
       
       SaveEncounter = QPushButton("Save Encounter", self)
       SaveEncounter.clicked.connect(self.saveEncounter)
       ExitButton = QPushButton("Exit", self)
       ExitButton.clicked.connect(self.exitEditor)
       self.enemyBox.addWidget(QLabel("Add enemies to Encounter here."),0,0)
       self.enemyBox.addWidget(QLabel("Enemy List"),0,1)
       self.enemyBox.addWidget(self.addedBox, 1, 0)
       self.enemyBox.addWidget(self.enemyTabs, 1, 1)
       self.enemyBox.addWidget(appendButton, 2, 1)
       self.enemyBox.addWidget(removeButton, 2, 0)
       self.enemyBox.addWidget(SaveEncounter,3,0)
       self.enemyBox.addWidget(ExitButton,3,1)
       self.tabLayout.addWidget(self.beforeLayout)
       self.tabLayout.addWidget(self.afterLayout)
       self.tabLayout.addWidget(self.encounterMaker)
       self.tabLayout.addWidget(self.battleManager)
       self.tabLayout.setCurrentIndex(0)
       self.setLayout(self.tabLayout)
       self.data = {}

   def getData(self,hasData):
      if hasData:
         print('data loaded')
         self.data = hasData
         print(self.afterLayout.indexOf(self.encScreen))
         self.tabLayout.setCurrentIndex(1)
         self.tabLayout.update()
         
   
   def changeEncounter(self):
     print('encounter menu')
     #TODO Move this to another window for convenience
     if len(self.data.keys()) == self.enemyTabs.count():
        self.tabLayout.setCurrentIndex(2)
        return
     for key in self.data.keys():
        if self.data[key]['name'] in self.EnemyDb:
           continue
        self.enemyTabs.addItem(self.data[key]['name'])
        self.EnemyDb[self.data[key]['name']] = key
     self.tabLayout.setCurrentIndex(2)

   def addToEncounter(self):
     enemyName = self.enemyTabs.currentItem().text()
     self.encounter.append(self.EnemyDb[enemyName])
     self.addedBox.addItem(enemyName)
     print(self.encounter)

   def removeFromEncounter(self):
      enemyIndex = self.addedBox.currentRow()
      self.encounter.pop(enemyIndex)
      self.addedBox.takeItem(enemyIndex)
      print(self.encounter)

   def saveEncounter(self):
      self.tabLayout.setCurrentIndex(1)

   def exitEditor(self):
      self.tabLayout.setCurrentIndex(1)
      self.encounter = []
      self.addedBox.clear()
    
   def battleSim(self):
      self.tabLayout.setCurrentIndex(3)
      self.battleManager.importEncounter(self.encounter,self.data)