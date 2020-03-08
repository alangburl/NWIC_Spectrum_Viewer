#write the spe files
from PyQt5.QtWidgets import (QApplication, QPushButton,QWidget,QGridLayout,
                             QSizePolicy,QLineEdit,
                             QMessageBox,QFileDialog,QLabel,QInputDialog)
import datetime
from Calibration import Detector_Calibration as Calib
class Save_Spe(QWidget):
    def __init__(self,loaded_data,legend,name):
        super().__init__()
        self.data=loaded_data
        self.legend=legend
        self.name=name
        self.save()
        
    def save(self):
        name=self.name
        #get a linear fit so the file generally works
        counts=[i*self.data[2] for i in self.data[1]]
        channels=[i for i in range(len(counts))]
        m,b=Calib(channels).linear_least_squares_fit(
                channels,self.data[0],True)
        now=datetime.datetime.now()
        #rescale the counts 
        
        if int(now.hour)>12:
            hr=int(now.hour-12)
            ma='PM'
        elif int(now.hour==12):
            hr=12
            ma='PM'
        else:
            hr=now.hour
            ma='AM'
        f=open(name[0],'w')
        f.write('$SPEC_ID:\n{}\n$MEAS_TIM:\n{:.6f} {:.6f}\n'.format(
                self.legend,self.data[2],self.data[2]))
        f.write('$DATE_MEA:\n')
        f.write('{}/{}/{} {}:{}:{} {}\n'.format(now.month,now.day,
                now.year,hr,now.minute,now.second,ma))
        f.write('$DATA:\n0 {}\n'.format(len(self.data[0])))
        for i in range(len(counts)):
            f.write('{}\n'.format(int(counts[i])))
        f.write('$ENER_FIT:\n')
        f.write('{:.6f} {:.6f} {:.6f}\n'.format(0,m*1000,0))
        f.write('MCA_CAL:\n3\n{:.6f} {:.6f} {:.6f}\n'.format(0,m*1000,0))
        f.write('$END_RECORD:')