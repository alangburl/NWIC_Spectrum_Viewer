import matplotlib.pyplot as plt
import sys,time,os
from PyQt5.QtWidgets import (QApplication, QPushButton,QWidget,QGridLayout,
                             QSizePolicy,QLineEdit,
                             QMainWindow,QAction,QVBoxLayout
                             ,QDockWidget,QListView,
                             QAbstractItemView,QLabel,QFileDialog,QTextEdit,
                             QInputDialog,QSlider,QMdiArea,QMdiSubWindow,QProgressBar)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
##import numpy as np
#from matplotlib.figure import Figure
#from matplotlib.backends.backend_qt5agg import (
#        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
##import matplotlib.pyplot as plt
class Time_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.size_policy=QSizePolicy.Expanding
        self.font=QFont()
        self.font.setPointSize(12)
        self.setGeometry(600,600,300,300)
        self.setWindowTitle('Timing Processing')
        self.init()
        self.show()
    def init(self):
        self.process=QPushButton('Process',self)
        self.process.setSizePolicy(self.size_policy,self.size_policy)
        self.process.clicked.connect(self.proce)
        
        self.progress=QProgressBar(self)
        self.progress.setSizePolicy(self.size_policy,self.size_policy)
        
        items=[str(i) for i in range(11)]
        self.text,self.ok=QInputDialog.getItem(self,'View Timing',
                                               'Number of timing:',
                                               items,0,False)
        if self.text and self.ok:
            self.progress.setMaximum(int(self.text))
        layout=QVBoxLayout(self)
        layout.addWidget(self.process)
        layout.addWidget(self.progress)
        self.setLayout(layout)

    def proce(self):
        self.file_names=[]
        self.values={}
        try:
            if self.ok and self.text:
                for i in range(int(self.text)):
                    te,ko=QFileDialog.getOpenFileName(self,'File Name','',
                                 'Text File (*.txt);;Comma Seperated File (*.csv)')
                    if te!='' and ko:
                        self.values[os.path.split(te)[1].split(sep='.')[0]]=self.get_data(te)
                        self.file_names.append(te)
                    self.progress.setValue(i)
            self.close()
            plt.plot(self.values[self.file_names[0]][0],self.values[self.file_names[0]][1])
            plt.show()
        except:
            self.close()
    def get_data(self,file_name):
        try:
            f=open(file_name)
            data=f.readlines()
            f.close()
            counts=[]
            times=[]
            for i in range(1,len(data)):
                line=data[i].split(sep=',')
                times.append(float(line[0]))
                counts.append(float(line[1]))
            return times,counts
        except:
            pass

if __name__ =="__main__":
    app=QApplication(sys.argv)
    ex=Time_Window()
    sys.exit(app.exec_())