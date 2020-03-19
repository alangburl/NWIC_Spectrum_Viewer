import matplotlib.pyplot as plt
import sys,os
from PyQt5.QtWidgets import (QApplication, QPushButton,QWidget,QGridLayout,
                             QSizePolicy,QLineEdit,
                             QMainWindow,QAction,QVBoxLayout
                             ,QDockWidget,QListView,
                             QAbstractItemView,QLabel,QFileDialog,QTextEdit,
                             QInputDialog,QSlider,QMdiArea,QMdiSubWindow,QProgressBar)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
##import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
##import matplotlib.pyplot as plt
class Time_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.size_policy=QSizePolicy.Expanding
        self.font=QFont()
        self.font.setPointSize(12)
        self.showMaximized()
        self.setWindowTitle('Timing Processing')
        self.init()
        self.show()
        
    def init(self):
        self.process=QPushButton('Process',self)
        self.process.setFont(self.font)
#        self.process.setSizePolicy(self.size_policy,self.size_policy)
        self.process.clicked.connect(self.process_)
        self.process.setEnabled(False)
        self.progress=QProgressBar(self)
#        self.progress.setSizePolicy(self.size_policy,self.size_policy)
        self.save_image=QPushButton('Save Image',self)
        self.save_image.setFont(self.font)
#        self.save_image.setSizePolicy(self.size_policy,self.size_policy)
        self.save_image.clicked.connect(self.saver)
        
        self.total_plot=QWidget()
        self.total_figure=Figure()
        self.total_canvas=FigureCanvas(self.total_figure)
        self.total_toolbar=NavigationToolbar(self.total_canvas,self)
        layout=QVBoxLayout()
        layout.addWidget(self.total_toolbar)
        layout.addWidget(self.total_canvas)
        self.total_plot.setLayout(layout)
        self.total_ax=self.total_canvas.figure.subplots()
        self.total_ax.set_title('Total')
        
        items=[str(i) for i in range(1,11)]
        self.text,self.ok=QInputDialog.getItem(self,'View Timing',
                                               'Number of timing:',
                                               items,0,False)
        if self.text and self.ok:
            self.progress.setMaximum(int(self.text))
            self.proce()
        layout=QGridLayout(self)
        layout.addWidget(self.process,0,0)
#        layout.addWidget(self.progress,0,1)
        layout.addWidget(self.total_plot,1,0,1,2)
        layout.addWidget(self.save_image,0,1)
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
                        self.file_names.append(os.path.split(te)[1].split(sep='.')[0])
                    self.progress.setValue(i+1)
#            self.close()
            self.process.setEnabled(True)
#            print(self.)
        except:
            self.close()
    def process_(self):
        duty,ok=QInputDialog.getInt(self,'Enter Duty Cycle','Duty Cycle %:',5,0,100)
        frequency,ok2=QInputDialog.getInt(self,'Enter Frequency','Frequency[Hz]:',200,0,1000)
        markers=['c+','rx','k*','m1','y.','g8','b2','mh','c--','k+']
        self.total_ax.clear()
        maxr=0
        for i in range(len(self.file_names)):
            self.total_ax.plot(self.values[self.file_names[i]][0],
                               self.values[self.file_names[i]][1],markers[i],
                               label=self.file_names[i],markersize=12)
            if max(self.values[self.file_names[i]][1])> maxr:
                maxr=max(self.values[self.file_names[i]][1])
        if ok and ok2:
            on_time=(1/frequency)*(duty/100)*1e6
            xs=[0,0,on_time,on_time]
            ys=[0,maxr,maxr,0]
            self.total_ax.axvline(on_time,
          label='Region divider at {:.1f}us\nafter rising edge'.format(on_time))
        
            self.total_ax.plot(xs,ys,label='Duty cycle: {}%'.format(duty))
        self.total_ax.legend(prop={'size':18})
        self.total_ax.set_yscale('log')
        self.total_ax.set_ylabel('Counts',fontsize=18)
        self.total_ax.set_xlabel(r'Time [$\mu s$]',fontsize=18)
        self.total_ax.tick_params(labelsize=18)
        self.total_canvas.draw()
        
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

    def saver(self):
        options='Portable Network Graphics (*.png);;'
        options_='Joint Photographic Experts Group(*.jpg)'
        options=options+options_
        file_name=QFileDialog.getSaveFileName(self,'Spectrum Image Save',""
                                              ,options)
        
        if file_name:
            self.total_figure.savefig(file_name[0],dpi=600,figsize=(6,6))
            
if __name__ =="__main__":
    app=QApplication(sys.argv)
    ex=Time_Window()
    sys.exit(app.exec_())