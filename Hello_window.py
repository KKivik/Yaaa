import io
import os
import sys


from PyQt6 import uic  # Импортируем uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QDialog, QMessageBox, QDialogButtonBox, QComboBox
from Crypto import Decoder, No_Flash_Drive, No_Key_On_Flash

class Dialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('consts/Dialog.ui', self)
        self.comboBox.addItem('C')
        self.comboBox.addItem('F')
        self.comboBox.addItem('G')
        self.comboBox.addItem('D')
        self.comboBox.addItem('M')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Dialog()
    ex.show()
    sys.exit(app.exec())
