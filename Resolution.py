from PyQt5.QtWidgets import (QApplication, QPushButton,QWidget,QGridLayout,
                             QSizePolicy,QLineEdit,
                             QMainWindow,QAction,QVBoxLayout
                             ,QDockWidget,QListView,
                             QAbstractItemView,QLabel,QFileDialog,QTextEdit,
                             QInputDialog)
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
import sys
import numpy as np
from scipy import signal
class Resolution(QMainWindow):
    def __init__(self,spectrum,width,distance,font):
        '''Expects the spectrum to be a 2d list having counts in the 
        first column and energy in the second, width of the peaks to detect
        in channels and distance from peak to peak in channels. Font is a
        QFont'''
        super().__init__()
        self.spectrum=spectrum
        # self.peaks,self.eres,self.l,self.r=self.find_peaks(spectrum[0],
                                                           # width,distance)
        self.menu()
        self.showMaximized()
        self.geometry()
        self.setWindowTitle('Peak Detection and Energy Resolution')
        self.font=font
        self.show()
        
    def geometry(self):
        self.calibrated_plot=QWidget()
        layout1=QVBoxLayout()
        self.figure1=Figure()
        self.canvas1=FigureCanvas(self.figure1)
        self.toolbar1=NavigationToolbar(self.canvas1,self)
        layout1.addWidget(self.toolbar1)
        layout1.addWidget(self.canvas1)
        self.calibrated_plot.setLayout(layout1)
        self.ax1=self.canvas1.figure.subplots()
        self.ax1.set_yscale('log')
        self.ax1.set_xlabel('Energy (MeV)')
        self.ax1.set_ylabel('Counts')
        self.ax1.set_title('Peak Finder')
        self.figure1.tight_layout()
        
        main=QWidget()
        main_lay=QVBoxLayout()
        main_lay.addWidget(self.calibrated_plot)
        main.setLayout(main_lay)
        self.setCentralWidget(main)
    
    def menu(self):
        self.menuFile=self.menuBar().addMenu('&File')
        self.save_image=QAction('&Save Image',self)
        self.save_image.triggered.connect(self.saver)
        self.menuFile.addAction(self.save_image)
        
    def saver(self):
        options='Portable Network Graphics (*.png);;'
        options_='Joint Photographic Experts Group(*.jpg)'
        options=options+options_
        file_name,ok=QFileDialog.getSaveFileName(self,'Spectrum Image Save',""
                                              ,options)
        
        if file_name and ok:
            self.figure1.savefig(file_name[0],dpi=600,figsize=(10,10))


    def find_peaks(self,x,width,distance):
        peaks, properties = signal.find_peaks(x,width=width,distance=distance)
        e_res=[]
        widths=properties['widths'] #the fwhm of the peak
        left=properties['left_ips'] #left point of the fwhm
        right=properties['right_ips'] #right point of the fwhm
        sigma=[i/(2*np.sqrt(2*np.log(2))) for i in widths] #standard deviation
        left_sig=[]
        right_sig=[]
        #recalculate the peak location based on the average fo the left and right fwhm
        for i in range(len(peaks)):
            avg=(left[i]+right[i])/2
            peaks[i]=avg
            left_sig.append(avg-4*sigma[i])
            right_sig.append(avg+4*sigma[i])
            e_res.append(widths[i]/avg*100)
            
        return peaks,e_res,left_sig,right_sig
    
if __name__=="__main__":
    app=QApplication(sys.argv)
    ex=Resolution(10,1,1,1)
    sys.exit(app.exec_())
        