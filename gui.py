from PyQt5 import QtCore, QtGui, QtWidgets ,QtMultimedia
from PyQt5.QtWidgets import QMessageBox
from scipy.io import wavfile
from numpy import pi, tan
from scipy import signal
from scipy.io import wavfile
import numpy as np
from pathlib import Path

from scipy.signal.wavelets import qmf

"""
HASAN FURKAN BALKAÇ 
150150056

"""
class myFilter():
    def lowpass_filter(data, cutoff, fs):

        """
        Does a lowpass filter over the given data.
        :param data: The data (numpy array) to be filtered.
        :param cutoff: The high cutoff in Hz.
        :param fs: The sample rate in Hz of the data.
        :ORDER OF FILTER = 3
        :returns: Filtered data (numpy array).

        """
        
        angle = (2* pi * cutoff) / fs
        omega = tan (angle/2)
        
        #Array coefficents were calculated in pdf 
        #Functions only calculate the omega value for given frequency and
        #Numerator and Denumerator are calculated depends on this omega value

        num = np.array([ pow(omega,3), pow(omega,3)*3 , pow(omega,3)*3 , pow(omega,3) ])
        dem = np.array([ pow(omega,3) + 2*omega + 3 , -1*omega-1 , -1*omega+1, 3*omega-3 ])

        #print(num)
        #print(dem)

        y = signal.lfilter(num, dem, data)
        return y 
        
    def highpass_filter(data, cutoff, fs):

        """
        Does a highpass filter over the given data.

        :param data: The data (numpy array) to be filtered.
        :param cutoff: The low cutoff in Hz.
        :param fs: The sample rate in Hz of the data.
        :param order: The order of the filter. The higher the order, the tighter the roll-off.
        :ORDER OF FILTER = 3
        :returns: Filtered data (numpy array).
        """
        #nyq = 0.5 * fs
        #omega = cutoff / nyq
        
        angle = (2* pi * cutoff) / fs
        omega = tan (angle/2)
        
        #Array coefficents were calculated in pdf 
        #Functions only calculate the omega value for given frequency and
        #Numerator and Denumerator are calculated depends on this omega value

        num = np.array([ 1, -3 , 3 , -1 ])
        dem = np.array([ pow(omega,3) + 4*omega + 1 , 3*pow(omega,3) -3 , 3*pow(omega,3)-4*omega+3, pow(omega,3)-1 ])

        #print(num)
        #print(dem)

        y = signal.lfilter(num, dem, data)
        return y 

    def bandpass(data, fcl,fch, fs):

        filtered_data = myFilter.highpass_filter(data,fcl,fs)
        filtered_data = myFilter.lowpass_filter(data,fch,fs)

        return filtered_data

    def bandstop( data,fcl,fch,fs ):

        filtered_data = myFilter.highpass_filter(data,fcl,fs)
        filtered_data = myFilter.lowpass_filter(data,fch,fs)
        filtered_data = data - filtered_data 

        return filtered_data

class Ui_MainWindow(QtWidgets.QMainWindow):

    samplerate, data = 0,0
    f_low,f_high = 0,0
    FILEPATH = ""

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(450, 400)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(70, 190, 95, 20))
        self.radioButton.setObjectName("radioButton")
        

        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_2.setGeometry(QtCore.QRect(200, 190, 95, 20))
        self.radioButton_2.setObjectName("radioButton_2")
        
        """
        # PLAY BUTTON
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(70, 250, 131, 61))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.play)
        """

        # SAVE BUTTON
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(240, 250, 131, 61))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.save)
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(70, 70, 191, 81))
        font = QtGui.QFont()
        font.setPointSize(10)
        
        self.label.setFont(font)
        self.label.setObjectName("label")
        
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(70, 130, 131, 21))
        self.lineEdit.setObjectName("lineEdit")
        
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(240, 70, 191, 81))
        
        font = QtGui.QFont()
        font.setPointSize(10)
        
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(240, 130, 131, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        
        #Choosing Directory for wav BUTTON
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(70, 40, 151, 31))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.get_wav_file)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "FILTER GUI"))
        self.radioButton.setText(_translate("MainWindow", "Band Pass"))
        self.radioButton_2.setText(_translate("MainWindow", "Band Stop"))
        #self.pushButton.setText(_translate("MainWindow", "Play"))
        self.pushButton_2.setText(_translate("MainWindow", "Save"))
        self.label.setText(_translate("MainWindow", "Central frequency"))
        self.label_2.setText(_translate("MainWindow", "the Bandwidth"))
        self.pushButton_3.setText(_translate("MainWindow", "Choose .wav File"))

    """
    def play(self):
        print("Play button")
        central_freq = int(self.lineEdit.text())
        bandwith = int(self.lineEdit_2.text())
        print(central_freq, bandwith)
    """
        
    def save(self):
        #print("Save button")
        try:
            central_freq = int(self.lineEdit.text())
            bandwith = int(self.lineEdit_2.text())
            self.frequency_calculate(central_freq,bandwith)
        except:
            self.errorPopUp()
        #print(central_freq, bandwith)
        if self.radioButton.isChecked(): #BANDPASS RADIO BUTTON SELECTED
            #print("bandpass_selected")
            #print(self.f_low, self.f_high) 
            try:
                filtered_data = myFilter.bandpass(self.data,self.f_low,self.f_high,self.samplerate)
                path = Path(self.FILEPATH)
                wavfile.write(str(path.parent) + "/"+ path.stem +"2.wav",self.samplerate,filtered_data.astype(np.int16))
                self.savePopUp()
            except:
                self.errorPopUp()
        elif self.radioButton_2.isChecked(): #BANDSTOP RADIO BUTTON SELECTED
            #print("bandstop_selected")
            #print(self.f_low, self.f_high)
            try:
                filtered_data = myFilter.bandstop(self.data,self.f_low,self.f_high,self.samplerate)
                path = Path(self.FILEPATH)
                wavfile.write(str(path.parent) + "/"+ path.stem +"2.wav",self.samplerate,filtered_data.astype(np.int16))
                self.savePopUp()
            except:
                self.errorPopUp()

        else:
            self.errorPopUp()

        
    def get_wav_file(self):
        #print("Choosen file")
        file_name = QtWidgets.QFileDialog.getOpenFileName(self,"Select wav File",'/',filter="Sound Files (*.wav)")   
        if file_name[0]:
            self.FILEPATH = file_name[0]
            #print(file_name)
            self.samplerate, self.data  = wavfile.read(file_name[0])
            #print(self.samplerate, self.data)
            
    def frequency_calculate(self,central_freq, bandwith):    
        difference = central_freq * (bandwith / 100)
        self.f_low = central_freq - difference # this freq will be lower, but it is used for high pass side 
        self.f_high = central_freq + difference # this freq will be higher. but it is used for low pass side
        #print("f_low = ",self.f_low, "f_high = ",self.f_high)
       

    def savePopUp(self):
        msg = QMessageBox()
        msg.setWindowTitle("SAVE SUCCESS")
        path = Path(self.FILEPATH)
        filename = path.stem
        path = str(path.parent) #we got only directory file 
        msg.setText(filename + "2.wav " + "saved in " + path)
        x = msg.exec_()


    def errorPopUp(self):
        msg = QMessageBox()
        msg.setWindowTitle("WRONG INPUT")
        msg.setText("""Some cause an ERROR. It may be because of 
                    WRONG TYPE INPUT,
                    EMPTY INPUT FIELD, 
                    NON SELECTED RADIO TYPE or 
                    NOT CHOOSING .wav file.""")
        msg.setIcon(QMessageBox.Critical)
        x = msg.exec_()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
