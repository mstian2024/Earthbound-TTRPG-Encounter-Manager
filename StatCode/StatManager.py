import json
from PyQt6.QtCore import *
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import *
class StatManager(QWidget):
   loadedData = {}
   encounter = []
   def __init__(self):
      super().__init__()
      self.title = "Stat Manager"
      button = QPushButton("Press Me!")
      button.clicked.connect(self.inputStat)
      #set layout
      layout = QVFormLayout()
      #input to get name 
      layout.addWidget(button)
      self.setLayout(layout)
      #add all rows to form

   def getFileData(self,filePath):
      #add way to check if file is formatted correctly.
      try: 
        with open(filePath,'r', encoding='utf-8') as file:
          if filePath.endswith('.json'):
            self.loadedData = json.load(file)
            print("Stats loaded from Database!")
            return self.loadedData
          else:
            print ('Error: The file is not a .json file, Please try again.')
            return
      except FileNotFoundError:
        print ('Error: The file was not found, Please try again.')
        return
      except json.JSONDecodeError:
        # Handle cases where the JSON in the file is invalid
        print(f"Error decoding JSON from file: {filePath}")
        return

   def inputStat(self):
      print("Input Stat Function")
    
