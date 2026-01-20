from PyQt6.QtGui import  QIntValidator
from PyQt6.QtCore import  Qt
from PyQt6.QtWidgets import QWidget,  QVBoxLayout, QPushButton, QLabel, QGridLayout, QListWidget ,QLineEdit, QComboBox,QListWidgetItem
class BattleManager(QWidget):
     encounterHP = []
     def __init__(self):
       super().__init__()
       Ailments = ["Select Status","NORM",'PARA','CRY','SLEEP','POI','STRANGE','WSTPL', 'SOLID']
       ElemRes = [ 'Select Element','Bash','Fire','Ice','Elec','Bomb']
       self.mainWidget= QVBoxLayout()

       self.enemyBox = QListWidget()
       self.inputWidg = QWidget()

       self.inputs = QGridLayout()
       self.results = QLabel("Battle Results are here.")
       self.initResult = QLabel("Initiative Order is here.")
       self.lucInput = QLineEdit()
       self.lucInput.setValidator(QIntValidator())
       self.lucInput.setPlaceholderText("Enter Player Luck")
       self.dmgInput = QLineEdit()
       self.dmgInput.setValidator(QIntValidator())
       self.dmgInput.setPlaceholderText("Enter Incoming Damage")
       self.initInput = QLineEdit()
       self.initInput.setValidator(QIntValidator())
       self.initInput.setPlaceholderText("Enter Player Initiative")
       self.nameInput = QLineEdit()
       self.nameInput.setPlaceholderText("Enter Player Name")
       self.elemInput = QComboBox()
       self.elemInput.addItems(ElemRes)
       self.ailInput = QComboBox()
       self.ailInput.addItems(Ailments)
       
       self.addInitiativeBut = QPushButton("Add Initiative")
       self.addInitiativeBut.clicked.connect(self.addInit)
       self.rollInitiativeBut = QPushButton("Roll Initiative")
       self.rollInitiativeBut.clicked.connect(self.rollInitiative)
       self.addStatus= QPushButton("Inflict Status")
       self.addStatus.clicked.connect(self.doAilment)
       self.doDamageBut = QPushButton("Inflict Damage (-damage = healing)")
       self.doDamageBut.clicked.connect(self.doDamage)
       
       self.setupLayout()

       self.inputWidg.setLayout(self.inputs)
       self.mainWidget.addWidget(self.enemyBox)
       self.mainWidget.addWidget(self.inputWidg)
       self.setLayout(self.mainWidget)
       
     def setupLayout(self):
        self.inputs.addWidget(self.results,0,0)
        self.inputs.addWidget(self.dmgInput,1,0)
        self.inputs.addWidget(self.elemInput,1,1)
        self.inputs.addWidget(self.doDamageBut,1,2)
        self.inputs.addWidget(self.ailInput,2,0)
        self.inputs.addWidget(self.lucInput,2,1)
        self.inputs.addWidget(self.addStatus,2,2)
        self.inputs.addWidget(self.initResult,3,0)
        self.inputs.addWidget(self.initInput,4,0)
        self.inputs.addWidget(self.addInitiativeBut,4,1)
        self.inputs.addWidget(self.rollInitiativeBut,4,2)

     def importEncounter(self, encData, data):
        self.encounterHp= [] 
        if not encData:
            label = QLabel("Please make or load an encounter First", alignment=Qt.AlignmentFlag.AlignCenter)
            self.mainWidget.addWidget(label)
            return
        
        for item in encData:
            curEnemy = data[item]
            curEnemy['isDef'] = False
            curEnemy['MaxHP']= curEnemy['HP']
            curEnemy['MaxPP']= curEnemy['PP']
            
            self.encounterHP.append(curEnemy)
            listItem = QListWidgetItem()
            wrapperWidg = QWidget()
            gridLay = QGridLayout()
            self.encounterHP.append(data[item])
            gridLay.addWidget(QLabel(f"{curEnemy['name']}"), 0, 0)
            gridLay.addWidget(QLabel(f"HP"), 0, 1)
            gridLay.addWidget(QLabel(f"PP"), 0, 2)
            gridLay.addWidget(QLabel(f"Status"), 0, 3)
            gridLay.addWidget(QLabel(f"{curEnemy['HP']}"),1,1)
            gridLay.addWidget(QLabel(f"{curEnemy['PP']}"),1,2)
            gridLay.addWidget(QLabel(f"{curEnemy['Status']}"),1,3)
            wrapperWidg.setLayout(gridLay)
            listItem.setSizeHint(wrapperWidg.layout().sizeHint())
            self.enemyBox.addItem(listItem)
            self.enemyBox.setItemWidget(listItem,wrapperWidg)

        print(self.encounterHP)

     def doDamage(self):
         print("damageTime")
         print(self.enemyBox.currentRow())
     def doAilment(self):
         print("AilTime")
     def addInit(self):
         print("addInit")
     def rollInitiative(self): 
         print("rolling")       