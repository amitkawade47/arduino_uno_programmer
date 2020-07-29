
import sys, subprocess
import serial.tools.list_ports
from PySide2.QtWidgets  import QApplication, QMainWindow, QFileDialog
import time
from mainwindow import Ui_MainWindow

filename = ""
data=""

class mainWindow(QMainWindow,Ui_MainWindow):

    def __init__(self):
        try:
            QMainWindow.__init__(self)
            self.setupUi(self)
            self.setFixedSize(self.size())
            self.connectMe()
            self.getPorts()
        except Exception as e:
            print(e)

    def getPorts(self):
        try:
            port_name=""
            ports = serial.tools.list_ports.comports()
            port_name = [port.device for port in ports]
            self.comboBox.clear()
            self.comboBox.addItems(port_name)
            print(port_name)
        except Exception as e:
            print(e)

    def connectMe(self):
        try:
            self.toolButton.clicked.connect(self.selectFile)
            self.pushButton.clicked.connect(self.programBoard)
            self.pushButton_2.clicked.connect(self.getPorts)
        except Exception as e:
            print(e)

    def selectFile(self):
        global filename,data
        try:
            filepath, filter = QFileDialog.getOpenFileName(parent=self, caption='Open file', dir='.', filter='Hex Files (*.hex)')
            filename = filepath.split("/")[-1]
            self.label.setText(filename)
        except Exception as e:
            print(e)

    def programBoard(self):
        global filename,data
        try:
            port_name = str(self.comboBox.currentText())
            hex_file = "flash:w:"+filename
            pwd = subprocess.run(['pwd'],shell= True,stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,universal_newlines=True)
            data = str(pwd.stdout)
            print(data)
            self.label_6.setText(data)
        except Exception as e:
            print(e)

        try:
            result = subprocess.run(['avrdude', '-V', '-c', 'arduino', '-p','ATMEGA328P','-P',port_name,'-b','115200','-U',hex_file],shell= True,stdout=subprocess.PIPE, stderr=subprocess.PIPE,stdin=subprocess.PIPE, universal_newlines=True)
            print("returncode" + str(result.returncode))
            print("err"+ str(result.stderr))
            self.label_6.setText(data + "\n"+ str(result.stderr))
        except Exception as e:
            print(e)


if (__name__ == "__main__"):
    try:
        app = QApplication(sys.argv)
        mw = mainWindow()
        mw.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)


