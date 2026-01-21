from PyQt6.QtGui import  QIntValidator
import random
from PyQt6.QtCore import  Qt
from PyQt6.QtWidgets import QWidget,  QVBoxLayout, QPushButton, QLabel, QGridLayout, QListWidget ,QLineEdit, QComboBox,QListWidgetItem , QAbstractItemView, QDialog, QVBoxLayout , QPushButton 
class BattleManager(QWidget):
     encounterHP = []
     initGuide = {}
     def __init__(self):
       super().__init__()
       self.Ailments = ["Select Status","Norm",'Paralysis','Crying','Sleep','Poison','Strange','Wall Stapled', 'Solidification', "Def", "NotDef"]
       self.ElemRes = [ 'Select Element','Bash','Fire','Ice','Elec','Bomb']
       self.mainWidget= QVBoxLayout()

       self.enemyBox = QListWidget()
       self.enemyBox.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
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
       self.elemInput.addItems(self.ElemRes)
       self.ailInput = QComboBox()
       self.ailInput.addItems(self.Ailments)
       self.enemyIdInput = QLineEdit()
       self.initInput.setValidator(QIntValidator())

       self.addInitiativeBut = QPushButton("Add Initiative")
       self.addInitiativeBut.clicked.connect(self.addInit)
       self.rollInitiativeBut = QPushButton("Roll Initiative")
       self.rollInitiativeBut.clicked.connect(self.rollInitiative)
       self.addStatus= QPushButton("Inflict Status")
       self.addStatus.clicked.connect(self.doAilment)
       self.doDamageBut = QPushButton("Inflict Damage (-damage = healing)")
       self.doDamageBut.clicked.connect(self.doDamage)
       self.addEnemyBut = QPushButton("Add Enemy")
       self.addEnemyBut.clicked.connect(self.addEnemyToEncounter)
       self.clearInitBut =  QPushButton("Clear Init")
       self.clearInitBut.clicked.connect(self.clearInit)

       self.errLabel = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
       self.setupLayout()

       self.inputWidg.setLayout(self.inputs)
       
       self.mainWidget.addWidget(self.enemyBox)
       self.mainWidget.addWidget(self.inputWidg)
       self.mainWidget.addWidget(self.errLabel)
       self.setLayout(self.mainWidget)
       
     def setupLayout(self):
        #setups the layout for the input area.
        self.inputs.addWidget(self.results,0,0)
        self.inputs.addWidget(self.dmgInput,1,0)
        self.inputs.addWidget(self.elemInput,1,1)
        self.inputs.addWidget(self.doDamageBut,1,2)
        self.inputs.addWidget(self.ailInput,2,0)
        self.inputs.addWidget(self.lucInput,2,1)
        self.inputs.addWidget(self.addStatus,2,2)
        self.inputs.addWidget(self.initResult,3,0)
        self.inputs.addWidget(self.initInput,4,0)
        self.inputs.addWidget(self.nameInput,4,1)
        self.inputs.addWidget(self.addInitiativeBut,4,2)
        self.inputs.addWidget(self.rollInitiativeBut,4,3)
        self.inputs.addWidget(self.clearInitBut,4,4)
        self.inputs.addWidget(self.enemyIdInput,5,0)
        self.inputs.addWidget(self.addEnemyBut,5,1)
        

     def importEncounter(self, encData, data):
        self.data = data
        self.encounterHP = [] 
        self.encounterList = encData
        self.enemyBox.clear()
        self.name_counts = {}
        if not self.encounterList:

            self.errLabel.setText("Please make or load an encounter First")
            return

        for item in self.encounterList:
            self.populateList(item)

     def populateList(self, item):
        curEnemy = self.data[item].copy()
        curEnemy['isDef'] = False
        curEnemy['MaxHP']= curEnemy['HP']
        curEnemy['MaxPP']= curEnemy['PP']
        #This is to give numbering to duplicate enemies in an encounter.
        base_name = curEnemy['name']
        if base_name in self.name_counts:
            self.name_counts[base_name] += 1
            display_name = f"{base_name} {self.name_counts[base_name]}"
        else:
            self.name_counts[base_name] = 1
            display_name = base_name
        curEnemy['display_name'] = display_name
        #add in the grids to the enemylist since it looks preetier 
        self.encounterHP.append(curEnemy)
        listItem = QListWidgetItem()
        wrapperWidg = QWidget()
        gridLay = QGridLayout()
        gridLay.addWidget(QLabel(display_name), 0, 0)
        gridLay.addWidget(QLabel(f"HP"), 0, 1)
        gridLay.addWidget(QLabel(f"PP"), 0, 2)
        gridLay.addWidget(QLabel(f"Hit/Dodge"), 0, 3)
        gridLay.addWidget(QLabel(f"SMASH"), 0, 5)
        gridLay.addWidget(QLabel(f"Status"), 0, 4)
        gridLay.addWidget(QLabel(f"{curEnemy['HP']}"),1,1)
        gridLay.addWidget(QLabel(f"{curEnemy['PP']}"),1,2)
        gridLay.addWidget(QLabel(f"{curEnemy['SPD']//13}"),1,3)
        gridLay.addWidget(QLabel(f"{curEnemy['Status']}"),1,4)
        gridLay.addWidget(QLabel(f"{curEnemy['GUT']}"),1,5)
        wrapperWidg.setLayout(gridLay)
        listItem.setSizeHint(wrapperWidg.layout().sizeHint())
        self.enemyBox.addItem(listItem)
        self.enemyBox.setItemWidget(listItem,wrapperWidg)
        print(self.encounterHP)

     def doDamage(self):
         #applies the damage formulas to enemies
         print("damageTime")
         targets = ""
         toDelete = []
         for x in self.enemyBox.selectionModel().selectedRows():
            index = x.row()
            print("index "+f'{index}')
            curitem = self.encounterHP[index]
            damageCalc = int(self.dmgInput.text())
            element = self.elemInput.currentText()
            if element == "Bash":
                damageCalc = (damageCalc - curitem['DEF'])
                if(curitem["isDef"]):#defending calculations
                    damageCalc = damageCalc // 2
            elif element in self.ElemRes[2:]:#elemental attack calculations according to rules right now
                damageCalc = int(damageCalc * curitem[f'{element}Res'])
            if(int(self.dmgInput.text()) > 0 and damageCalc <= 0):
                damageCalc = 1
            targets+=f'{curitem["display_name"]}, '
            self.encounterHP[index]["HP"] -= damageCalc
            print(self.encounterHP[index]["HP"])
            print(damageCalc)
            if self.encounterHP[index]["HP"] <= 0:
                #mark entries as delete for later since it causes issues during the loop.
                toDelete.append(index)
            else:
                if(self.encounterHP[index]["HP"] >self.encounterHP[index]["MaxHP"]): 
                    #make sure enemies can't go over their maxHP Value
                    self.encounterHP[index]["HP"] =  self.encounterHP[index]["MaxHP"]
                widget = self.enemyBox.itemWidget(self.enemyBox.item(index))
                hp_label = widget.layout().itemAtPosition(1, 1).widget()
                hp_label.setText(str(self.encounterHP[index]["HP"]))
         #Reverse sort so bigger indexes are first to prevent further issues
         toDelete.sort(reverse=True)
         
         for index in toDelete:
             self.encounterList.pop(index)
             self.encounterHP.pop(index)
             self.enemyBox.takeItem(index)
         self.results.setText(f'{targets.rstrip(", ")} took {damageCalc} damage!')

             

     def doAilment(self):
         print("AilTime")
         luck = self.lucInput.text()
         if luck:
             luck = int(luck)
         else:
             luck = 0
         success = ""
         failed = ""
         ailment = self.ailInput.currentText()
         possibleAil = ['Paralysis','Crying','Sleep','Poison','Strange','Wall Stapled', 'Solidification']
         #set enemies to defending
         if ailment == "Def":
            for x in self.enemyBox.selectionModel().selectedRows():
                index = x.row()
                curitem = self.encounterHP[index]
                curitem["Def"] = True
                success+=f'{curitem["display_name"]}, '
            self.results.setText(f'{success.rstrip(", ")} Put their Guard up!')
            return
         #Turn off Defending 
         elif ailment == "NotDef":
            for x in self.enemyBox.selectionModel().selectedRows():
                index = x.row()
                curitem = self.encounterHP[index]
                curitem["Def"] = False
                success+=f'{curitem["display_name"]}, '
            self.results.setText(f'{success.rstrip(", ")} stopped Defending')
            return 
         ailmentSubStr = ailment[0:3]+"Res"
         if ailment in possibleAil:
             
            for x in self.enemyBox.selectionModel().selectedRows():
                index = x.row()
                curitem = self.encounterHP[index]
                ailmentRes = curitem[ailmentSubStr]
                if ailmentRes == 0:
                    failed+=f'{curitem["display_name"]}, '
                    continue
                check = self.rollDie(1,20)+ (curitem["IQ"]//(2**ailmentRes)) - luck
                if(check<20):
                    success += f'{curitem["display_name"]}, '
                    widget = self.enemyBox.itemWidget(self.enemyBox.item(index))
                    status_label = widget.layout().itemAtPosition(1, 4).widget()
                    status_label.setText(ailment)
                else:
                    failed += f'{curitem["display_name"]}, '
         else:
            for x in self.enemyBox.selectionModel().selectedRows():
                index = x.row()
                curitem = self.encounterHP[index]
                success += f'{curitem["display_name"]}, '
                widget = self.enemyBox.itemWidget(self.enemyBox.item(index))
                status_label = widget.layout().itemAtPosition(1, 4).widget()
                status_label.setText(ailment)
         final = ""
         if success:
             final += f'{success.rstrip(", ")} has {ailment}!'
         if failed:
             final+= f'{failed.rstrip(", ")} is unaffected!'
         self.results.setText(f'{success.rstrip(", ")} has {ailment}! {failed.rstrip(", ")} is unaffected!')        
            
            

     def rollDie(self, times, maxVal):
         total = 0
         for i in range(times):
             total+= random.randint(1,maxVal)
         return total

     def addInit(self):
         init = 0
         if self.initInput.text():
             init = int ( self.initInput.text())
         self.initGuide[f'{self.nameInput.text()}']  = init

     def rollInitiative(self):
         outcome = ""
         for item in self.encounterHP:
             self.initGuide[ item['display_name']] = (self.rollDie(1,20)+(item['SPD']//2))
         sorted_items = sorted(self.initGuide.items(), key=lambda x: x[1], reverse=True)
         print(self.initGuide)
         for index, (name, init_val) in enumerate(sorted_items, 1):
             outcome += f'{index}. {name}\n'
         self.initResult.setText(outcome)

     def clearInit(self):
         
         self.initGuide={}
         self.initResult.setText("")

     def addEnemyToEncounter(self):
         if(self.enemyIdInput.text()):
             self.populateList(self.enemyIdInput.text())