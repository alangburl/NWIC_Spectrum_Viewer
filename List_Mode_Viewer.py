from List_Mode_Reader import List_Mode 
#prefined imports
import sys
from PyQt5.QtWidgets import (QApplication, QPushButton,QWidget,QGridLayout,
                             QSizePolicy,QLineEdit,
                             QMainWindow,QAction,QVBoxLayout
                             ,QDockWidget,QListView,
                             QAbstractItemView,QLabel,QFileDialog,QTextEdit,
                             QInputDialog,QSlider)
from PyQt5.QtGui import (QFont,QStandardItemModel,QStandardItem)
from PyQt5.QtCore import Qt,QModelIndex
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)


class List_Mode_Viewer(QMainWindow):
    sync=False
    lis=False
    calibration=False
    def __init__(self):
        super().__init__()
        self.setWindowTitle('List Mode Viewer')
        self.font=QFont()
        self.font.setPointSize(12)
        self.size_policy=QSizePolicy.Expanding
        self.menu()
        self.geometry()
        self.showMaximized()
        self.popup()
        self.show()
        
    def menu(self):
        self.menuFile=self.menuBar().addMenu('&File')
        self.load_new=QAction('&Load New Data')
        self.load_new.triggered.connect(self.loading)
        self.load_new.setShortcut('CTRL+N')
        self.save_file=QAction('&Save Spectrum')
        self.save_file.triggered.connect(self.save_spectrum)
        self.save_file.setEnabled(False)
        
        self.menuView=self.menuBar().addMenu('&View')
        self.view_pop=QAction('&Show Tools')
        self.view_pop.triggered.connect(self.popup)
        self.view_pop.setShortcut('CTRL+U')
        self.menuView.addActions([self.view_pop])
        self.menuFile.addActions([self.load_new,self.save_file])
    def geometry(self):
        self.central_widget=QWidget()
        self.region1_plot=QWidget()
        self.region1_figure=Figure()
        self.region1_canvas=FigureCanvas(self.region1_figure)
        self.region1_toolbar=NavigationToolbar(self.region1_canvas,self)
        layout=QVBoxLayout()
        layout.addWidget(self.region1_toolbar)
        layout.addWidget(self.region1_canvas)
        self.region1_plot.setLayout(layout)
        self.region1_ax=self.region1_canvas.figure.subplots()
        
        self.region2_plot=QWidget()
        self.region2_figure=Figure()
        self.region2_canvas=FigureCanvas(self.region2_figure)
        self.region2_toolbar=NavigationToolbar(self.region2_canvas,self)
        layout=QVBoxLayout()
        layout.addWidget(self.region2_toolbar)
        layout.addWidget(self.region2_canvas)
        self.region2_plot.setLayout(layout)
        self.region2_ax=self.region2_canvas.figure.subplots()
        self.region2_ax.set_title('Region 2')
        
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
        
        layout=QGridLayout()
        layout.addWidget(self.region1_plot,0,0)
        layout.addWidget(self.region2_plot,0,1)
        layout.addWidget(self.total_plot,1,0,1,2)
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)
        
    def loading(self):
        self.loader=QWidget()
        self.loader.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.sync_label=QLabel('Sync Pulse Location: ')
        self.sync_label.setSizePolicy(self.size_policy,self.size_policy)
        self.sync_label.setFont(self.font)
        
        self.sync_location=QPushButton('Browse')
        self.sync_location.setSizePolicy(self.size_policy,self.size_policy)
        self.sync_location.setFont(self.font)
        self.sync_location.clicked.connect(self.sync_browse)
        
        self.detector_label=QLabel('Detector List Mode Data: ')
        self.detector_label.setSizePolicy(self.size_policy,self.size_policy)
        self.detector_label.setFont(self.font)
        
        self.detector_location=QPushButton('Browse')
        self.detector_location.setSizePolicy(self.size_policy,self.size_policy)
        self.detector_location.setFont(self.font)
        self.detector_location.clicked.connect(self.detector_browse)
        
        self.calibration_label=QLabel('Calibration:(Optional)')
        self.calibration_label.setSizePolicy(self.size_policy,self.size_policy)
        self.calibration_label.setFont(self.font)
        
        self.calibration_location=QPushButton('Browse')
        self.calibration_location.setSizePolicy(self.size_policy,self.size_policy)
        self.calibration_location.setFont(self.font)
        self.calibration_location.clicked.connect(self.calibration_browse)
        
        self.process_new=QPushButton('Process')
        self.process_new.setSizePolicy(self.size_policy,self.size_policy)
        self.process_new.setFont(self.font)
        self.process_new.clicked.connect(self.processing_new)
        self.process_new.setEnabled(False)
        
        layout=QGridLayout()
        layout.addWidget(self.sync_label,0,0)
        layout.addWidget(self.sync_location,0,1)
        layout.addWidget(self.detector_label,1,0)
        layout.addWidget(self.detector_location,1,1)
        layout.addWidget(self.calibration_label,2,0)
        layout.addWidget(self.calibration_location,2,1)
        layout.addWidget(self.process_new,3,0,1,2)
        self.loader.setLayout(layout)
        self.loader.setWindowTitle('Load New List Mode')
        self.loader.show()
        
    def sync_browse(self):
        self.sync_filename=QFileDialog.getOpenFileName(self,
                           'Sync File Location',"",
                           'Text File (*.txt);;Comma Seperated File (*.csv)')
        if self.sync_filename[0]!="":
            self.sync=True
            self.sync_location.setStyleSheet("background-color: green")
            if self.lis==True:
                self.process_new.setEnabled(True)
    def detector_browse(self):
        self.list_filename=QFileDialog.getOpenFileName(self,
                           'Listmode File Location',"",
                           'Text File (*.txt);;Comma Seperated File (*.csv)')
        if self.list_filename[0]!="":
            self.lis=True
            self.detector_location.setStyleSheet("background-color: green")
            if self.sync==True:
                self.process_new.setEnabled(True)
    def calibration_browse(self):
        self.calib_filename=QFileDialog.getOpenFileName(self,
                           'calibration File Location',"",
                           'Text File (*.txt);;Comma Seperated File (*.csv)')
        if self.calib_filename[0]!='':
            self.calibration=True
            f=open(self.calib_filename[0],'r')
            data=f.readlines()
            f.close()
            self.calibration_data=[]
            for i in range(len(data)):
                self.calibration_data.append(float(data[i]))
            del data
            del f
    def processing_new(self):
        try:
            self.loader.close()
        except:
            True
        self.save_file.setEnabled(True)
        self.list_mode_processor=List_Mode()
        self.sync_time,sync_channel=self.list_mode_processor.read_file(
                self.sync_filename[0])
        del sync_channel
        self.list_time,self.list_channel=self.list_mode_processor.read_file(
                self.list_filename[0])
        delt=(self.sync_time[2]-self.sync_time[1])
        self.offset.setMaximum(delt-self.duty_cycle.value()/100*delt)
        self.updater()
        
    def popup(self):
        self.popup=QWidget()
        self.popup.setWindowTitle('View Controls')
        self.popup.setSizePolicy(self.size_policy,self.size_policy)
        self.popup.setFont(self.font)
        
        self.duty_label=QLabel('Duty Cycle [%]: ')
        self.duty_label.setSizePolicy(self.size_policy,self.size_policy)
        self.duty_label.setFont(self.font)
        
        self.duty_cycle=QSlider(Qt.Horizontal)
        self.duty_cycle.setSizePolicy(self.size_policy,self.size_policy)
        self.duty_cycle.setFont(self.font)
        self.duty_cycle.setMinimum(0)
        self.duty_cycle.setMaximum(100)
        self.duty_cycle.setSingleStep(1)
        self.duty_cycle.setValue(10)
        self.duty_cycle.setTickPosition(QSlider.TicksBelow)
        self.duty_cycle.valueChanged.connect(self.duty_changed)
        
        self.duty_indicator=QLineEdit()
        self.duty_indicator.setSizePolicy(self.size_policy,self.size_policy)
        self.duty_indicator.setFont(self.font)
        self.duty_indicator.setToolTip(
                'Duty cycle of the sync pulse from\neutron generator')
        
        self.offset_label=QLabel('Offset from sync [us]: ')
        self.offset_label.setSizePolicy(self.size_policy,self.size_policy)
        self.offset_label.setFont(self.font)
        
        self.offset=QSlider(Qt.Horizontal)
        self.offset.setSizePolicy(self.size_policy,self.size_policy)
        self.offset.setFont(self.font)
        self.offset.setMinimum(0)
        self.offset.setMaximum(1000)
        self.offset.setSingleStep(1)
        self.offset.setValue(10)
        self.offset.setTickPosition(QSlider.TicksBelow)
        self.offset.setTickInterval(100)
        self.offset.setToolTip(
            'After end of pulse to divide into Region 1 and 2 in micro seconds')
#        self.offset.valueChanged.connect(self.offset_changed)
        self.offset.valueChanged.connect(self.offset_changed)
        self.offset_indicator=QLineEdit()
        self.offset_indicator.setSizePolicy(self.size_policy,self.size_policy)
        self.offset_indicator.setFont(self.font)
        self.offset_indicator.setToolTip(
            'After end of pulse to divide into Region 1 and 2 in micro seconds')
        
        self.update=QPushButton('Update')
        self.update.setSizePolicy(self.size_policy,self.size_policy)
        self.update.setFont(self.font)
        self.update.clicked.connect(self.updater)
        
        layout=QGridLayout()
        layout.addWidget(self.duty_label,0,0)
        layout.addWidget(self.duty_cycle,0,1)
        layout.addWidget(self.duty_indicator,0,2)
        layout.addWidget(self.offset_label,1,0)
        layout.addWidget(self.offset,1,1)
        layout.addWidget(self.offset_indicator,1,2)
        layout.addWidget(self.update,2,0)
        
        self.popup.setLayout(layout)
        self.duty_changed()
        self.offset_changed()
        self.popup.show()
        
    def duty_changed(self):
        self.duty_indicator.setText(str(self.duty_cycle.value()))
        
    def offset_changed(self):
        self.offset_indicator.setText(str((self.offset.value())))
        
    def updater(self):
        delta_time=self.duty_cycle.value()/100*(
                self.sync_time[2]-self.sync_time[1])
        delta_time+=self.offset.value()
        self.region1_spec,self.region2_spec=self.list_mode_processor.timing(
                                        delta_time,self.sync_time,
                                        self.list_time,self.list_channel)
        total=[]
        for i in range(len(list(self.region2_spec.values()))):
            total.append(list(self.region2_spec.values())[i]+list(self.region1_spec.values())[i])
        self.region1_ax.clear()
        self.region2_ax.clear()
        self.total_ax.clear()
        self.region1_ax.set_title('Region 1')
        self.region2_ax.set_title('Region 2')
        self.total_ax.set_title('Total')
        r1_values=list(self.region1_spec.values())[:-1]
        r2_values=list(self.region2_spec.values())[:-1]
        uncal_keys=list(self.region1_spec.keys())
        if self.calibration:
            self.region1_ax.set_xlim(self.calibration_data[0],
                                     14)
            self.region2_ax.set_xlim(self.calibration_data[0],
                                     14)
            self.total_ax.set_xlim(self.calibration_data[0],14)
            self.region1_ax.set_xlabel('Energy [MeV]')
            self.region2_ax.set_xlabel('Energy [MeV]')
            self.total_ax.set_xlabel('Energy [MeV]')
            self.region1_ax.plot(self.calibration_data,r1_values)
            self.region2_ax.plot(self.calibration_data,r2_values)
            self.total_ax.plot(self.calibration_data,total[:-1],label='Total')
            self.total_ax.plot(self.calibration_data,r1_values,label='Region 1')
            self.total_ax.plot(self.calibration_data,r2_values,label='Region 2')
        else:
            self.region1_ax.set_xlabel('Channel')
            self.region2_ax.set_xlabel('Channel')
            self.total_ax.set_xlabel('Channel')
            self.region1_ax.set_xlim(0,len(list(self.region1_spec.keys())))
            self.region2_ax.set_xlim(0,len(list(self.region2_spec.keys())))
            self.total_ax.set_xlim(0,len(list(self.region2_spec.keys())))
            self.region1_ax.plot(uncal_keys[:-1],r1_values)
            self.region2_ax.plot(uncal_keys[:-1],r2_values)
            self.total_ax.plot(uncal_keys[:-1],total[:-1],label='Total')
            self.total_ax.plot(uncal_keys[:-1],r1_values,label='Region 1')
            self.total_ax.plot(uncal_keys[:-1],r2_values,label='Region 2')
        self.region1_ax.set_yscale('log')
        self.region2_ax.set_yscale('log')
        self.total_ax.set_yscale('log')
        self.total_ax.legend()
        self.region1_canvas.draw()
        self.region2_canvas.draw()
        self.total_canvas.draw()
        
    def save_spectrum(self):
        items=['Region 1','Region 2']
        self.updater()
        text,ok=QInputDialog.getItem(self,'Save Spectrum','Saving:',items,0,False)
        if ok and text:
            name=QFileDialog.getSaveFileName(self,'File Name','','Text File (*.txt)')
            f=open(name[0],'w')
            if text=='Region 1' and name[0]!="":
                counts=list(self.region1_spec.values())
                bins=list(self.region1_spec.keys())
                for i in range(len(bins)-1):
                    f.write('{}\n'.format(counts[i]))
            if text=='Region 2' and name[0]!='':
                counts=list(self.region2_spec.values())
                bins=list(self.region2_spec.keys())
                for i in range(len(bins)-1):
                    f.write('{}\n'.format(counts[i]))
            f.close()
        
if __name__ =="__main__":
    app=QApplication(sys.argv)
    ex=List_Mode_Viewer()
    sys.exit(app.exec_())