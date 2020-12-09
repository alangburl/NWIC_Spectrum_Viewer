'''Interface for loading a new spectrum name
'''
import numpy as np
import sys
from PyQt5.QtWidgets import (QApplication, QPushButton,QWidget,QGridLayout,
                             QSizePolicy,QLineEdit,
                             QMessageBox,QFileDialog,QLabel)
from PyQt5.QtGui import (QFont)

class Load_New(QWidget):
    counts_=False
    calibrate_=False
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Load New Spectrum')
        self.font=QFont()
        self.font.setPointSize(12)
        self.size_policy=QSizePolicy.Expanding
        
        self.legend=QLineEdit(self)
        self.legend.setFont(self.font)
        self.legend.setSizePolicy(self.size_policy,self.size_policy)
        self.legend.setToolTip('Name that will be shown\non plot legend')
        
        self.legend_label=QLabel('Legend:',self)
        self.legend_label.setFont(self.font)
        self.legend_label.setSizePolicy(self.size_policy,self.size_policy)
        
        self.run_time=QLineEdit(self)
        self.run_time.setFont(self.font)
        self.run_time.setSizePolicy(self.size_policy,self.size_policy)
        
        self.run_label=QLabel('Run Time: (s)',self)
        self.run_label.setFont(self.font)
        self.run_label.setSizePolicy(self.size_policy,self.size_policy)
        
        self.counts_loc=QLineEdit(self)
        self.counts_loc.setFont(self.font)
        self.counts_loc.setSizePolicy(self.size_policy,self.size_policy)
        
        self.counts_label=QLabel('Spectrum Count Location:',self)
        self.counts_label.setFont(self.font)
        self.counts_label.setSizePolicy(self.size_policy,self.size_policy)
        
        self.calibration_loc=QLineEdit(self)
        self.calibration_loc.setFont(self.font)
        self.calibration_loc.setSizePolicy(self.size_policy,self.size_policy)
        
        self.calibration_label=QLabel('Calibration Location:',self)
        self.calibration_label.setFont(self.font)
        self.calibration_label.setSizePolicy(self.size_policy,self.size_policy)
        
        self.browse_counts=QPushButton('Browse',self)
        self.browse_counts.setFont(self.font)
        self.browse_counts.setSizePolicy(self.size_policy,self.size_policy)
        self.browse_counts.clicked.connect(self.count_browser)
        
        self.browse_calibration=QPushButton('Browse',self)
        self.browse_calibration.setFont(self.font)
        self.browse_calibration.setSizePolicy(self.size_policy,self.size_policy)
        self.browse_calibration.clicked.connect(self.calibration_browse)
        
        self.add=QPushButton('Add Spectrum',self)
        self.add.setFont(self.font)
        self.add.setSizePolicy(self.size_policy,self.size_policy)
#        self.add.clicked.connect(self.add_spectrum)
        self.add.setEnabled(False)
        
        layout=QGridLayout(self)
        layout.addWidget(self.legend_label,0,0)
        layout.addWidget(self.legend,0,1)
        layout.addWidget(self.run_label,1,0)
        layout.addWidget(self.run_time,1,1)
        layout.addWidget(self.counts_label,2,0)
        layout.addWidget(self.counts_loc,2,1,1,4)
        layout.addWidget(self.browse_counts,2,5)
        layout.addWidget(self.calibration_label,3,0)
        layout.addWidget(self.calibration_loc,3,1,1,4)
        layout.addWidget(self.browse_calibration,3,5)
        layout.addWidget(self.add,4,0)
        
        self.setLayout(layout)
        self.show()
    def count_browser(self):
        fileName=QFileDialog.getOpenFileName(self,'Counts File Location',
                                             "",
                         'Text File (*.txt);;Comma Seperated File (*.csv);;IAEA (*.spe)')
        if fileName:
            self.counts_=True
            if self.calibrate_:
                self.add.setEnabled(True)
            self.counts_loc.setText(fileName[0])

    def calibration_browse(self):
        
        fileName=QFileDialog.getOpenFileName(self,'Calibration File Location',
                                             "",
                         'Text File (*.txt);;Comma Seperated File (*.csv)')
        
        if fileName:
            self.calibrate_=True
            if self.counts_:
                self.add.setEnabled(True)
            self.calibration_loc.setText(fileName[0])
            
    def add_spectrum(self):
        '''Open and load the information into memory, 
        also check to make sure the arrays are the same length for plotting
        '''
        counts=self.counts_loc.text()
        calibration=self.calibration_loc.text()
        
        if '.spe' in counts.lower():
            self.counts,scale=self.load_spe(counts)
        else:
            f=open(counts,'r')
            c_data=f.readlines()
            f.close()
            self.counts=[float(i.split(sep=',')[0].split(sep='\n')[0]) \
                         for i in c_data]
            try:
                scale=float(self.run_time.text())
            except:
                scale=1.0
                
        self.accum_time=scale
        self.count_rate=np.sum(self.counts)/scale
        self.counts=[self.counts[i]/scale for i in range(len(self.counts))]
    
        g=open(calibration,'r')
        g_data=g.readlines()
        g.close()
        self.calibration=[float(i.split(sep=',')[0].split(sep='\n')[0]) \
                          for i in g_data]
        if len(self.calibration)!=len(self.counts):
            print(len(self.calibration))
            print(len(self.counts))
            reply=QMessageBox.information(self,'Length Error',
                          'Calibration and Count\nfile have different lengths',
                          QMessageBox.Ok)
            pass
        self.close()
        
    
    def load_spe(self,file_path):
        '''Load a spectrum file type using the SPE file format'''
        f=open(file_path,'r')
        data=f.readlines()
        f.close()
        
        counts=[]
        channels=[]
        # num_counts=int(data[7].split()[1])
        #first find the index for $DATA so
        s_index=0
        e_index=0
        timer=0
        for i in range(len(data)):
            if '$MEAS_TIM:' in data[i]:
                timer=float(data[i+1].split(sep=' ')[0])
            if '$DATA:' in data[i]:
                s_index=i+2
                
        for i in range(s_index,len(data)):
            if '$' in data[i]:
                e_index=i-1
                break
        print(s_index,e_index)
        for i in range(s_index,e_index):
            counts.append(float(data[i]))
            channels.append(i-s_index)
        return counts,timer
        
    
if __name__=="__main__":
    app=QApplication(sys.argv)
    ex=Load_New()
    sys.exit(app.exec_())