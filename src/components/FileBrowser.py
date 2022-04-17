from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
  
import sys
  
# A simple widget consisting of a QLabel, a QLineEdit and a 
# QPushButton. The class could be implemented in a separate 
# script called, say, file_browser.py
class FileBrowser(QWidget):
  
    OpenFile = 0
    OpenFiles = 1
    OpenDirectory = 2
    SaveFile = 3
    
    def __init__(self, title, mode=OpenFile, defaultValue=None):
        QWidget.__init__(self)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.browser_mode = mode
        self.filter_name = 'All files (*.*)'
        self.dirpath = QDir.currentPath()
        
        self.label = QLabel()
        self.label.setText(title)
        self.label.setFixedWidth(65)
        self.label.setFont(QFont("Arial",weight=QFont.Bold))
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        layout.addWidget(self.label)
        
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setFixedWidth(180)
        if defaultValue != None:
            self.lineEdit.setText(defaultValue)

        layout.addWidget(self.lineEdit)
        
        self.button = QPushButton('Search')
        self.button.clicked.connect(self.getFile)
        layout.addWidget(self.button)
        layout.addStretch()

    # For example, 
    #    setMode(FileBrowser.OpenFile)
    #    setMode(FileBrowser.OpenFiles)
    #    setMode(FileBrowser.OpenDirectory)
    #    setMode(FileBrowser.SaveFile)
    def setMode(self, mode):
        self.mode = mode

    # For example, 
    #    setFileFilter('Images (*.png *.xpm *.jpg)')
    def setFileFilter(self, text):
        self.filter_name = text        

    def setDefaultDir(self, path):
        self.dirpath = path

    def getFile(self):
        self.filepaths = []
        
        if self.browser_mode == FileBrowser.OpenFile:
            self.filepaths.append(QFileDialog.getOpenFileName(self, caption='Choose File',
                                                    directory=self.dirpath,
                                                    filter=self.filter_name)[0])
        elif self.browser_mode == FileBrowser.OpenFiles:
            self.filepaths.extend(QFileDialog.getOpenFileNames(self, caption='Choose Files',
                                                    directory=self.dirpath,
                                                    filter=self.filter_name)[0])
        elif self.browser_mode == FileBrowser.OpenDirectory:
            self.filepaths.append(QFileDialog.getExistingDirectory(self, caption='Choose Directory',
                                                    directory=self.dirpath))
        else:
            options = QFileDialog.Options()
            if sys.platform == 'darwin':
                options |= QFileDialog.DontUseNativeDialog
            self.filepaths.append(QFileDialog.getSaveFileName(self, caption='Save/Save As',
                                                    directory=self.dirpath,
                                                    filter=self.filter_name,
                                                    options=options)[0])
        if len(self.filepaths) == 0:
            return
        elif len(self.filepaths) == 1:
            self.lineEdit.setText(self.filepaths[0])
        else:
            self.lineEdit.setText(",".join(self.filepaths))    

    def setLabelWidth(self, width):
        self.label.setFixedWidth(width)    

    def setlineEditWidth(self, width):
        self.lineEdit.setFixedWidth(width)

    def getPaths(self):
        return self.filepaths

    def getFilePath(self):
        return self.lineEdit.text()