from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
  
import sys

class TextEdit(QWidget):
    def __init__(self, title, width=180, textAlign=Qt.AlignLeft, defaultValue=None):
        QWidget.__init__(self)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        
        self.label = QLabel()
        self.label.setText(title)
        self.label.setFixedWidth(65)
        self.label.setFont(QFont("Arial",weight=QFont.Bold))
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        layout.addWidget(self.label)
        
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setFixedWidth(width)
        self.lineEdit.setAlignment(textAlign)
        if defaultValue != None:
            self.lineEdit.setText(defaultValue)

        layout.addWidget(self.lineEdit)
        layout.addStretch()
    
    def getText(self):
        return self.lineEdit.text()