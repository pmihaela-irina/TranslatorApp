from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QApplication, QPushButton, QTextEdit, QVBoxLayout, QComboBox, QMessageBox, QMainWindow, \
    QStyle
from PyQt5 import uic
from PyQt5.QtCore import Qt, QUrl
from playsound import playsound
from gtts import gTTS
import sys
import os
import googletrans
import json
import speech_recognition as sr


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # Load the ui file
        uic.loadUi("translate.ui", self)
        self.setWindowTitle("Translator App")

        # read json file
        self.file = self.readFile()

        # define our widgets
        self.translate_button = self.findChild(QPushButton, "pushButton_translate")
        self.clear_button = self.findChild(QPushButton, "pushButton_clear")
        self.soundLang1_button = self.findChild(QPushButton, "pushButton_soundLang1")
        self.soundLang2_button = self.findChild(QPushButton, "pushButton_soundLang2")
        self.record_button = self.findChild(QPushButton, "pushButton_record")
        # set color for buttons
        self.translate_button.setStyleSheet(
            "background-color : " + self.file['dark_blue'] + "; color : " + self.file['light_blue'])
        self.clear_button.setStyleSheet(
            "background-color : " + self.file['dark_blue'] + "; color : " + self.file['light_blue'])
        self.soundLang1_button.setStyleSheet(
            "background-color : " + self.file['light_blue1'])
        self.soundLang2_button.setStyleSheet(
            "background-color : " + self.file['light_blue1'])
        self.record_button.setStyleSheet(
            "background-color : " + self.file['light_blue1'])

        #set icons for buttons
        self.soundLang1_button.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
        self.soundLang2_button.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
        self.record_button.setIcon(QIcon('mic_icon.png'))

        self.lang1_comboBox = self.findChild(QComboBox, "comboBox_lang1")
        self.lang2_comboBox = self.findChild(QComboBox, "comboBox_lang2")
        # TODO fix scoll bar for comboBoxes
        self.lang1_comboBox.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.lang2_comboBox.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.text1_textEdit = self.findChild(QTextEdit, "textEdit")
        self.text2_textEdit = self.findChild(QTextEdit, "textEdit_2")

        # click the buttons
        self.translate_button.clicked.connect(self.translate)
        self.clear_button.clicked.connect(self.clear)
        self.soundLang1_button.clicked.connect(lambda: self.textToSpeech(self.text1_textEdit, self.lang1_comboBox,
                                                                         self.soundLang1_button))
        self.soundLang2_button.clicked.connect(lambda: self.textToSpeech(self.text2_textEdit,
                                                                         self.lang2_comboBox,
                                                                         self.soundLang2_button))
        self.record_button.clicked.connect(self.record)

        # add lang to the combo boxes
        self.languages = googletrans.LANGUAGES
        # print(self.languages)

        # convert to list
        self.language_list = list(self.languages.values())
        # print(self.language_list)

        # add items to combo boxes
        self.lang1_comboBox.addItems(self.language_list)
        self.lang2_comboBox.addItems(self.language_list)

        # set default combo item
        self.lang1_comboBox.setCurrentText("romanian")
        self.lang2_comboBox.setCurrentText("english")

        self.player = QMediaPlayer()

    def clear(self):
        #playsound('zapsplat_multimedia_button_click_fast_short_002_79286.mp3')
        full_file_path = os.path.join(os.getcwd(),'zapsplat_multimedia_button_click_fast_short_002_79286.mp3')
        url = QUrl.fromLocalFile(full_file_path)
        content = QMediaContent(url)
        self.player.setMedia(content)
        self.player.play()
        # clear the text boxes
        self.text1_textEdit.setText("")
        self.text2_textEdit.setText("")

        # reset the combo boxes
        self.lang1_comboBox.setCurrentText("romanian")
        self.lang2_comboBox.setCurrentText("english")

    def translate(self):
        try:
            #playsound('zapsplat_multimedia_button_click_fast_short_002_79286.mp3')
            full_file_path = os.path.join(os.getcwd(), 'zapsplat_multimedia_button_click_fast_short_002_79286.mp3')
            url = QUrl.fromLocalFile(full_file_path)
            content = QMediaContent(url)
            self.player.setMedia(content)
            self.player.play()
            # get original language key
            for key, value in self.languages.items():
                if value == self.lang1_comboBox.currentText():
                    from_language_key = key

            # get translated language key
            for key, value in self.languages.items():
                if value == self.lang2_comboBox.currentText():
                    to_language_key = key

            # self.text1_textEdit.setText(from_language_key)
            # self.text2_textEdit.setText(to_language_key)

            # translate words
            translator = googletrans.Translator()
            words = translator.translate(self.text1_textEdit.toPlainText(), src=from_language_key, dest=to_language_key)

            # output text
            self.text2_textEdit.setPlainText(words.text)
            # playsound('https://kstatic.googleusercontent.com/files/c69e6ccd8c737fa86fe5447bfe8c819ca32f1c920663223730dc2ddb5cf4d6b9aa8d94c88717cb999e7e0a2291e2d63e84e67b2a452b7ec52275f487f896f884')

        except Exception as e:
            # playsound('zapsplat_multimedia_game_error_tone_002_24920.mp3')
            full_file_path = os.path.join(os.getcwd(), 'zapsplat_multimedia_game_error_tone_002_24920.mp3')
            url = QUrl.fromLocalFile(full_file_path)
            content = QMediaContent(url)
            self.player.setMedia(content)
            self.player.play()

            QMessageBox.about(self, "Translator", str(e))
            print(e)

    def textToSpeech(self, text_textEdit, language_comboBox, sound_button):
        try:
            # playsound('zapsplat_multimedia_button_click_fast_short_002_79286.mp3')
            full_file_path = os.path.join(os.getcwd(), 'zapsplat_multimedia_button_click_fast_short_002_79286.mp3')
            url = QUrl.fromLocalFile(full_file_path)
            content = QMediaContent(url)
            self.player.setMedia(content)
            self.player.play()
            
            sound_button.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
            sound_button.repaint()
            text = text_textEdit.toPlainText()
            for key, value in self.languages.items():
                if value == language_comboBox.currentText():
                    from_language_key = key

            myobj = gTTS(text=text, lang=from_language_key)

            # Saving the converted audio in a mp3 file
            myobj.save("play_sound.mp3")
            playsound('play_sound.mp3')
            sound_button.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
            os.remove('play_sound.mp3')
        except Exception as e:
            #self.soundLang1_button.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
            sound_button.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
            playsound('zapsplat_multimedia_game_error_tone_002_24920.mp3')
            QMessageBox.about(self, "Translator", str(e))

    def speechToText(self, recognizer, microphone,  to_language_key):
        with microphone as source:
            # recognizer.pause_threshold = 1
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, phrase_time_limit=3)

        response = {
            "success": True,
            "error": None,
            "transcription": None
        }

        try:
            response["transcription"] = recognizer.recognize_google(audio, language=to_language_key)
        except sr.RequestError:
            response["success"] = False
            response["error"] = "API unavailable"
        except sr.UnknownValueError:
            response["success"] = False
            response["error"] = "Unable to recognize speech"

        return response

    def record(self):
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()

        for key, value in self.languages.items():
            if value == self.lang1_comboBox.currentText():
                to_language_key = key

        translator = googletrans.Translator()
        words = translator.translate('Speak now..', src='en', dest=to_language_key)
        print(words.text)
        self.text1_textEdit.setPlainText(words.text)
        quitFlag=True
        while quitFlag:
            text = self.speechToText(recognizer, microphone, to_language_key)
            if not text["success"] and text["error"] == "API unavailable":
                self.text1_textEdit.setPlainText("ERROR: {}\nclose program".format(text["error"]))
                self.text1_textEdit.repaint()
                sys.exit()
            while not text["success"]:
                print("I didn't catch that. What did you say?\n")
                self.text1_textEdit.setPlainText(translator.translate("I didn't catch that. What did you say?\n", src='en', dest=to_language_key).text)
                self.text1_textEdit.repaint()
                text = self.speechToText(recognizer, microphone, to_language_key)

            if text["transcription"].lower() == "exit":
                quitFlag = False

            print(text["transcription"].lower())
            self.text1_textEdit.setPlainText(text["transcription"].lower())
            self.text1_textEdit.repaint()

    def readFile(self):
        # JSON file
        f = open('color.json', "r")
        # Reading from file
        data = json.loads(f.read())
        f.close()
        return data


# initialize the app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = UI()
    UIWindow.show()
    sys.exit(app.exec_())
