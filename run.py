#!/usr/bin/env python

# ___        AlarmPi V 1.1.1 by nickpettican            ___
# ___   Your smart alarm clock for the Raspberry Pi     ___

# ___        Copyright 2017 Nicolas Pettican            ___

# ___    This software is licensed under the Apache 2   ___
# ___    license. You may not use this file except in   ___
# ___    compliance with the License.                   ___
# ___    You may obtain a copy of the License at        ___

# ___    http://www.apache.org/licenses/LICENSE-2.0     ___

# ___    Unless required by applicable law or agreed    ___
# ___    to in writing, software distributed under      ___
# ___    the License is distributed on an "AS IS"       ___
# ___    BASIS, WITHOUT WARRANTIES OR CONDITIONS OF     ___
# ___    ANY KIND, either express or implied. See the   ___
# ___    License for the specific language governing    ___
# ___    permissions and limitations under the License. ___

from PyQt4 import QtCore, QtGui #PyQt4 is used for designing the GUI
from time import strftime # To get time from Raspberry pi
from alarmpi import Alarmpi
import sys
from sys import platform
import random, time, os

'''
Bellow you can enter your credentials
in order to personalise your AlarmPi.

Explanation:

Alarmpi(owner = 'your name/nickname',               # name by which it will greet you
        tune = True or False,                       # enable or disable alarm tune
        voice_female = True or False or name,       # make the voice female or give specific name
        voice_male = True or False or name,         # make the voice male or give specific name
        auth = 'your Ivona auth key',               # Ivona auth key
        auth_secret = 'your Ivona auth secret',     # Ivona auth secret key
        weather = True or False,                    # turn weather forecasting on / off
            weather_auth='your Open Weather auth',  # Open Weather auth code for weather
            city='London',                          # Your city name
            country_code='uk',                      # Your country 2 character code
        news = True or False,                       # turn news telling on / off
            world_news = True or False,             # enable / disable world news
            uk_news = True or False,                # enable / disable UK news
            health_news = True or False,            # enable / disable UK medical news
            tech_news = True or False,              # enable / disable UK tech news
            science_news = True or False)           # enable / disable UK science news

'''

app_directory = '/home/pi/Alarm-Pi2'


def main():
    # --- ENTER YOUR PERSONAL CREDENTIALS BELLOW ---
    global alarmpi
    alarmpi = Alarmpi(  owner = 'Ian',
                        app_dir = app_directory,
                        tune = True,
                        voice_female = 'Joanna',
                        voice_male = False,
                        weather = True,
                            weather_auth='236adfa20ec34eb04cdfbacfabf9b5e0',
                            city='New London',
                            country_code='us',
                        news = False,
                            world_news = False,
                            country_news = True,
                            health_news = True,
                            tech_news = True,
                            science_news = False)
    
    if alarmpi.tune:
        alarmpi.alarm_sound()

    time.sleep(10)
    
    alarmpi.main()
        
    
#Code from Qt Designer
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.alarm_h = 0
        self.alarm_m = 0
        
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(676, 439)
        
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.centralwidget)
        
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)
        
        self.Time_LCD = QtGui.QLCDNumber(self.centralwidget)
        self.Time_LCD.setObjectName(_fromUtf8("Time_LCD"))
        self.Time_LCD.setDigitCount(8)
        self.Time_LCD.display(strftime("%H"+":"+"%M"+":"+"%S")) #get time from Pi and display it 
        self.gridLayout.addWidget(self.Time_LCD, 1, 0, 1, 3)
        self.timer = QtCore.QTimer(MainWindow)
        self.timer.timeout.connect(self.Time)
        self.timer.start(1000)
        
        current_time = QtCore.QTime()
        self.Set_Time = QtGui.QTimeEdit(self.centralwidget)
        self.Set_Time.setObjectName(_fromUtf8("Set_Time"))
        self.Set_Time.setTime(current_time.currentTime())
        self.gridLayout.addWidget(self.Set_Time, 2, 0, 1, 1)
        
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton.clicked.connect(self.button_pressed)
        self.gridLayout.addWidget(self.pushButton, 2, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 676, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
#End of code from Qt Designer
        
    def retranslateUi(self, MainWindow): #update the GUI window 
        print("Dispay Re-translated")
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "Alarm is currently Turned off", None))
        self.pushButton.setText(_translate("MainWindow", "Set Alarm", None))
    
    def Time(self): #Function to compare current time with set time 
        self.Time_LCD.display(strftime("%H"+":"+"%M"+":"+"%S"))
        self.current_h = int (strftime("%H"))
        self.current_m = int (strftime("%M"))
        if (self.current_h == self.alarm_h) and (self.current_m == self.alarm_m) and ((int(strftime("%S"))%15) == 0): #if the both time match 
            message1 = " The time is " + str(self.alarm_h) + " : " + str(self.alarm_m) + " on " + strftime("%A")
            message2 = "Alarm is currently turned off"
            self.label.setText(_translate("MainWindow",message1, None)) #display the message on GUI screen  
##            espeak.synth (message) #speak the message through audio jack
                # --- turn speakers on ---
            if 'linux' in platform:
                os.system(app_directory + '/audio_output/./AUDIO_JACK.sh')
            main()
            time.sleep(5*random.random())
            self.label.setText(_translate("MainWindow",message2, None))
             # --- turn speakers off ---
            if 'linux' in platform:
                os.system(app_directory + '/audio_output/./HDMI_out.sh')
            
    def button_pressed(self): #when set alarm button is pressed 
        print("Button Pressed")
        alarm_time = self.Set_Time.time()
        alarm_time_hour = alarm_time.hour()
        alarm_time_minute = alarm_time.minute()
        alarm_time = str(self.Set_Time.time())
        
        self.alarm_h = int(alarm_time_hour)
        self.alarm_m = int (alarm_time_minute) 
        message = "Alarm is set at " + str(self.alarm_h) + " hours " + str(self.alarm_m) + " minutes"
        self.label.setText(_translate("MainWindow", message, None)) #display the message on GUI screen  
##        espeak.synth (message) #speak the message through audio jack 
        



if __name__ == "__main__":
    

    
    # --- main function ---
##    main()
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
   
    
    

    

        

        
    

    