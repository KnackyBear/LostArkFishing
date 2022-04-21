import sys
import os
import pyautogui

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from components.FileBrowser import FileBrowser
from components.TextEdit import TextEdit
from LostArkFishing import LostArkFishing

class Windows(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.screenWidth, self.screenHeight = pyautogui.size()
        self.setWindowTitle('LostArk Fishing')
        self.setGeometry(100,100, 200, 500)
        self.initSettingsGroupBox()
        self.initOutputGroupBox()
        vbox = QVBoxLayout()
        vbox.addWidget(self.outputGroupBox, 2)
        vbox.addWidget(self.settingsGroupBox)
        self.setLayout(vbox)

        self.btnStart.clicked.connect(self.start)
        self.btnStop.clicked.connect(self.stop)

        self.show()

    def initSettingsGroupBox(self):
        self.settingsGroupBox = QGroupBox('Settings')
        self.settingsGroupBox.setStyleSheet('QGroupBox {border: 1px solid gray; margin-top: 0.5em;}'
                                            'QGroupBox::title {subcontrol-origin: margin; subcontrol-position: top center; padding: 0 3px;}')
        self.settingsGroupBox.setTitle('Settings')
        
        defaultPath = os.path.normcase(f"{os.getcwd()}/resources/{self.screenHeight}")
        self.fb_asset = FileBrowser("Assets dir.", FileBrowser.OpenDirectory, defaultValue=defaultPath)
        self.txt_float_fishing_bind = TextEdit("Float fishing", width=25, textAlign=Qt.AlignHCenter, defaultValue="e")
        self.txt_throw_bait_bind = TextEdit("Throw bait", width=25, textAlign=Qt.AlignHCenter, defaultValue="d")
        self.txt_energy = TextEdit("Energy", width=50, textAlign=Qt.AlignLeft, defaultValue="10500")
        self.chk_autorepair = QCheckBox("Auto repair", self)
        self.txt_autorepair = TextEdit("Every", width=25, textWith=30, textAlign=Qt.AlignLeft, defaultValue="50")

        vbox = QVBoxLayout()
        vbox.addWidget(self.fb_asset)

        gbox = QGridLayout()
        gbox.addWidget(self.txt_float_fishing_bind, 1, 1)
        gbox.addWidget(self.txt_throw_bait_bind, 1, 2, 1, 2)
        gbox.addWidget(self.txt_energy, 2, 1)
        gbox.addWidget(self.chk_autorepair, 2, 2)
        gbox.addWidget(self.txt_autorepair, 2, 3, Qt.AlignLeft)
        vbox.addLayout(gbox)


        self.btnStart = QPushButton('Start')
        self.btnStop = QPushButton('Stop')
        self.btnStop.setEnabled(False)

        hbox_btn = QHBoxLayout()
        hbox_btn.addWidget(self.btnStart)
        hbox_btn.addWidget(self.btnStop)

        vbox.addStretch()
        vbox.addLayout(hbox_btn)
        self.settingsGroupBox.setLayout(vbox)
        self.settingsGroupBox.show()

    def initOutputGroupBox(self):
        self.outputGroupBox = QGroupBox('Output')
        self.outputGroupBox.setStyleSheet('QGroupBox {border: 1px solid gray; margin-top: 0.5em;}'
                                          'QGroupBox::title {subcontrol-origin: margin; subcontrol-position: top center; padding: 0 3px;}')
        self.outputGroupBox.setTitle('Output')
        self.initLogOuputTextEdit()
        vbox = QVBoxLayout()
        vbox.addWidget(self.logOutputTextEdit)
        self.outputGroupBox.setLayout(vbox)
        self.outputGroupBox.show()

    def initLogOuputTextEdit(self):
        self.logOutputTextEdit = QTextEdit()
        self.logOutputTextEdit.setGeometry(10, 10, 200, 200)
        self.logOutputTextEdit.setStyleSheet('QTextEdit {border: 1px solid gray; margin-top: 0.5em;}')
        self.logOutputTextEdit.setReadOnly(True)

    def message(self, value):
        self.logOutputTextEdit.appendPlainText(str(value) + "\n")

    def start(self):
        self.btnStart.setEnabled(False)
        self.btnStop.setEnabled(True)
        self.thread = LostArkFishing(fish_key=self.txt_float_fishing_bind.getText(), 
                                     bait_key=self.txt_throw_bait_bind.getText(), 
                                     energy=self.txt_energy.getText(), 
                                     autorepair=self.chk_autorepair.isChecked(), 
                                     roundrepair=self.txt_autorepair.getText(),
                                     assetPath=self.fb_asset.getFilePath())
        self.thread.loggerSignal.connect(self.on_thread_signal_logging)
        self.thread.endSignal.connect(self.stop)
        self.thread.start()

        #lostArkFishing = LostArkFishing(self.logger)
        #lostArkFishing.execute()
    
    def stop(self):
        self.btnStart.setEnabled(True)
        self.btnStop.setEnabled(False)
        self.thread.terminate()

    def on_thread_signal_logging(self, value):
        self.logOutputTextEdit.insertPlainText(str(value) + "\n")
        self.logOutputTextEdit.verticalScrollBar().setValue(self.logOutputTextEdit.verticalScrollBar().maximum())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Windows()
    sys.exit(app.exec_())

