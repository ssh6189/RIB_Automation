if __name__ == '__main__':
    from PySide2.QtCore import QCoreApplication
    QCoreApplication.setLibraryPaths(['C:/Users/cai-kvm-8/anaconda3/envs/yolov5/Lib/site-packages/pyside2/plugins'])
    

from PySide2.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QPushButton, QGraphicsView, QGraphicsItem 
from PySide2.QtWidgets import QWidget, QFileDialog

from PySide2.QtGui import QPixmap, QImage
import sys
from main_ui import Ui_MainWindow
from Result import Ui_Result
import main_v2 as m2
import webbrowser
import os


class Result(QWidget, Ui_Result):
    def __init__(self):
        super().__init__()
        """
        Ui 설정
        """
        self.setupUi(self)
        
        x1 = ""
        x2 = ""
        x3 = ""
        
        for i in result_1:
            x1 = x1 + str(i)
            x1 = x1 + "\n"
            
        for j in result_2:
            x2 = x2 + str(j)
            x2 = x2 + "\n"
            
        for k in result_3:
            x3 = x3 + str(k)
            x3 = x3 + "\n"
            
            
        self.Result_DB1.setText(x1)
        self.Result_DB1.show()
        self.Result_DB2.setText(x2)
        self.Result_DB2.show()
        self.Result_DB3.setText(x3)
        self.Result_DB3.show()
        
class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Ui 클래스 상속
    """
    
    def __init__(self):
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
        
        self.CAI.load("CAILAB.png")
        self.CAI = self.CAI.scaled(261, 101)
        self.CAILAB.setPixmap(self.CAI)
        
        self.Load1.clicked.connect(self.Load1Clicked)
        self.Load2.clicked.connect(self.Load2Clicked)
        self.Predict.clicked.connect(self.PredictClicked)
        self.Tin.clicked.connect(self.TinClicked)

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
    
    #열기
    def open(self):
        fileName, _ = QFileDialog.getOpenFileName(self,
                            "Open Image File",".","Images (*.png *.xpm *.jpg)") 
        if fileName != "":
            self.load(fileName)
            
        return fileName

    #로드
    def load(self, fileName):
        image = QImage(fileName)
        if image.isNull():
            QMessageBox.information(self,QApplication.applicationName(),
                                    "Cannot load "+fileName)
    def result_show(self):
        global result
        result = 0
        result = Result()
        result.show()
        
    #늑근 자동화 도면해석 실행    
    def PredictClicked(self):
        global result
        result = 0
        
        global result_1
        global result_2
        global result_3
        
        result_1 = []
        result_2 = []
        result_3 = []
        
        bujae = str(os.path.dirname(image1))
        gujo = str(os.path.dirname(image2))
        
        sr, gujo_list = m2.main_analisys(bujae, gujo)
        
        for sr in gujo_list:
            if len(sr) == 3:
                for sizes in sr[2]:
            #print(sr[0], sr[1], sizes)
                    result_1.append(sr[0])
                    result_2.append(sr[1])
                    result_3.append(sizes)
                    
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