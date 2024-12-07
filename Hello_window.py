import io
import os
import sys


from PyQt6 import uic  # Импортируем uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QDialog
from Crypto import Decoder, No_Flash_Drive, No_Key_On_Flash

class Cryptographer_window(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('consts/Main_window.ui', self)  # Загружаем дизайн





