from PySide2.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QPushButton, QGraphicsView, QGraphicsItem, QLabel
from PySide2.QtWidgets import QWidget, QFileDialog, QLineEdit
from PySide2 import QtGui
from PySide2.QtGui import QPixmap, QImage, QIcon
import sys
from main_ui import Ui_MainWindow
from Result import Ui_Result
from Save import Ui_Save
from state import Ui_Wait
import webbrowser
import serial
import pickle
import time
import os

import Read_and_Send as RaS
import Controll_PLC as CPLC
import machine_init as mci

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Result(QWidget, Ui_Result):
    def __init__(self):
        global x1
        global x2
        global x3
        
        super().__init__()
        """
        Ui 설정
        """
        self.setupUi(self)
        
        self.Save.clicked.connect(self.Save_Window)
        
        x1 = ""
        x2 = ""
        x3 = ""
        
        for i in r1:
            x1 = x1 + i
            x1 = x1 + "\n"
            
        for j in r2:
            x2 = x2 + str(j)
            x2 = x2 + "\n"
            
        for k in r3:
            x3 = x3 + str(k)
            x3 = x3 + "\n"
            
        self.Result_DB1.setText(x1)
        self.Result_DB1.show()
        self.Result_DB2.setText(x2)
        self.Result_DB2.show()
        self.Result_DB3.setText(x3)
        self.Result_DB3.show()
        
        op = x3
        #ser.write(op.encode())
        #print("R: ", ser.readline())
    
    def Save_Window(self):
        global save
        
        save = 0
        save = Save()
        save.show()
        
class Save(QWidget,Ui_Save):
    def __init__(self):
        super().__init__()
        """
        Ui 설정
        """
        self.setupUi(self)
        """
        버튼 클릭 시그널에 슬롯 추가
        """
        self.pushButton_1.clicked.connect(self.Save_Yes)
        self.pushButton_2.clicked.connect(self.Save_No)
        
    def Save_Yes(self):
        fw = open("./Predict_Save/Stirrup_{0}.txt".format(time.time()), 'w')
        fw.write(str(r1) + "\n")
        fw.write(str(r2) + "\n")
        fw.write(str(r3) + "\n")
        fw.close()
            
        self.hide()

        
    def Save_No(self):
        self.hide()
        
class State(QWidget, Ui_Wait):
    def __init__(self):
        super().__init__()
        """
        Ui 설정
        """
        self.setupUi(self)
        """
        버튼 클릭 시그널에 슬롯 추가
        """
        self.Left.clicked.connect(self.CW)
        self.Right.clicked.connect(self.CCW)
        self.Okay.clicked.connect(self.OK)
        self.Stop.clicked.connect(self.Stop_Rotation)
        
    def CW(self):
        mci.rw('W', 612, 2, PN)
        
    def CCW(self):
        mci.rw('W', 612, 1, PN)
        
    def OK(self):
        fileName = self.txtopen()
        file = str(fileName)
        LP = CPLC.chuchul(file)
        LP = CPLC.pick_number(LP)
        LP = CPLC.transpormation(LP)
        CPLC.trasport(LP, PN)
        
        return 0
    
    def Stop_Rotation(self):
        mci.rw('W', 612, 0, PN)
        
        #LP = CPLC.chuchul(file)
        #LP = CPLC.pick_number(LP)
        #LP = CPLC.transpormation(LP)
        #CPLC.trasport(LP, PN)
        
    #텍스트파일열기
    def txtopen(self):
        fileName, _ = QFileDialog.getOpenFileName(self,
                            "Open txt File",".","Predict_Result (*.txt)") 
        if fileName != "":
            self.txtload(fileName)
            
        return fileName
    
    #텍스트파일로드        
    def txtload(self, fileName):
        fileName = open(fileName, 'r')
        with fileName:
            fileName = fileName.read()
        
        #if fileName.isNull():
        #    QMessageBox.information(self,QApplication.applicationName(),
        #                            "Cannot load "+fileName)
        
class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Ui 클래스 상속
    """
    
    def __init__(self):
        global PN
        super().__init__()
        """
        Ui 설정
        """
        self.setupUi(self)
        """
        버튼 클릭 시그널에 슬롯 추가
        """
        
        #QPixmap 객체 생성
        self.image1 = QPixmap()
        self.image2 = QPixmap()
        self.CAI = QPixmap()
        self.TinLogo = QPixmap()
        
        CAILAB_Logo = resource_path("C:/Users/user/Desktop/RIB_Auto/image/CAILAB.png")
        self.CAI.load(CAILAB_Logo)
        self.CAI = self.CAI.scaled(261, 81)
        self.CAILAB.setPixmap(self.CAI)
        
        Tin_Logo = resource_path("C:/Users/user/Desktop/RIB_Auto/image/T_in_Robotics.png")
        self.TinLogo.load(Tin_Logo)
        self.TinLogo = self.TinLogo.scaled(261, 121)
        self.Tin_Logo.setPixmap(self.TinLogo)

        #PN = self.PortNumber.text()
        #PN = str(PN)
        #self.PortNumber.setPlaceholderText("Set your password")
        #self.PortNumber.setEchMode(QLineEdit.Password);
        
        self.Load1.clicked.connect(self.Load1Clicked)
        self.Load2.clicked.connect(self.Load2Clicked)
        self.Predict.clicked.connect(self.PredictClicked)
        self.Tin.clicked.connect(self.TinClicked)
        self.Launch_PLC.clicked.connect(self.Launch_PLC_On_clicked)
        
        #버튼에 이미지 넣기
        pixmap = QPixmap(Tin_Logo)
        button_icon = QIcon(pixmap)
        self.Tin.setIcon(button_icon)
        
        
    #부재리스트 도면 업로드
    def Load1Clicked(self):
        global image1
        image1 = self.open()
        image1 = str(image1)
        self.image1.load(image1)
        self.image1 = self.image1.scaled(261, 192)
        self.Display1.setPixmap(self.image1)
        return image1

    #구조평면도 도면 업로드
    def Load2Clicked(self):
        global image2
        image2 = self.open()
        image2 = str(image2)
        self.image2.load(image2)
        self.image2 = self.image2.scaled(261, 192)
        self.Display2.setPixmap(self.image2)
        return image2
    
    def Launch_PLC_On_clicked(self):
        global PN
        global state
        global LP
        
        self.PortNumber.setRange(1,9)
        PN = self.PortNumber.value()
            
        state = 0
        state = State()
        state.show()
        
        return 0
    
    #열기
    def open(self):
        fileName, _ = QFileDialog.getOpenFileName(self,
                            "Open Image File",".","Images (*.png *.xpm *.jpg)") 
        if fileName != "":
            self.load(fileName)
            
        return fileName
    
    #텍스트파일열기
    def txtopen(self):
        fileName, _ = QFileDialog.getOpenFileName(self,
                            "Open txt File",".","Predict_Result (*.txt)") 
        if fileName != "":
            self.txtload(fileName)
            
        return fileName

    #로드
    def load(self, fileName):
        image = QImage(fileName)
        if image.isNull():
            QMessageBox.information(self,QApplication.applicationName(),
                                    "Cannot load "+fileName)
            
    def txtload(self, fileName):
        fileName = open(fileName, 'r')
        with fileName:
            fileName = fileName.read()
        
        #if fileName.isNull():
        #    QMessageBox.information(self,QApplication.applicationName(),
        #                            "Cannot load "+fileName)
            
    #늑근 자동화 도면해석 실행    
    def PredictClicked(self):
        
        global r1
        global r2
        global r3
        global result
        
        r1 = ['1b6', '1g2', '1b1', '1b1', '1b5']
        r2 = [4553, 3426, 5789, 7773, 7353]
        r3 = [{'a1':1, 'b1':2}, {'a2':3, 'b2':4}, {'a3':5, 'b3':6}, {'a4':7, 'b4':8}, {'a5':9, 'b5':10}]
        
        result = 0
        result = Result()
        result.show()
        #sys.exit(app.exec_())
    
    #트인 홈페이지 접속
    def TinClicked(self):
        url = 'http://t-in.co.kr/'
        webbrowser.open(url)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())