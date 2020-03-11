
from Load_New import Load_New as New
from Calibration_Window import Calibration_Window as Window
from Save_Spe import Save_Spe
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
        
        self.menuView=self.menuBar().addMenu('&View')
        self.view_energies=QAction('&View Energies')
        self.view_energies.setToolTip('Add Vertical Energy Lines')
        self.view_energies.triggered.connect(self.vert_lines)
        self.view_calibration_energies=QAction('&Calibration Energies')
        self.view_calibration_energies.triggered.connect(self.calib_lines)
        self.view_countrate=QAction('&Count Rates')
        self.view_countrate.triggered.connect(self.rate_tracking)
        self.roi_action=QAction('&ROI Counts')
        self.roi_action.triggered.connect(self.roi_display)
        self.menuView.addActions([self.view_energies,self.change_zoom,
                                  self.view_calibration_energies,
                                  self.view_countrate,self.roi_action])
        
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
        self.static_ax.legend()
        self._canvas.draw()
        
    def save_fig(self):
        options='Portable Network Graphics (*.png);;'
        options_='Joint Photographic Experts Group(*.jpg)'
        options=options+options_
        file_name=QFileDialog.getSaveFileName(self,'Spectrum Image Save',""
                                              ,options)
        
        if file_name:
            self.figure.savefig(file_name[0],dpi=600,figsize=(10,6))
    
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
        self.txt=self.static_ax.text(0.8,0.9,"",transform=self.static_ax.transAxes)
        self.figure.canvas.mpl_connect('motion_notify_event',self.mouse_move)
        
    def mouse_move(self,event):
        if not event.inaxes:
            return
        self.txt.set_text('Energy: {:,.2f} MeV'.format(event.xdata))
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
                scale+=roi_counts[i][j]*timer
            roi[i]=scale
        self.display_roi=QWidget()
        self.display_roi.setWindowTitle('ROI counts')
        rois=QTextEdit()
        rois.setFont(self.font)
        rois.setSizePolicy(self.size_policy,self.size_policy)
        for i in list(roi.keys()):
            rois.append('{}: {} counts'.format(i,roi[i]))
        layout=QVBoxLayout()
        layout.addWidget(rois)
        self.display_roi.setLayout(layout)
        self.display_roi.show()
        
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
        
if __name__=="__main__":
    app=QApplication(sys.argv)
    ex=Viewer()
    sys.exit(app.exec_())