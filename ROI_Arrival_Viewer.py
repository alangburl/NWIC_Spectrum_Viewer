import numpy as np
from ROI_Arrival import ROI_Arrival,ROI_Location
#prefined imports
import sys,time,winsound
import numpy as np
from PyQt5.QtWidgets import (QApplication, QPushButton,QWidget,QGridLayout,
                             QSizePolicy,QLineEdit,
                             QMainWindow,QAction,QVBoxLayout
                             ,QDockWidget,QListView,
                             QAbstractItemView,QLabel,QFileDialog,QTextEdit,
                             QInputDialog,QSlider,QMdiArea,QMdiSubWindow,
                             QMessageBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
#import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)

class ROI_Viewer(QMainWindow):
    done=False
    def __init__(self,list_time,list_channel,sync_time,calibration):
        super().__init__()
        self.num_sync=sync_time.size
        self.num_pulses=list_time.size
        self.list_time,self.list_channel=list_time,list_channel
        self.sync_time,self.calibration=sync_time,calibration
        self.sync_delta=sync_time[2]-sync_time[1]
        self.lower,self.upper=9.5,10.9
        self.font1=QFont()
        self.font1.setPointSize(12)
        self.size_policy=QSizePolicy.Expanding
        self.menu()
        self.showMaximized()
        self.setWindowTitle('ROI Timing Arrival')
        self.geometry()
#        self.process()
        self.show()
        
    def menu(self):
        self.menuFile=self.menuBar().addMenu('&File')
        self.save_file=QAction('&Save Spectrum')
        self.save_file.triggered.connect(self.save_spectrum)
        self.save_file.setShortcut('CTRL+S')
        self.save_file.setEnabled(False)
        self.menuFile.addActions([self.save_file])
        
    def geometry(self):
        r1_label=QLabel(r'Region 1-2 divider: [us]')
        r1_label.setFont(self.font1)
        r2_label=QLabel(r'Region 2-3 divider: [us]')
        r2_label.setFont(self.font1)
        
        self.r_1_slider=QSlider(Qt.Horizontal)
        self.r_1_slider.setSizePolicy(self.size_policy,self.size_policy)
        self.r_1_slider.setMinimum(0)
        self.r_1_slider.setMaximum(self.sync_delta-1)
        self.r_1_slider.setSingleStep(1)
        self.r_1_slider.setTickInterval(50)
        self.r_1_slider.setValue(100)
        self.r_1_slider.setTickPosition(QSlider.TicksBelow)
        self.r_1_slider.valueChanged.connect(self.update_r_1)
        self.r_1_slider.setFont(self.font1)
        
        self.r_2_slider=QSlider(Qt.Horizontal)
        self.r_2_slider.setSizePolicy(self.size_policy,self.size_policy)
        self.r_2_slider.setMinimum(101)
        self.r_2_slider.setMaximum(self.sync_delta)
        self.r_2_slider.setSingleStep(1)
        self.r_2_slider.setTickInterval(50)
        self.r_2_slider.setValue(101)
        self.r_2_slider.setTickPosition(QSlider.TicksBelow)
        self.r_2_slider.valueChanged.connect(self.update_r_2)
        self.r_2_slider.setFont(self.font1)
        
        self.r_1_label=QLabel(self)
        self.r_1_label.setSizePolicy(self.size_policy,self.size_policy)
        self.r_1_label.setText(str(self.r_1_slider.value()))
        self.r_1_label.setFont(self.font1)
        self.r_2_label=QLabel(self)
        self.r_2_label.setSizePolicy(self.size_policy,self.size_policy)
        self.r_2_label.setText(str(self.r_2_slider.value()))        
        self.r_2_label.setFont(self.font1)
        
        self.processer=QPushButton('Process',self)
        self.processer.clicked.connect(self.process)
        self.processer.setFont(self.font1)
        
        lower_label=QLabel('Lower ROI: [MeV]',self)
        lower_label.setFont(self.font1)
        upper_label=QLabel('Upper ROI: [MeV]',self)
        upper_label.setFont(self.font1)
        
        self.lower_text=QLineEdit(self)
        self.lower_text.setFont(self.font1)
        self.lower_text.setText(str(self.lower))
        self.upper_text=QLineEdit(self)
        self.upper_text.setFont(self.font1)
        self.upper_text.setText(str(self.upper))
        
        self.time_plot=QWidget()
        self.time_figure=Figure()
        self.time_canvas=FigureCanvas(self.time_figure)
        self.time_toolbar=NavigationToolbar(self.time_canvas,self)
        layout=QVBoxLayout()
        layout.addWidget(self.time_toolbar)
        layout.addWidget(self.time_canvas)
        self.time_plot.setLayout(layout)
        self.time_ax=self.time_canvas.figure.subplots()
        self.time_ax.set_title('Time')
        
        main_=QWidget()
        layout=QGridLayout(self)
        layout.addWidget(r1_label,0,0)
        layout.addWidget(self.r_1_slider,0,1)
        layout.addWidget(self.r_1_label,0,2)
        layout.addWidget(lower_label,0,3)
        layout.addWidget(self.lower_text,0,4)
        layout.addWidget(upper_label,1,3)
        layout.addWidget(self.upper_text,1,4)
        layout.addWidget(r2_label,1,0)
        layout.addWidget(self.r_2_slider,1,1)
        layout.addWidget(self.r_2_label,1,2)
        layout.addWidget(self.processer,2,0)
        layout.addWidget(self.time_plot,3,0,1,5)
        main_.setLayout(layout)
        self.setCentralWidget(main_)
        
    def update_r_1(self):
        self.r_2_slider.setMinimum(self.r_1_slider.value()+1)
        self.r_1_label.setText(str(self.r_1_slider.value()))
                
    def update_r_2(self):
        self.r_2_label.setText(str(self.r_2_slider.value()))

    def process(self):
        self.save_file.setEnabled(True)
        s1=time.time()
        delt=(self.sync_time[2]-self.sync_time[1])
        self.lower=float(self.lower_text.text())
        self.upper=float(self.upper_text.text())
        self.arrival,self.height=ROI_Arrival(self.sync_time,self.list_time,
                                             self.num_sync,self.list_channel,
                                             self.num_pulses,self.lower,
                                             self.upper,self.calibration)
        num_bins=int(delt/4)
        bins=np.linspace(0,delt,num_bins)
        self.bins=bins
        s=len(self.arrival)
        self.output=ROI_Location(self.arrival,bins,num_bins,s)
        r1,r2,r3=0,0,0
        print('Process ROI Arrivals in {:.3f}s'.format(time.time()-s1))
        for i in range(num_bins):
            if bins[i]<=self.r_1_slider.value():
                r1+=self.output[i]
            elif bins[i]>self.r_1_slider.value() and bins[i]<=self.r_2_slider.value():
                r2+=self.output[i]
            else:
                r3+=self.output[i]
                
        self.time_ax.clear()
        self.time_ax.plot(bins,self.output,'r*')
        self.time_ax.axvline(self.r_1_slider.value(),label='Region 1-2 divider at {:.2f}'.format(self.r_1_slider.value()))
        self.time_ax.axvline(self.r_2_slider.value(),label='Region 2-3 divider at {:.2f}'.format(self.r_2_slider.value()))
#        self.time_ax.set_yscale('log')
        self.time_ax.set_ylabel('Counts',fontsize=18)
        self.time_ax.set_xlabel(r'Arrival Time [$\mu s$]',fontsize=18)
        self.time_canvas.draw()
        self.done=True
        self.percentages=[r1/(r1+r2+r3)*100,
                          r2/(r1+r2+r3)*100,
                          r3/(r1+r2+r3)*100]
        QMessageBox.information(self,
                        'ROI Perecentages','''Region 1:{:.2f}%\nRegion 2:{:.2f}%\nRegion 3:{:.2f}%'''.format(
                                r1/(r1+r2+r3)*100,
                                r2/(r1+r2+r3)*100,r3/(r1+r2+r3)*100),
                                QMessageBox.Ok)
#        print('Region 1 total ROI percentage: {:.2f}%'.format(r1/(r1+r2+r3)*100))
#        print('Region 2 total ROI percentage: {:.2f}%'.format(r2/(r1+r2+r3)*100))
#        print('Region 3 total ROI percentage: {:.2f}%'.format(r3/(r1+r2+r3)*100))
        
    def save_spectrum(self):
        name=QFileDialog.getSaveFileName(self,'File Name','',
                             'Text File (*.txt);;Comma Seperated File (*.csv)')
        if name[0]!=' ':
            f=open(name[0],'w')
            f.write('%{:.2f},{:.2f},{:.2f}\n'.format(*self.percentages))
            for i in range(len(self.bins)):
                f.write('{:.6f},{}\n'.format(self.bins[i],self.output[i]))
            f.close()