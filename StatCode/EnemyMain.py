
from StatManager import StatManager
from EncounterManager import EncounterManager
import os
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QHBoxLayout, QFormLayout, QStackedWidget, QListWidget, QWidget, QLabel, QMainWindow, QApplication, QFileDialog
import sys
# Defining main function
class main(QMainWindow):
    data = {}
    def __init__(self):
        super().__init__()
        self.statManager = StatManager()
        self.encounterManager = EncounterManager()
        self.setWindowTitle("Enemy Stat Manager")
        self.setMinimumSize(QSize(500,500))
        # Set the central widget of the Window.
        self.label = QLabel("Please input in a file.", alignment=Qt.AlignmentFlag.AlignTop)
        self.parentLayout = QHBoxLayout()
        self.widgetStack = QStackedWidget()
        self.widgetStack.addWidget(self.label)
        self.widgetStack.addWidget(self.statManager)
        self.widgetStack.addWidget(self.encounterManager)
        openButton = QAction("Open Json", self)
        openButton.triggered.connect(self.file_open)
        openButton.setCheckable(False)

        addButton = QAction("Add New", self)
        addButton.triggered.connect(self.add_new)
        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        file_menu.addSection("File Operations")
        file_menu.addAction(addButton)
        file_menu.addAction(openButton)

        encounter_menu = menu.addMenu("&Encounter")
        encounter_menu.addAction("EncounterMenus", self.change_encounter)
        self.parentLayout.addWidget(self.widgetStack)
        self.setLayout(self.parentLayout)
        self.setCentralWidget(self.widgetStack)
    def file_open(self):
        print("File Opened")
        HOME_PATH = os.path.abspath(os.getcwd())+"/EnemyData"
        fName = QFileDialog.getOpenFileName(
            parent=self,
            caption="Select directory",
            directory=HOME_PATH,
            options=QFileDialog.Option.DontUseNativeDialog,
            filter="JSON Files (*.json)"
        )
        self.data = self.statManager.getFileData(fName[0])
        self.encounterManager.getData(self.data)
        self.label.setText("File Loaded")
    def add_new(self):
        print("Add New File")
        self.widgetStack.setCurrentIndex(1)
        
    def change_encounter(self):
        print("Change Encounter")
        self.widgetStack.setCurrentIndex(2)
        self.encounterManager.getData(self.data)
# Using the special variable
# __name__
if __name__=="__main__":
    app = QApplication(sys.argv)
    window = main()
    window.show()
    sys.exit(app.exec())