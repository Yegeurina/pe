import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from Generate import pe_generator

class App(QWidget) :
    def __init__(self) :
        super().__init__()
        self.initUI()

    def initUI(self) :
        self.setWindowTitle('PE Generator_by _Yeah_Jin')
        self.center()
        self. resize(500,360)

        #set line
        line =  QFrame(self)
        line.setGeometry(QRect(150,20,20,280))
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)

        #set font
        Labelfont = QFont()
        Labelfont.setFamily("굴림")
        Labelfont.setPointSize(12)
        Labelfont.setBold(True)
        font = QFont()
        font.setFamily("굴림")
        font.setPointSize(12)

        #EntryPoint
        Label_EP = QLabel('EntryPoint',self)
        Label_EP.setGeometry(QRect(40,20,90,30))
        Label_EP.setFont(Labelfont)
        self.EP = QTextEdit(self)
        self.EP.setGeometry(QRect(180,20,300,30))
        self.EP.setFont(font)

        #ImageBase
        Label_IB = QLabel('ImageBase',self)
        Label_IB.setGeometry(QRect(40,80,90,30))
        Label_IB.setFont(Labelfont)
        self.IB = QTextEdit(self)
        self.IB.setGeometry(QRect(180,80,300,30))
        self.IB.setFont(font)

        #Section Alignment
        Label_SA = QLabel('Section Alignment',self)
        Label_SA.setGeometry(QRect(10,140,150,30))
        Label_SA.setFont(Labelfont)
        self.SA = QTextEdit(self)
        self.SA.setGeometry(QRect(180,140,300,30))
        self.SA.setFont(font)

        #File Alignment
        Label_FA = QLabel('File Alignment',self)
        Label_FA.setGeometry(QRect(25,200,150,30))
        Label_FA.setFont(Labelfont)
        self.FA = QTextEdit(self)
        self.FA.setGeometry(QRect(180,200,300,30))
        self.FA.setFont(font)
        
        #How Many?
        Label_HM = QLabel('How Many?',self)
        Label_HM.setGeometry(QRect(30,260,150,30))
        Label_HM.setFont(Labelfont)
        self.HM = QTextEdit(self)
        self.HM.setGeometry(QRect(180,260,300,30))
        self.HM.setFont(font)

        # 생성 버튼 정의
        btn = QPushButton("Create",self)
        #btn.move(10,250)
        btn.setGeometry(QRect(10,320,480,30))
        btn.clicked.connect(self.btn_clicked)

    def btn_clicked(self) :
        try :
            val_ep = int(self.EP.toPlainText(),16)
            val_ib = int(self.IB.toPlainText(),16)
            val_sa = int(self.SA.toPlainText(),16)
            val_fa = int(self.FA.toPlainText(),16)
            val_hm = int(self.HM.toPlainText())

            if not (val_ib >= int('00000000',16) and val_ib<=int('FFFFFFFF',16)):
                QMessageBox.about(self,"Warnint","ImageBase의 범위가 잘못되었습니다.(0~FFFFFFFF)")
            elif not ((val_sa & (val_sa-1))==0 and val_sa>=1 and val_sa>=val_fa) :
                QMessageBox.about(self,"Warnint","Section Alignment가 잘못되었습니다.(2의 n승으로 구성되어야 함) 또한 File Alignment보다 크거나 같아야 합니다.")
            elif not ((val_fa & (val_fa-1))==0 and val_fa>=1)  :
                QMessageBox.about(self,"Warnint","File Alignment가 잘못되었습니다.(2의 n승으로 구성되어야 함)")
            elif val_hm<=0:
                QMessageBox.about(self,"Warnint","생성되는 파일은 1개 이상이어야 합니다.")
            else :
                msg = "EntryPoint : " + hex(val_ep) \
                    +"\nImageBase : " + hex(val_ib)\
                    +"\nSection Aligment : " + hex(val_sa)\
                    +"\nFile Aligmnet : " + hex(val_fa)\
                    +"\nHow Many : " + str(val_hm)

                QMessageBox.about(self, "message", msg)
                
                ge = pe_generator(val_ep,val_ib,val_sa,val_fa)
                for i in range(0,val_hm) :
                    ge.run()

        except Exception as e:
            #입력되지 않은 값이 존재할 경우
            QMessageBox.about(self, "Warning", str(e))


    def center(self) :
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__' :
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    app.exec_()
