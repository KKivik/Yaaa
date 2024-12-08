import io
import os
import sys


from PyQt6 import uic  # Импортируем uic
from PyQt6.QtWidgets import QApplication, QWidget, QFileDialog, QListWidget
from PyQt6.QtGui import QIcon
from Crypto import Decoder, No_Flash_Drive, No_Key_On_Flash
from Hello_window import Dialog
from Main_window_UI import Ui_Form

class Cryptographer_window(QWidget, Ui_Form):
    def __init__(self, *args):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Cryptography")
        self.setWindowIcon(QIcon('images/ico.png'))
        self.dialog = Dialog()
        self.letter = self.dialog.exec()
        self.drive_letter = self.dialog.index

        self.select_folder.clicked.connect(self.selecting_folder)
        self.encode_button.clicked.connect(self.encoding_select)
        self.decode_button.clicked.connect(self.decoding_select)
        self.fname = ''

    def selecting_folder(self):
        self.fname = QFileDialog.getExistingDirectory(self, 'Выберите папку')
        if self.fname != '' and self.status.text() != '':
            self.status.setText('')

    def encoding_select(self):
        if self.fname == '':
            self.status.setText('Выберите папку!')
            self.status.setStyleSheet("font: 15pt Comic Sans MS")
            self.listWidget.clear()
            self.listWidget.addItem('Ошибка')
        else:
            try:
                self.listWidget.clear()
                self.Encryptor = Decoder(self.fname, True, self.drive_letter)
                self.listWidget.addItems(self.Encryptor.list)
            except No_Flash_Drive:
                self.listWidget.clear()
                self.listWidget.addItem('Ошибка')
                self.status.setText('Вставьте флешку')
                self.status.setStyleSheet("font: 15pt Comic Sans MS")
            else:
                self.status.setText('Успешно')
                self.status.setStyleSheet("font: 15pt Comic Sans MS")

    def decoding_select(self):
        if self.fname == '':
            self.status.setText('Выберите файл!')
            self.status.setStyleSheet("font: 15pt Comic Sans MS")
        else:
            try:
                self.listWidget.clear()
                self.Encryptor = Decoder(self.fname, False, self.drive_letter)
                self.listWidget.addItems(self.Encryptor.list)

            except No_Flash_Drive:
                self.listWidget.clear()
                self.listWidget.addItem('Ошибка')
                self.status.setText('Вставьте флешку')
                self.status.setStyleSheet("font: 15pt Comic Sans MS")
            except No_Key_On_Flash:
                self.listWidget.clear()
                self.listWidget.addItem('Ошибка')
                self.status.setText('На флешке отсутствует ключ')
                self.status.setStyleSheet("font: 15pt Comic Sans MS")
            else:
                self.status.setText('Успешно')
                self.status.setStyleSheet("font: 15pt Comic Sans MS")

    def except_hook(cls, exception, traceback):
        sys.__excepthook__(cls, exception, traceback)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Cryptographer_window()
    ex.show()
    sys.exit(app.exec())
