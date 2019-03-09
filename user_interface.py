
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QMessageBox, QPushButton, QLineEdit
import sys
from PyQt5.QtGui import QPixmap
import os
import Run

cwd = os.getcwd()


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "Crowd Copter"
        self.top = 100
        self.left = 100
        self.width = 1500
        self.height = 900


        self.InitWindow()


    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon(cwd+"\\icon.ico"))
        self.label1 = QLabel("Select Sector", self)
        self.label1.move(50,50)

        self.label = QLabel(self)
        self.label.setPixmap(QPixmap(cwd+"\\frame70.jpg"))
        self.label.setGeometry(300,0,1280,720)

        self.linedit = QLineEdit(self)
        self.linedit.move(50,100)
        self.linedit.resize(100,40)

        self.button = QPushButton("Select", self)
        self.button.move(50,150)
        self.button.clicked.connect(self.onClick)
        
        self.button = QPushButton("Run", self)
        self.button.move(50,200)
        self.button.clicked.connect(self.OpenClick)

        
        self.button = QPushButton("show result", self)
        self.button.move(50,250)
        self.button.clicked.connect(self.OClick)

        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

    def onClick(self):
        textValue = self.linedit.text()
        QMessageBox.question(self, "Line Edit", "You Have Choose " + textValue,QMessageBox.Ok, QMessageBox.Ok)

    def OpenClick(self):
        Run.USER()

    def OClick (self):
        self.label.setPixmap(QPixmap(cwd+"\\result.jng"))
        



App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())

        



