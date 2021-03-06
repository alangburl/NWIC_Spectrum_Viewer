from List_Mode_Reader import List_Mode 
import Conversion
from Arrival_Timing import Arrival_Spread
from ROI_Arrival import ROI_Arrival,ROI_Location
from ROI_Arrival_Viewer import ROI_Viewer
import Timing
#prefined imports
import sys,time,winsound
import numpy as np
from PyQt5.QtWidgets import (QApplication, QPushButton,QWidget,QGridLayout,
                             QSizePolicy,QLineEdit,
                             QMainWindow,QAction,QVBoxLayout
                             ,QDockWidget,QListView,
                             QAbstractItemView,QLabel,QFileDialog,QTextEdit,
                             QInputDialog,QSlider,QMdiArea,QMdiSubWindow)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
#import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
import matplotlib.pyplot as plt

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
#        self.popup()
        self.show()
        
    def menu(self):
        self.menuFile=self.menuBar().addMenu('&File')
        self.load_new=QAction('&Load New Data')
        self.load_new.triggered.connect(self.loading)
        self.load_new.setShortcut('CTRL+N')
        self.save_file=QAction('&Save Spectrum')
        self.save_file.triggered.connect(self.save_spectrum)
        self.save_file.setShortcut('CTRL+S')
        self.save_file.setEnabled(False)
        self.save_roi=QAction('&Save ROI')
        self.save_roi.triggered.connect(self.save_roi_csv)
        self.save_roi.setEnabled(False)
        
        self.menuView=self.menuBar().addMenu('&View')
        self.view_pop=QAction('&Show Tools')
        self.view_pop.triggered.connect(self.popup_)
        self.view_pop.setShortcut('CTRL+U')
        self.view_pop.setEnabled(False)
        
        self.view_all=QAction('&Show Plots')
        self.view_all.triggered.connect(self.initiate)
        self.view_all.setShortcut('CTRL+V')
        
        self.view_variation=QAction('&Pulse Deviation')
        self.view_variation.triggered.connect(self.deviation)
        
        self.view_roi_arrive=QAction('&ROI Arrival Times')
        self.view_roi_arrive.triggered.connect(self.ROI_Arrivals)
        
        self.menuView.addActions([self.view_pop,self.view_all,self.view_variation,
                                  self.view_roi_arrive])
        self.menuFile.addActions([self.load_new,self.save_file,self.save_roi])
        
    def geometry(self):        
#        self.central_widget=QWidget()
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
        self.setup()
        
    def setup(self):
        sub1=QMdiSubWindow()
        sub1.setWidget(self.region1_plot)
        sub1.setWindowTitle('Region 1 Plot')
        
        sub2=QMdiSubWindow()
        sub2.setWidget(self.region2_plot)
        sub2.setWindowTitle('Region 2 Plot')
        
        sub3=QMdiSubWindow()
        sub3.setWidget(self.total_plot)
        sub3.setWindowTitle('Total Plot')
        
        sub4=QMdiSubWindow()
        sub4.setWidget(self.time_plot)
        sub4.setWindowTitle('Time Plot')
        
        self.mdi=QMdiArea()
        self.mdi.addSubWindow(sub1)
        self.mdi.addSubWindow(sub2)
        self.mdi.addSubWindow(sub3)
        self.mdi.addSubWindow(sub4)
        
        self.mdi.tileSubWindows()
        self.setCentralWidget(self.mdi)
        
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
        self.calibration_location.setSizePolicy(self.size_policy,
                                                self.size_policy)
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
                           'Comma Seperated File (*.csv);;Text File (*.txt)')
        if self.sync_filename[0]!="":
            self.sync=True
            self.sync_location.setStyleSheet("background-color: green")
            if self.lis==True:
                self.process_new.setEnabled(True)
    def detector_browse(self):
        self.list_filename=QFileDialog.getOpenFileName(self,
                           'Listmode File Location',"",
                           'Comma Seperated File (*.csv);;Text File (*.txt)')
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
        self.setWindowTitle(self.list_filename[0])
        self.save_file.setEnabled(True)
        self.save_roi.setEnabled(True)
        self.popup_()
        self.list_mode_processor=List_Mode()
        s=time.time()
        self.sync_time,sync_channel=Conversion.convert(self.sync_filename[0])
        del sync_channel
        self.list_time,self.list_channel=Conversion.convert(self.list_filename[0])
        
        print('Imported and conveted in {:.2f}s'.format(time.time()-s))
        winsound.MessageBeep()
        delt=(self.sync_time[2]-self.sync_time[1])
        #set the maximum value for the end time and start times
        maxe=int((self.list_time[-1]-self.list_time[0])*1e-6)
        self.end_time.setMaximum(maxe)
        self.end_time.setValue(maxe)
        self.start_time.setMaximum(maxe-1)
        self.start_time.setValue(0)
        self.offset.setMaximum(int(delt-self.duty_cycle.value()/100*delt))
        self.offset.setMinimum(int(-(delt*self.duty_cycle.value()/100)*.5))
        self.view_pop.setEnabled(True)
        self.updater()
        
    def popup_(self):
        self.popup=QWidget()
        self.popup.setWindowTitle('View Controls')
        self.popup.setSizePolicy(self.size_policy,self.size_policy)
        self.popup.setFont(self.font)
        
        start_label=QLabel('Start Time: s')
        start_label.setSizePolicy(self.size_policy, self.size_policy)
        start_label.setFont(self.font)
        self.s_label=start_label
        
        self.start_time=QSlider(Qt.Horizontal)
        self.start_time.setSizePolicy(self.size_policy,self.size_policy)
        self.start_time.setFont(self.font)
        self.start_time.setMinimum(0)
        self.start_time.setMaximum(100)
        self.start_time.setSingleStep(1)
        self.start_time.setValue(10)
        self.start_time.setTickInterval(100)
        self.start_time.setTickPosition(QSlider.TicksBelow)
        self.start_time.valueChanged.connect(self.start_updated)
        
        end_label=QLabel('End Time: s')
        end_label.setSizePolicy(self.size_policy, self.size_policy)
        end_label.setFont(self.font)
        self.e_label=end_label
        
        self.end_time=QSlider(Qt.Horizontal)
        self.end_time.setSizePolicy(self.size_policy,self.size_policy)
        self.end_time.setFont(self.font)
        self.end_time.setMinimum(1)
        self.end_time.setMaximum(100)
        self.end_time.setSingleStep(1)
        self.end_time.setValue(10)
        self.end_time.setTickInterval(100)
        self.end_time.setTickPosition(QSlider.TicksBelow)
        self.end_time.valueChanged.connect(self.end_updated)
        
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
        self.offset.valueChanged.connect(self.offset_changed)
        
        self.update=QPushButton('Update')
        self.update.setSizePolicy(self.size_policy,self.size_policy)
        self.update.setFont(self.font)
        self.update.clicked.connect(self.updater)
        
        layout=QGridLayout()
        layout.addWidget(start_label,0,0)
        layout.addWidget(self.start_time,0,1)
        layout.addWidget(end_label, 1, 0)
        layout.addWidget(self.end_time,1,1)
        layout.addWidget(self.duty_label,2,0)
        layout.addWidget(self.duty_cycle,2,1)
        layout.addWidget(self.offset_label,3,0)
        layout.addWidget(self.offset,3,1)
        layout.addWidget(self.update,4,0)
        
        self.popup.setLayout(layout)
        self.duty_changed()
        self.offset_changed()
        self.popup.show()
        
    def start_updated(self):
        time=self.start_time.value()
        self.s_label.setText('Start Time: {:.2f}s'.format(time))
        self.end_time.setMinimum(time+1)

    def end_updated(self):
        time=self.end_time.value()
        self.e_label.setText('End Time: {:.2f}s'.format(time))
        
    def duty_changed(self):
        self.duty_label.setText('Duty Cycle: {:.2f}%'.format(
            self.duty_cycle.value()))
        
    def offset_changed(self):
        self.offset_label.setText('Offset from sync: {:.1f} us'.format(
            self.offset.value()))
        
    def updater(self):
        delta_time=self.duty_cycle.value()/100*(
                self.sync_time[2]-self.sync_time[1])
        delt=(self.sync_time[2]-self.sync_time[1])
        self.offset.setMinimum(-int((delt*self.duty_cycle.value()/100)*.75))
        sync_width=delta_time
        delta_time+=self.offset.value()
        self.delta_time=delta_time
        start=float(self.start_time.value())*1e6
        end=float(self.end_time.value())*1e6
        sb,se=Timing.Splitter(self.sync_time,len(self.sync_time),
                                            start,end)
        cb,ce=Timing.Splitter(self.list_time,len(self.list_time),
                                            start,end)
        self.region1_spec,self.region2_spec,self.time=self.list_mode_processor.timing(
                                        delta_time,self.sync_time[sb:se],
                                        self.list_time[cb:ce],self.list_channel[cb:ce])
        total=[]
        for i in range(len(list(self.region2_spec.values()))):
            total.append(list(self.region2_spec.values())[i]+list(
                    self.region1_spec.values())[i])
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
        self.region1_ax.set_ylabel('Counts')
        self.region2_ax.set_ylabel('Counts')
        self.total_ax.set_ylabel('Counts')
        self.total_ax.legend()
        self.region1_canvas.draw()
        self.region2_canvas.draw()
        self.total_canvas.draw()
        
        #plot the timing stuff
        self.time_ax.clear()
        self.time_ax.plot(self.time[1][:-1],
                          self.time[0][:-1],'*',label='Time Distribution')
        height=max(self.time[0])
        ys=[0,height,height,0]
        xs=[0,0,sync_width,sync_width]
        self.time_ax.plot(xs,ys,
                  label='Sync Pulse, {:.1f}%'.format(self.duty_cycle.value()))
        self.time_ax.axvline(delta_time,
             label='Region divider, {:.1f}us\nafter pulse'.format(delta_time))
        self.time_ax.set_xlabel(r'Time [$\mu$s]')
        self.time_ax.set_title('Time')
        self.time_ax.set_ylabel('Counts')
        self.time_ax.set_yscale('log')
        self.time_ax.legend()
        self.time_canvas.draw()
        winsound.MessageBeep()
        
    def save_spectrum(self):
        items=['Region 1','Region 2','Time Decay']
        # self.updater()
        text,ok=QInputDialog.getItem(self,'Save Spectrum','Saving:',
                                     items,0,False)
        if ok and text:
            name=QFileDialog.getSaveFileName(self,'File Name','',
                             'Text File (*.txt);;Comma Seperated File (*.csv)')
            try:
                f=open(name[0],'w')
                if text==items[0] and name[0]!=" ":
                    counts=list(self.region1_spec.values())
                    bins=list(self.region1_spec.keys())
                    for i in range(len(bins)-1):
                        f.write('{}\n'.format(counts[i]))
                if text==items[1] and name[0]!='':
                    counts=list(self.region2_spec.values())
                    bins=list(self.region2_spec.keys())
                    for i in range(len(bins)-1):
                        f.write('{}\n'.format(counts[i]))
                if text==items[2] and name[0]!='':
                    times=self.time[1][:-1]
                    counts=self.time[0][:-1]
                    f.write('Time[us],counts\n')
                    for i in range(len(counts)):
                        f.write('{:.9f},{}\n'.format(times[i],counts[i]))
                    
                f.close()
            except:
                pass
    
    def initiate(self):
        self.geometry()
        self.updater()
        
    def deviation(self):
        Arrival_Spread(self.sync_filename[0]).process()
        
    def ROI_Arrivals(self):
        #check to see if a calibration file exists, if not make them get one
        if not self.calibration:
            self.calibration_browse()
        list_time=np.asarray(self.list_time)
        list_channel=np.asarray(self.list_channel)
        sync_time=np.asarray(self.sync_time)
        calibration=np.asarray(self.calibration_data)
        self.view=ROI_Viewer(list_time,list_channel,sync_time,calibration)
        self.view.processer.clicked.connect(self.roi_arrive)
        
    def roi_arrive(self):
#        while self.view.done!=True:
#            False
        self.time_ax.plot(self.view.bins,self.view.output,'*',
         label='ROI of {}MeV-{}MeV'.format(self.view.lower,self.view.upper))
        self.time_ax.legend()
        self.time_canvas.draw()
        
    def ROI_Spectrum_Saving(self):
        '''Saving the roi pulses and their respective timing to later perform
        an integration to find the MDM'''
        if not self.calibration:
            self.calibration_browse()
        list_time=np.asarray(self.list_time)
        list_channel=np.asarray(self.list_channel)
        calibration=np.asarray(self.calibration_data)
        sync_time=np.asarray(self.sync_time)
        lower,ok=QInputDialog.getDouble(self, 'Lower ROI', 'Lower Bound (MeV)',9.6,0,14,4)
        upper,ok2=QInputDialog.getDouble(self, 'Upper ROI', 'Upper Bound (MeV)',10.9,0,14,4)
        if ok and ok2:
    #     #outputs the pulses and associated times to save and integrate to
    #     #calculate the detection probability at integrated time windows
            s=time.time()
            print('Begin processing data')
            pulses,times=Timing.ROI_Timing(sync_time,int(len(sync_time)),
                                           list_time,list_channel, 
                                           self.delta_time,8192,
                                           calibration,upper,lower)
            print('Done processing in {:.2f}s'.format(time.time()-s))
        return pulses,times
    
    def save_roi_csv(self):
        name,ok=QFileDialog.getSaveFileName(self,'Safe File Name','',
                              'Comma Seperated File (*.csv)')
        if ok:
            f=open(name,'w')
            f.write('Pulse_Height(MeV),Time(s)\n')
            pulse,time=self.ROI_Spectrum_Saving()
            for i in range(len(pulse)):
                f.write('{:.3f},{:.3f}\n'.format(pulse[i],time[i]*1e-6))
            f.close()
            print('All finished')
            
if __name__ =="__main__":
    app=QApplication(sys.argv)
    ex=List_Mode_Viewer()
    sys.exit(app.exec_())