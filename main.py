from PyQt5.QtWidgets import *
from PyQt5 import uic
from time import sleep
from os import system
import pyttsx3

class MyGUI(QMainWindow):
    def __init__(self):
        super(MyGUI, self).__init__()
        self.engine = pyttsx3.init() # object creation

        try: uic.loadUi("main.ui", self); system("cls")
        except FileNotFoundError: 
            print("File Not Found")
            print("Please visit https://github.com/OZX-OG/learn-english To download file 'main.ui'")
            sleep(10)
            exit()

        self.setWindowTitle("Learn English - by: OZX-OG")
        # self.setWindowIcon(QIcon("icon.png"))
        self.setFixedSize(655, 319)

        ################### Hide elem ###################
        self.lbl_word.hide()
        self.lbl_lenwords.hide()
        self.lbl_mode.hide()
        self.txtbox_word.hide()
        self.btn_stop.hide()
        self.btn_select_mode.hide()
        self.btn_hear.hide()
        self.btn_help.hide()
        self.lbl_help.hide()
        

        ################### show app ###################
        self.show()

        ################### connect ###################
        self.btn_mode_english.clicked.connect(self.mode_english)
        self.btn_mode_arabic.clicked.connect(self.mode_arabic)
        self.btn_mode_english_voice.clicked.connect(self.mode_english_voice)
        self.btn_select_mode.clicked.connect(self.select_mode)
        self.btn_stop.clicked.connect(self.stop)
        self.txtbox_word.returnPressed.connect(self.word)
        self.btn_help.clicked.connect(self.help)
        self.btn_hear.clicked.connect(self.hear)
        
        ################### variables ###################
        self.indx_word = 0
        self.b_mode_english = False
        self.b_mode_arabic = False
        self.b_mode_english_voice = False
        self.start_game = True
        self.words = ""
        self.first = True
        self.en_ar_index = 0

    ############## defualt func ##############
    def default(self):
        self.start_game = True
        self.first = True
        self.btn_mode_english.hide()
        self.btn_mode_arabic.hide()
        self.btn_mode_english_voice.hide()

        self.lbl_word.show()
        self.lbl_lenwords.show()
        self.lbl_mode.show()
        self.txtbox_word.show()
        self.btn_select_mode.show()

        self.txtbox_word.setFocus()
        
        try: f = open("words.txt", "r", encoding='UTF-8')
        except FileNotFoundError:
            print("File Not Found")
            print("Please visit https://github.com/OZX-OG/learn-english To download file 'words.txt'")
            print("You Can Add Words If You Want")
            sleep(10); exit()

        x = f.readlines()
        self.words = x

        self.lbl_title.setText("Learning Arabic") if self.b_mode_arabic else self.lbl_title.setText("Learning English")
        self.lbl_mode.setText("Mode : Arabic") if self.b_mode_arabic else self.lbl_mode.setText("Mode : English")

    ############## select mode func ##############
    def select_mode(self):
        self.lbl_word.hide()
        self.lbl_lenwords.hide()
        self.lbl_mode.hide()
        self.txtbox_word.hide()
        self.btn_stop.hide()
        self.btn_select_mode.hide()
        self.btn_hear.hide()
        self.btn_help.hide()
        self.lbl_help.hide()

        self.btn_mode_english.show()
        self.btn_mode_arabic.show()
        self.btn_mode_english_voice.show()


        self.lbl_title.setText("Select Mode")
        self.lbl_word.setText("Let's get Started")
        self.lbl_lenwords.setText("words : 0 / 0")
        self.lbl_help.setText("")
        self.txtbox_word.setText("Perss Enter To Start")
        self.txtbox_word.setStyleSheet("color: rgb(170, 170, 170);")
        self.start_game = True
        self.first = True
        self.t = 0
        self.indx_word = 0

    ############## voice_speach func ##############
    def voice_speach(self):
        self.engine.setProperty('rate', 125)     # setting up new voice rate
        self.engine.setProperty('volume', 0.5)    # setting up volume level  between 0 and 1
        voices = self.engine.getProperty('voices')       #getting details of current voice
        self.engine.setProperty('voice', voices[1].id)
        try: self.engine.say( self.words[self.indx_word].split(":")[0].strip().lower() )
        except IndexError: pass
        self.engine.runAndWait()
        self.engine.stop()
        self.btn_hear.show()



    ############## checking func ##############
    def checking(self, _ , mode: str, voice: bool = False):
        self.txtbox_word.setFocus()
        
        self.en_ar_index = 0 if mode == "arabic" else 1
        if self.first:
            self.lbl_word.setText( self.words[self.indx_word].split(":")[self.en_ar_index].strip().lower()  )
            if voice: self.voice_speach()

            self.first = False

        if self.txtbox_word.text().lower().strip() == self.words[self.indx_word].split(":")[not self.en_ar_index].strip().lower():
            self.txtbox_word.setStyleSheet("color: white")

            self.indx_word += 1
            try: self.lbl_word.setText( self.words[self.indx_word].split(":")[self.en_ar_index].strip().lower() )
            except IndexError: pass
            self.txtbox_word.setText("")
            self.lbl_help.setText("")
        
            if voice: 
                self.voice_speach()


        elif self.start_game:
            self.start_game = False
            self.txtbox_word.setText("")
            self.txtbox_word.setStyleSheet("color: white")
        else:
            self.txtbox_word.setStyleSheet("color: red;")

        if self.indx_word + 1 > len(self.words):
            self.lbl_lenwords.setText(f"words : 0 / 0")
            self.btn_stop.hide()
            self.btn_help.hide()
            self.btn_hear.hide()
            self.lbl_help.hide()
            self.lbl_help.setText("")
            self.lbl_word.setText( "You Finished" )
            self.txtbox_word.setText("Perss Enter To Start Again")
            self.txtbox_word.setStyleSheet("color: rgb(170, 170, 170);")
            self.indx_word = 0
            self.start_game = True
            self.first = True


        self.lbl_lenwords.setText(f"words : {self.indx_word + 1} / { str(len(self.words)) } ")

    ############## word func ##############
    def word(self):
        ### variables
        self.btn_stop.show()
        self.btn_help.show()
        self.lbl_help.show()
        
        
        if self.b_mode_arabic:
            self.checking(self, "arabic")

        elif self.b_mode_english:
            self.checking(self, "english")
            
        elif self.b_mode_english_voice: 
            self.checking(self, "english", True)




    ############## stop_btn func ##############
    def stop(self):
        self.btn_stop.hide()

        self.lbl_word.setText("Let's get Started")
        self.lbl_lenwords.setText("words : 0 / 0")
        self.lbl_help.setText("")
        self.txtbox_word.setText("Perss Enter To Start")
        self.txtbox_word.setStyleSheet("color: rgb(170, 170, 170);")
        self.start_game = True
        self.first = True
        self.indx_word = 0

    ################### mode btns func ###################
    def mode_english(self):
        self.b_mode_arabic = False
        self.b_mode_english = True
        self.b_mode_english_voice = False

        self.txtbox_word.setFocus()
        self.default()

    def mode_arabic(self):
        self.b_mode_arabic = True
        self.b_mode_english = False
        self.b_mode_english_voice = False

        self.txtbox_word.setFocus()
        self.default()

    def mode_english_voice(self):
        self.b_mode_english = False
        self.b_mode_arabic = False
        self.b_mode_english_voice = True

        self.txtbox_word.setFocus()
        self.default()
        
    ############## btn_help func ##############
    def help(self):
        self.lbl_help.setText( self.words[self.indx_word].split(":")[not self.en_ar_index].strip().lower() )

    ############## btn_hear func ##############
    def hear(self):
        self.voice_speach()
        self.txtbox_word.setFocus()

app = QApplication([])
window = MyGUI()
app.exec_()
