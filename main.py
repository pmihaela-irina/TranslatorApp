import sys
import json

from PyQt5.QtWidgets import QApplication, QPushButton, QTextEdit, QVBoxLayout
from PyQt5.QtWidgets import QWidget


class TextEditDemo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.file = self.readFile()
        self.setWindowTitle("QTranslator")
        self.resize(600, 470)
        self.move(360, 15)
        self.setStyleSheet("background-color: " + self.file['light_blue'])

        self.textEdit1 = QTextEdit()
        self.textEdit2 = QTextEdit()
        self.btnPress1 = QPushButton("Translate")
        #self.btnPress2 = QPushButton("Button 2")

        layout = QVBoxLayout()
        layout.addWidget(self.textEdit1)
        layout.addWidget(self.textEdit2)
        layout.addWidget(self.btnPress1)
        #layout.addWidget(self.btnPress2)
        self.setLayout(layout)

        self.btnPress1.setStyleSheet("background-color : " + self.file['dark_blue'] + "; color : " + self.file['light_blue'])
        #self.btnPress2.setStyleSheet("background-color : " + self.file['dark_blue'])
        self.btnPress1.clicked.connect(self.btnPress1_Clicked)
        #self.btnPress2.clicked.connect(self.btnPress2_Clicked)

    def btnPress1_Clicked(self):
        text = self.textEdit1.toPlainText()
        self.textEdit2.setPlainText(text)

    def btnPress2_Clicked(self):
        self.textEdit1.setHtml("<font color=" + self.file['blue'] + " size='3'><red>Hello PyQt5!</font>")
    def readFile(self):
        # JSON file
        f = open('color.json', "r")

        # Reading from file
        data = json.loads(f.read())

        print(data['dark'])
        f.close()
        return data

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = TextEditDemo()
    window.show()

    sys.exit(app.exec_())
