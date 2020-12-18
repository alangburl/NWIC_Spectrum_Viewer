import numpy as np
import sys
from PyQt5.QtWidgets import (QApplication, QPushButton,QWidget,QGridLayout,
                             QSizePolicy,QLineEdit,
                             QMessageBox,QFileDialog,QLabel)
from PyQt5.QtGui import (QFont)

class Load_New(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Load New Probability')
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
        
        
        self.counts_loc=QLineEdit(self)
        self.counts_loc.setFont(self.font)
        self.counts_loc.setSizePolicy(self.size_policy,self.size_policy)
        
        self.counts_label=QLabel('Spectrum Count Location:',self)
        self.counts_label.setFont(self.font)
        self.counts_label.setSizePolicy(self.size_policy,self.size_policy)
        
        
        self.browse_counts=QPushButton('Browse',self)
        self.browse_counts.setFont(self.font)
        self.browse_counts.setSizePolicy(self.size_policy,self.size_policy)
        self.browse_counts.clicked.connect(self.count_browser)
        
        self.add=QPushButton('Add Spectrum',self)
        self.add.setFont(self.font)
        self.add.setSizePolicy(self.size_policy,self.size_policy)
#        self.add.clicked.connect(self.add_spectrum)
        self.add.setEnabled(False)
        
        layout=QGridLayout(self)
        layout.addWidget(self.legend_label,0,0)
        layout.addWidget(self.legend,0,1)
        layout.addWidget(self.counts_label,1,0)
        layout.addWidget(self.counts_loc,1,1)
        layout.addWidget(self.browse_counts,1,2)
        layout.addWidget(self.add,2,0)
        
        self.setLayout(layout)
        self.show()
        
    def count_browser(self):
        fileName,ok=QFileDialog.getOpenFileName(self,'Counts File Location',
                                             "",'Comma Seperated File (*.csv)')
        if fileName and ok:
            self.browse_counts.setStyleSheet("background-color: green")
            self.add.setEnabled(True)
            self.counts_loc.setText(fileName)
            self.fileName=fileName
    def process(self):
        self.name=self.legend.text()
        f=open(self.fileName,'r')
        data=f.readlines()
        f.close()
        self.time,self.probability=[],[]
        try:
            for i in range(len(data)):
                line=data[i].split(sep=',')
                self.time.append(float(line[2]))
                self.probability.append(float(line[3]))
        except:
            True
        self.close()
        
if __name__=="__main__":
    app=QApplication(sys.argv)
    ex=Load_New()
    sys.exit(app.exec_())