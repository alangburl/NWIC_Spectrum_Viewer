from Detection_Probability import Detection_Probability as DT
from Load_New import Load_New as New
from Calibration_Window import Calibration_Window as Window
from Save_Spe import Save_Spe
from Timing_plotter import Time_Window
from List_Mode_Viewer import List_Mode_Viewer
from std_calculation import net_std
from Decay import Background_Decay as bkg
from Animated_Gaussians import Movie_Maker as movie

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
#prefined imports
import sys
from PyQt5.QtWidgets import (QApplication, QPushButton,QWidget,QGridLayout,
                             QSizePolicy,QLineEdit,
                             QMainWindow,QAction,QVBoxLayout
                             ,QDockWidget,QListView,
                             QAbstractItemView,QLabel,QFileDialog,QTextEdit,
                             QInputDialog)
from PyQt5.QtGui import (QFont,QStandardItemModel,QStandardItem)
from PyQt5.QtCore import Qt,QModelIndex
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)

class Viewer(QMainWindow):
    loaded_spectrum={}
    count_rates={}
    plotted_spectrum=[]
    e_plot=[]
    e_calibration=[]
    mini=0
    maxi=14
    plotted_tracking=[]
    not_plotted_tracking=[]
    def __init__(self):
        super().__init__()
        self.size_policy=QSizePolicy.Expanding
        self.font=QFont()
        self.font.setPointSize(12)
        self.setWindowTitle('Calibrated Spectrum Viewer')
        self.menu()
        self.geometry()
        self.showMaximized()
        self.show()
        
    def menu(self):
        self.menuFile=self.menuBar().addMenu('&File')
        self.load_new=QAction('&Load New Spectrum')
        self.load_new.triggered.connect(self.new_spectrum)
        self.load_new.setShortcut('Ctrl+O')
        self.load_new.setToolTip('Load a new calibrated spectrum')
        
        self.save_figure=QAction('&Save Spectrum Image')
        self.save_figure.triggered.connect(self.save_fig)
        self.save_figure.setShortcut('Ctrl+Shift+S')
        self.save_spec=QAction('&Save Spe File')
        self.save_spec.triggered.connect(self.spe)
        self.save_spec.setShortcut('Ctrl+S')
        self.menuFile.addActions([self.load_new,self.save_figure,
                                  self.save_spec])
        
        self.menuEdit=self.menuBar().addMenu('&Edit')
        self.calibrate_spectrum=QAction('&Calibrate Spectrum')
        self.calibrate_spectrum.triggered.connect(self.spectrum_calibrate)
        self.calibrate_spectrum.setShortcut('Ctrl+G')
        self.calibrate_spectrum.setToolTip('Calibrate a raw spectrum')
        self.menuEdit.addActions([self.calibrate_spectrum])
        
        self.change_zoom=QAction('&Change Zoom Location')
        self.change_zoom.triggered.connect(self.zoom_change)
        self.change_zoom.setShortcut('Ctrl+Z')
        self.change_zoom.setToolTip('Change the initial zoom on the spectrum')
        
        self.menuView=self.menuBar().addMenu('&View Spectrum Data')
        self.view_energies=QAction('&View Energies')
        self.view_energies.setToolTip('Add Vertical Energy Lines')
        self.view_energies.triggered.connect(self.vert_lines)
        self.view_calibration_energies=QAction('&Calibration Energies')
        self.view_calibration_energies.triggered.connect(self.calib_lines)
        self.view_countrate=QAction('&Count Rates')
        self.view_countrate.triggered.connect(self.rate_tracking)
        self.roi_uncertainty=QAction('&ROI Uncertainties')
        self.roi_uncertainty.triggered.connect(self.roi_count_rate_uncertainty)    
        self.res_action=QAction('&Energy Resolution')
        self.res_action.triggered.connect(self.find_peaks)
        
        self.menuView.addActions([self.view_energies,self.change_zoom,
                          self.view_calibration_energies,
                          self.view_countrate,
                          self.roi_uncertainty,self.res_action])
        
        self.menuList=self.menuBar().addMenu('&List Mode Data Analysis')
        self.timing_window=QAction('&View Time Decay')
        self.timing_window.triggered.connect(self.time_display)
        self.list_mode=QAction('&Analyze List Mode Data')
        self.list_mode.triggered.connect(self.list_moder)
        self.detection_probability=QAction('&Detection Probability')
        self.detection_probability.triggered.connect(self.detec_prob)
        self.dieaway=QAction('&Analyze Die Away')
        self.dieaway.triggered.connect(self.bck_die_away)
        self.video=QAction('&Save Probability Videos')
        self.video.triggered.connect(self.save_detec_videos)
        
        self.menuList.addActions([self.timing_window,self.list_mode,
                                  self.detection_probability,
                                  self.dieaway,self.video])
        
    def geometry(self):
        self.open_=QDockWidget('Loaded Spectrums')
        #initialize the widget to be used for loading the spectrum
        self.open_spectrum=QListView(self)
        self.open_spectrum.setFont(self.font)
        self.open_spectrum.setSizePolicy(self.size_policy,self.size_policy)
        self.open_spectrum.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        self.loader=QStandardItemModel()
        self.open_spectrum.setModel(self.loader)
        self.open_spectrum.doubleClicked[QModelIndex].connect(self.update_add)
        
        self.open_.setWidget(self.open_spectrum)
        self.addDockWidget(Qt.LeftDockWidgetArea,self.open_)
        #initialize the widget to remove a spectrum from the plotter
        self.close_=QDockWidget('Plotted Spectrum')
        self.close_spectrum=QListView(self)
        self.close_spectrum.setFont(self.font)
        self.close_spectrum.setSizePolicy(self.size_policy,self.size_policy)
        self.close_spectrum.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        self.unloader=QStandardItemModel()
        self.close_spectrum.setModel(self.unloader)
        self.close_spectrum.doubleClicked[QModelIndex].connect(
                self.update_close)
        
        self.close_.setWidget(self.close_spectrum)
        self.addDockWidget(Qt.RightDockWidgetArea,self.close_)
        
        #add the plot window
        self.plot_window=QWidget()
        layout=QVBoxLayout()
        self.figure=Figure()
        self._canvas=FigureCanvas(self.figure)
        self.toolbar=NavigationToolbar(self._canvas,self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self._canvas)
        self.plot_window.setLayout(layout)
        self.setCentralWidget(self.plot_window)
        self.static_ax = self._canvas.figure.subplots()
        self.static_ax.set_yscale('log')
        self.static_ax.set_xlim(0,14)
        self.static_ax.set_xlabel('Energy [MeV]')
        self.static_ax.set_ylabel('Count Rate [cps]')
        self.figure.tight_layout()
    
    def new_spectrum(self):
        self.vals=New()
        self.vals.add.clicked.connect(self.new_getter)
        
    def new_getter(self):
        self.vals.add_spectrum()
        counts=self.vals.counts
        calibr=self.vals.calibration
        legend=self.vals.legend.text()
        accum_time=self.vals.accum_time
        self.count_rates[legend]=self.vals.count_rate
        self.loaded_spectrum[legend]=[calibr,counts,accum_time]
        self.loader.appendRow(QStandardItem(legend))
        self.not_plotted_tracking.append(legend)
        
    def vert_lines(self):
        self.widget=QWidget()
        self.widget.setWindowTitle('Add Energies')
        current_lines=''
        for i in range(len(self.e_plot)):
            if i!=0:
                current_lines+=',{}'.format(self.e_plot[i])
            else:
                current_lines+='{}'.format(self.e_plot[i])
        self.line=QLineEdit(self)
        self.line.setFont(self.font)
        self.line.setSizePolicy(self.size_policy,self.size_policy)
        self.line.setToolTip('Enter energies in MeV, seperated by commas')
        self.line.setText(current_lines)
        
        self.line_label=QLabel('Energies:',self)
        self.line_label.setFont(self.font)
        self.line_label.setSizePolicy(self.size_policy,self.size_policy)
        
        self.add=QPushButton('Update')
        self.add.setFont(self.font)
        self.add.setSizePolicy(self.size_policy,self.size_policy)
        self.add.clicked.connect(self.add_lines)
        layout=QGridLayout()
        layout.addWidget(self.line_label,0,0)
        layout.addWidget(self.line,0,1)
        layout.addWidget(self.add,1,0,1,2)
        self.widget.setLayout(layout)
        self.widget.show()
        
    def calib_lines(self):
        self.widget1=QWidget()
        self.widget1.setWindowTitle('Add Energies')
        current_lines=''
        for i in range(len(self.e_calibration)):
            if i!=0:
                current_lines+=',{}'.format(self.e_calibration[i])
            else:
                current_lines+='{}'.format(self.e_calibration[i])
        self.line1=QLineEdit(self)
        self.line1.setFont(self.font)
        self.line1.setSizePolicy(self.size_policy,self.size_policy)
        self.line1.setToolTip('Enter energies in MeV used for calibration, seperated by commas')
        self.line1.setText(current_lines)
        
        self.line_label1=QLabel('Energies:',self)
        self.line_label1.setFont(self.font)
        self.line_label1.setSizePolicy(self.size_policy,self.size_policy)
        
        self.add1=QPushButton('Update')
        self.add1.setFont(self.font)
        self.add1.setSizePolicy(self.size_policy,self.size_policy)
        self.add1.clicked.connect(self.add_cal_lines)
        layout=QGridLayout()
        layout.addWidget(self.line_label1,0,0)
        layout.addWidget(self.line1,0,1)
        layout.addWidget(self.add1,1,0,1,2)
        self.widget1.setLayout(layout)
        self.widget1.show()
        
    def add_lines(self):
        text=self.line.text().split(sep=',')
        try:
            self.e_plot=[float(i) for i in text]
        except:
            self.e_plot=[]
        self.widget.close()
        self.replot()
        
    def add_cal_lines(self):
        text=self.line1.text().split(sep=',')
        try:
            self.e_calibration=[float(i) for i in text]
        except:
            self.e_calibration=[]
        self.widget1.close()
        self.replot()        
    
    def zoom_change(self):
        self.change_zoomed=QWidget()
        
        min_label=QLabel('Min:[MeV]',self)
        min_label.setFont(self.font)
        min_label.setSizePolicy(self.size_policy,self.size_policy)
        max_label=QLabel('Max:[MeV]',self)
        max_label.setFont(self.font)
        max_label.setSizePolicy(self.size_policy,self.size_policy)
        
        self.min_=QLineEdit(self)
        self.min_.setFont(self.font)
        self.min_.setSizePolicy(self.size_policy,self.size_policy)
        self.min_.setText(str(self.mini))
        
        self.max_=QLineEdit(self)
        self.max_.setFont(self.font)
        self.max_.setSizePolicy(self.size_policy,self.size_policy)
        self.max_.setText(str(self.maxi))
        
        self.add_=QPushButton('Update')
        self.add_.setFont(self.font)
        self.add_.setSizePolicy(self.size_policy,self.size_policy)
        self.add_.clicked.connect(self.zoomed_update)
        
        layout=QGridLayout()
        layout.addWidget(min_label,0,0)
        layout.addWidget(self.min_,0,1)
        layout.addWidget(max_label,1,0)
        layout.addWidget(self.max_,1,1)
        layout.addWidget(self.add_,2,0,1,2)
        self.change_zoomed.setLayout(layout)
        self.change_zoomed.show()
        
    def zoomed_update(self):
        self.mini=float(self.min_.text())
        self.maxi=float(self.max_.text())
        self.change_zoomed.close()
        self.replot()
        
    def update_add(self,index):
        item=self.loader.itemFromIndex(index)
        val=item.text()
        self.plotted_spectrum.append(val)
        #add the item selected to the plotted side
        self.plotted_tracking.append(val)
        self.unloader.appendRow(QStandardItem(val))
        #remove all the values from the add plot 
        self.loader.removeRows(0,self.loader.rowCount())
        #remove the values clicked from the not plotted list
        self.not_plotted_tracking.remove(val)
        #add the remaining items back to the options
        for i in self.not_plotted_tracking:
            self.loader.appendRow(QStandardItem(i))
        self.replot()

    def update_close(self,index):
        item=self.unloader.itemFromIndex(index)
        val=item.text()
        self.plotted_spectrum.remove(val)
        #add the value to the not plotted side
        self.not_plotted_tracking.append(val)
        self.loader.appendRow(QStandardItem(val))
        #remove all the values from the unloading side
        self.unloader.removeRows(0,self.unloader.rowCount())
        #remove the value from the tracking list
        self.plotted_tracking.remove(val)
        #put the items back into the unloader
        for i in self.plotted_tracking:
            self.unloader.appendRow(QStandardItem(i))
        self.replot()
        
    def replot(self):
        self.static_ax.clear()
        self.mouse_tracking()
        self.static_ax.set_yscale('log')
        self.static_ax.set_xlim(self.mini,self.maxi)
        self.static_ax.set_xlabel('Energy [MeV]')
        self.static_ax.set_ylabel('Count Rate [cps]')
        current=list(self.static_ax.get_xticks())
        
        for i in self.e_plot:
            current.append(i)
            self.static_ax.axvline(i,color='r',linestyle='--',linewidth=0.8)
        for i in self.e_calibration:
            current.append(i)
            self.static_ax.axvline(i,color='k',linestyle='-',linewidth=1)
            
        for i in self.plotted_spectrum:
            spec=self.loaded_spectrum[i]
            self.static_ax.plot(spec[0],spec[1],
                                label='{}, Accum Time: {}s'.format(i,spec[2]))
            
        current=[round(float(k),2) for k in current]
        self.static_ax.set_xticks(current)
        self.static_ax.set_xticklabels(current, rotation=90)
        self.static_ax.legend(prop={'size':18})
#        self.static_ax.tick_params(labelsize=18)
        self._canvas.draw()
        self.figure.tight_layout()
        
    def save_fig(self):
        options='Portable Network Graphics (*.png);;'
        options_='Joint Photographic Experts Group(*.jpg)'
        options=options+options_
        file_name,ok=QFileDialog.getSaveFileName(self,'Spectrum Image Save',""
                                              ,options)
        
        if file_name and ok:
            self.figure.savefig(file_name,dpi=600,figsize=(10,10))
    
    def spectrum_calibrate(self):
        '''Launch a calibration window
        '''
        self.calibrator=Window()
        
    def rate_tracking(self):
        '''Show the count rate for all the loaded spectrum
        '''
        self.rater=QWidget()
        self.rater.setWindowTitle('Count Rates')
        editor=QTextEdit()
        editor.setFont(self.font)
        editor.setReadOnly(True)
        editor.setSizePolicy(self.size_policy, self.size_policy)
        
        for i in list(self.count_rates.keys()):
            editor.append('{}: {:,.2f}cps'.format(i,self.count_rates[i]))
        layout=QVBoxLayout()
        layout.addWidget(editor)
        self.rater.setLayout(layout)
        self.rater.show()
        
    def mouse_tracking(self):
        self.txt=self.static_ax.text(0.85,0.6,"",transform=self.static_ax.transAxes)
        self.figure.canvas.mpl_connect('motion_notify_event',self.mouse_move)
        
    def mouse_move(self,event):
        if not event.inaxes:
            return
        self.txt.set_text('Energy: {:,.3f} MeV'.format(event.xdata))
        self._canvas.draw()
        
    def roi_display(self):
        '''Determine the number of counts 
        in a specified ROI and display them
        '''
        self.change_roi=QWidget()
        
        min_label=QLabel('Min:[MeV]',self)
        min_label.setFont(self.font)
        min_label.setSizePolicy(self.size_policy,self.size_policy)
        max_label=QLabel('Max:[MeV]',self)
        max_label.setFont(self.font)
        max_label.setSizePolicy(self.size_policy,self.size_policy)
        
        self.min_roi=QLineEdit(self)
        self.min_roi.setFont(self.font)
        self.min_roi.setSizePolicy(self.size_policy,self.size_policy)
        
        self.max_roi=QLineEdit(self)
        self.max_roi.setFont(self.font)
        self.max_roi.setSizePolicy(self.size_policy,self.size_policy)
        
        self.add_roi=QPushButton('Update')
        self.add_roi.setFont(self.font)
        self.add_roi.setSizePolicy(self.size_policy,self.size_policy)
        self.add_roi.clicked.connect(self.roi_update)
        
        layout=QGridLayout()
        layout.addWidget(min_label,0,0)
        layout.addWidget(self.min_roi,0,1)
        layout.addWidget(max_label,1,0)
        layout.addWidget(self.max_roi,1,1)
        layout.addWidget(self.add_roi,2,0,1,2)
        self.change_roi.setLayout(layout)
        self.change_roi.show()
        
    def roi_update(self):
        self.change_roi.close()
        roi_counts={}
        for i in self.plotted_spectrum:
            calibration=self.loaded_spectrum[i]
            ma=0
            mi=len(calibration[0])
            for j in range(len(calibration[0])):
                if calibration[0][j] <= float(self.max_roi.text()):
                    ma=j
                if calibration[0][j] <=float(self.min_roi.text()):
#                    print(calibration[0][j])
                    mi=j
#            print(mi,ma)
            roi_counts[i]=self.loaded_spectrum[i][1][mi:ma]
            
#        scale the rois by the accumulation time and determine the sum of the 
#        area using np
        roi={}
        for i in list(roi_counts.keys()):
            timer=float(self.loaded_spectrum[i][2])
            scale=0
            for j in range(len(roi_counts[i])):
                scale+=roi_counts[i][j]#*timer
            roi[i]=scale
        self.roi_counts=roi
        if self.display==False:
            self.uncertain()
        if self.display:
            self.display_roi=QWidget()
            self.display_roi.setWindowTitle('ROI counts')
            rois=QTextEdit()
            rois.setFont(self.font)
            rois.setSizePolicy(self.size_policy,self.size_policy)
            for i in list(roi.keys()):
                rois.append('{}: {:.4f} cps'.format(i,roi[i]))
            layout=QVBoxLayout()
            layout.addWidget(rois)
            self.display_roi.setLayout(layout)
            self.display_roi.show()
        self.display=True
        
    def spe(self):
        '''Save the selected file out to an spe file format, even though the
        calibration will likely not be correct
        '''
        items=self.loaded_spectrum.keys()
        text,ok=QInputDialog.getItem(self,'Save Spectrum','Saving:',items,0,False)
        if ok and text:
            name=QFileDialog.getSaveFileName(self,'Spe File Name','','IAEA (*.spe)')
            if name!=" ":
                try:
                    Save_Spe(self.loaded_spectrum[text],text,name)
                except:
                    pass
                
    def time_display(self):
        self.di=Time_Window()
        
    def list_moder(self):
        self.lm=List_Mode_Viewer()
        
    def roi_count_rate_uncertainty(self):
        '''Calculate the std of the ROI count rates-- will 
        eventaully have the ability to indicate which loaded spectrum 
        are desired'''
        self.display=False
        self.roi_display()
        # self.display=True
    def uncertain(self):
        # now to select the foreground and background spectrum:
        foreground,ok=QInputDialog.getItem(self,'Foreground','Select Foreground',
                                      self.roi_counts.keys(),0,False)
        background,ok2=QInputDialog.getItem(self,'Background','Select Background',
                                      self.roi_counts.keys(),0,False)
        if ok and ok2:
            #get the count rates from both of them
            uncer=net_std(self.roi_counts[foreground],self.roi_counts[background])
            u=uncer.calculate_uncertainties()
            net_cr=self.roi_counts[foreground]-self.roi_counts[background]
            self.uncertainty_display(u,net_cr,foreground,background)
            
    def uncertainty_display(self,net_uncer,net_count_rate,foreground,background):
        self.rateu=QWidget()
        self.rateu.setWindowTitle('Count Rates')
        editor=QTextEdit()
        editor.setFont(self.font)
        editor.setReadOnly(True)
        editor.setSizePolicy(self.size_policy, self.size_policy)
        fore_cps=self.roi_counts[foreground]
        back_cps=self.roi_counts[background]
        editorappd=['Foreground: {}: {:.3f} +\- {:.3f} cps'.format(
            foreground,fore_cps,fore_cps**0.5),
                    'Background: {}: {:.3f} +\- {:.3f} cps'.format(
                        background,back_cps,back_cps**0.5),
                    'Net: {:.3f} +\- {:.3f} cps'.format(net_count_rate,net_uncer)
                    ]
        for i in editorappd:
            editor.append(i)
        
        layout=QVBoxLayout()
        layout.addWidget(editor)
        self.rateu.setLayout(layout)
        self.rateu.show()
        
    def bck_die_away(self):
        #get the file 
        file_name,ok=QFileDialog.getOpenFileName(self,
                           'Background Die Away List Mode File',"",
                           'Comma Seperated File (*.csv);;Text File (*.txt)')
        
        num_bins,ok2=QInputDialog.getInt(self,'Enter number of bins','Bins:',300,0,10000)
        if file_name!='' and ok and ok2:
            cts,time=bkg(file_name,num_bins).process_data()
        io=max(cts[1::])
        index=(np.abs(cts-io/2)).argmin()
        t_12=time[index]
        lambd=np.log(2)/t_12
        fit=[io*np.exp(-lambd*i) for i in time]
        plt.plot(time[1::],cts[1::],'*')
        # plt.plot(time[1::],fit[1::])
        plt.ylabel('Count Rate (cps)')
        plt.xlabel('Time (s)')
        plt.show()
        f=open('Back_Die_Away.csv','w')
        f.write('Time,Counts\n')
        for i in range(len(cts)):
            f.write('{:.5f},{:.5f}\n'.format(cts[i],time[i]))
        f.close()
        
    def detec_prob(self):
        #get the foreground and background file names and info
        #get the file 
        file_nameb,ok=QFileDialog.getOpenFileName(self,
                           'Background List Mode File',"",
                           'Comma Seperated File (*.csv);;Text File (*.txt)')
        file_namef,ok2=QFileDialog.getOpenFileName(self,
                           'Foreground List Mode File',"",
                           'Comma Seperated File (*.csv);;Text File (*.txt)')
        if ok and ok2:
            num,ok3=QInputDialog.getInt(self,'Start Value','Value:',200,0,3000)
            if ok3:
                evals=np.linspace(num,1800,181)
                detection_probability=DT(file_namef,file_nameb,evals)
                probs=detection_probability.probs
                probs=[i*100 for i in probs]
                # print(probs[0:50])
                time_detect=np.interp(99,probs,evals)
                plt.figure(1)
                plt.plot(evals, probs,'*')
                plt.axvline(time_detect,
                            label='Time to 99% detection probability: {:.2f}s'.format(time_detect))
                plt.xlabel('Time(s)')
                plt.ylabel('Probability (%)')
                plt.legend()
                # print(probs)
                plt.show()
                
                #save the raw data out
                fore_sums=detection_probability.f_sums
                back_sums=detection_probability.b_sums
                analysis_times=detection_probability.a_times
                raw_name,ok3=QFileDialog.getSaveFileName(self,
                               'Raw Data Save File Name',"",
                               'Comma Seperated File (*.csv);;Text File (*.txt)')
                if ok3:
                    f=open(raw_name,'w')
                    for i in range(len(fore_sums)):
                        f.write('{},{},{:.4f},{:.4f}\n'.format(fore_sums[i],
                                                       back_sums[i],
                                                       analysis_times[i],
                                                       probs[i]))
                    f.close()
                
    def save_detec_videos(self):
        file_nameb,ok=QFileDialog.getOpenFileName(self,
                       'Raw Data File',"",
                       'Comma Seperated File (*.csv);;Text File (*.txt)')
        file_nameg,ok1=QFileDialog.getSaveFileName(self,
                           'Curve Save File',"",
                           'Multimeda (*.mp4)')
        file_namep,ok2=QFileDialog.getSaveFileName(self,
                           'Probability Save File',"",
                           'Multimeda (*.mp4)')     
        
        if ok and ok1 and ok2:
            Movie=movie(file_nameb,file_nameg,file_namep)
            Movie.save_gaussian()
            Movie.save_probability()
            
    def find_peaks(self):
        #first get all the plotted spectrum names
        loaded_spectrum=self.plotted_spectrum
        selection,ok=QInputDialog.getItem(self, 'Energy Resolution', 
                                          'Selection', loaded_spectrum,
                                          0,False)
        if ok:
            x=self.loaded_spectrum[selection][1]
            y=self.loaded_spectrum[selection][0]
        #then let the user select which one to pick
        
        #then get the counts to analyze
        
        
            peaks, properties = signal.find_peaks(x,width=3,distance=2)
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
                
            plt.plot(y,x)
            plt.yscale('log')
            _,y_max=plt.gca().get_ylim()
            y_max=y_max-.5*y_max
            for i in range(len(peaks)):
                plt.axvline(y[int(peaks[i])],linestyle='--',color='m',linewidth=1)
                v=y[int(peaks[i])]+0.005*y[int(peaks[i])]
                plt.annotate('{:.2f}%'.format(e_res[i]), xy=(v,y_max), 
                             rotation='vertical',color='m')
            # plt.axvspan(y[int(left_sig[2])],y[int(right_sig[2])],facecolor='g',alpha=0.5)
            plt.show()
            return peaks,e_res
            
if __name__=="__main__":
    app=QApplication(sys.argv)
    ex=Viewer()
    sys.exit(app.exec_())