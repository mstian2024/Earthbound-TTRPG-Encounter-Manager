import json
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QAction, QIcon , QIntValidator, QDoubleValidator
from PyQt6.QtWidgets import  QWidget, QPushButton, QLineEdit, QVBoxLayout, QFormLayout, QGridLayout, QLabel, QComboBox ,QFileDialog
import os

class StatManager(QWidget):
   loadedData = {}
   encounter = []
   filePath = ""
   id = 1
   def __init__(self):
      super().__init__()
      self.title = "Stat Manager"
      button = QPushButton("Press Me!")
      button.clicked.connect(self.inputStat)
      #set layout

      self.bigLayout = QVBoxLayout()
      self.bigLayout.setSpacing(0)
      self.layout1 = QFormLayout()
      self.statLayout = QGridLayout()
      self.elementLayout = QGridLayout()
      self.ailmentLayout = QGridLayout()
      resistances = ['NORMAL','WEAK','STRONG','IMMUNE']
      StatValues = ['HP' ,'PP','OFF','DEF','IQ','SPD']
      ElemRes = ['Fire','Ice','Elec','Bomb']
      Ailments = ['Paralysis','Crying','Sleep','Poison','Strange','Wall Staples', 'Solidification']
      self.instructions = QLabel("Input Monster Stats Below:\nAny blank fields will default to 1. \nelemental resistance is what the damage will be multiplied by.\nNames are required.")
      #input to get name
      self.error = QLabel("")

      self.monName = QLineEdit()
      self.monName.setPlaceholderText("Enter Monster Name")
      self.monDesc = QLineEdit()
      self.monDesc.setPlaceholderText("Enter Monster Description")

      i = 0
      for stat in StatValues:
         self.statLayout.addWidget(QLabel(f"{stat}:"), 0, i)

         lineEdit = QLineEdit()
         lineEdit.setValidator(QIntValidator())
         self.statLayout.addWidget(lineEdit, 1, i)
         i += 1
      i = 0
      for elem in ElemRes:
          self.elementLayout.addWidget(QLabel(f"{elem}"), 0, i)
          lineEdit = QLineEdit()
          lineEdit.setValidator(QDoubleValidator())
          self.elementLayout.addWidget(lineEdit, 1, i)
          i += 1
      i = 0
      for ail in Ailments:
          self.ailmentLayout.addWidget(QLabel(f"{ail} Res:"), 0, i)
          lineEdit = QComboBox()
          lineEdit.addItems(resistances)
          self.ailmentLayout.addWidget(lineEdit, 1, i)
          i += 1
  
      submitButton = QPushButton("Submit Stats")
      submitButton.clicked.connect(self.inputStat)
      #add all rows to form

      self.layout1.addRow(self.instructions)
      self.layout1.addRow(self.error)
      self.layout1.addRow("Monster Name:",self.monName)
      self.layout1.addRow("Monster Description:",self.monDesc)

      self.bigLayout.addLayout(self.layout1)
      self.bigLayout.addWidget(QLabel("Stats:"))
      self.bigLayout.addLayout(self.statLayout)
      self.bigLayout.addWidget(QLabel("Elemental Resistances:"))
      self.bigLayout.addLayout(self.elementLayout)
      self.bigLayout.addWidget(QLabel("Ailment Resistances:"))
      self.bigLayout.addLayout(self.ailmentLayout)
      self.bigLayout.addWidget(submitButton)
      self.setLayout(self.bigLayout)

   def getFileData(self,filePath):
      #add way to check if file is formatted correctly.
      try: 
        with open(filePath,'r') as file:
          if filePath.endswith('.json'):
            self.loadedData = json.load(file)
            self.filePath = filePath
            self.id = int(list(self.loadedData.keys())[-1]) + 1
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
      if name := self.monName.text() == "":
         print("Error: Name field is required.")
         self.error.setText("Error: Name field is required.")
         return
      name = self.monName.text()
      desc = self.monDesc.text()
      stats =[]
      for i in range(6):
          widget = self.statLayout.itemAtPosition(1, i).widget()
          if isinstance(widget, QLineEdit):
              stats.append(widget.text() if widget.text() else 1)
      elements =[]
      for i in range(4):
          widget = self.elementLayout.itemAtPosition(1, i).widget()
          if isinstance(widget, QLineEdit):
              elements.append(widget.text() if widget.text() else 1)
      ailments =[]
      for i in range(7):
          widget = self.ailmentLayout.itemAtPosition(1, i).widget()
          if isinstance(widget, QComboBox):
              if widget.currentText() == 'STRONG':
                  ailments.append(1)
              elif widget.currentText() == 'NORMAL':
                  ailments.append(2)
              elif widget.currentText() == 'WEAK':
                  ailments.append(3)
              elif widget.currentText() == 'IMMUNE':
                  ailments.append(0)
              else:
                ailments.append(2)
      outData = {
         "name": name,
         "description": desc,
         "HP": stats[0],
         "PP": stats[1],
         "OFF": stats[2],
         "DEF": stats[3],
         "IQ": stats[4],
         "SPD": stats[5],
         "FireRes": elements[0],
         "IceRes": elements[1],
         "ElecRes": elements[2],
         "BombRes": elements[3],
         "ParaRes": ailments[0],
         "CryRes": ailments[1],
         "BraRes": ailments[4],
         "SleRes": ailments[2],
         "PoiRes": ailments[3],
         "WalRes": ailments[5],
         "SolRes": ailments[6]
      }
      print(outData)
      print("Input Stat Function")
      if self.filePath == "":
         HOME_PATH = os.path.abspath(os.getcwd())+"/EnemyData"
         fName = QFileDialog.getSaveFileName(
            parent=self,
            caption="Select directory",
            directory=HOME_PATH,
            options=QFileDialog.Option.DontUseNativeDialog,
            filter="JSON Files (*.json)"
        )
         self.filePath = fName[0]+'.json'
         self.id = 1
      outData = {self.id: outData}
      self.loadedData.update(outData)
      self.writeData(self.loadedData)
  
   def writeData(self,dataToWrite):
      try:
         with open(self.filePath,'w') as file:
            json.dump(dataToWrite,file, indent=4)
            print("Data written to file successfully.")
            self.id+=1
      except Exception as e:
         print(f"An error occurred while writing to the file: {e}")

    
