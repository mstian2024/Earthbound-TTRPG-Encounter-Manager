
from StatManager import StatManager
import os
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QHBoxLayout, QFormLayout, QStackedWidget, QListWidget, QWidget, QLabel, QMainWindow, QApplication, QFileDialog
import sys
# Defining main function
class main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.statManager = StatManager()
        self.statManager.show()
        self.setWindowTitle("Enemy Stat Manager")
        self.setMinimumSize(QSize(500,500))
        # Set the central widget of the Window.
        self.label = QLabel("Please input in a file.", self)
        self.widgetStack = QStackedWidget()
        self.widgetStack.addWidget(self.label)
        self.widgetStack.addWidget(self.statManager)
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
        encounter_menu.addAction("Change Encounter")
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
        print(fName[0])
        self.data = self.statManager.getFileData(fName[0])
        self.label.setText("File Opened")
    def add_new(self):
        print("Add New File")
        self.widgetStack.setCurrentIndex(1)
        self.setCentralWidget(self.widgetStack)
# Using the special variable
# __name__
if __name__=="__main__":
    app = QApplication(sys.argv)
    window = main()
    window.show()
    app.exec()