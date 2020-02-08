from Load_New import Load_New as New

#prefined imports
import sys
from PyQt5.QtWidgets import (QApplication, QPushButton,QWidget,QGridLayout,
                             QSizePolicy,QComboBox,QLineEdit,QTextEdit,
                             QMessageBox,QInputDialog,QMainWindow,QAction
                             ,QDockWidget,QTableWidgetItem,QVBoxLayout,
                             QTabWidget,QSystemTrayIcon,QListView,
                             QAbstractItemView,QCompleter,QLabel)
from PyQt5.QtGui import (QFont,QIcon, QImage, QPalette, QBrush,
                        QStandardItemModel,QStandardItem)
from PyQt5.QtCore import Qt,QModelIndex

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)

class Viewer(QMainWindow):
    loaded_spectrum={}
    plotted_spectrum=[]
    nonplot=[]
    e_plot=[]
    mini=0
    maxi=14
    def __init__(self):
        super().__init__()
        self.size_policy=QSizePolicy.Expanding
        self.font=QFont()
        self.font.setPointSize(12)
#        self.showMaximized()
        self.setWindowTitle('Calibrated Spectrum Viewer')
        self.menu()
        self.geometry()
        self.show()
        
    def menu(self):
        self.menuFile=self.menuBar().addMenu('&File')
        self.load_new=QAction('&Load New Spectrum')
        self.load_new.triggered.connect(self.new_spectrum)
        self.load_new.setShortcut('Ctrl+O')
        self.load_new.setToolTip('Load a new calibrated spectrum')
        
        self.change_zoom=QAction('&Change Zoom Location')
        self.change_zoom.triggered.connect(self.zoom_change)
        self.change_zoom.setShortcut('Ctrl+Z')
        self.change_zoom.setToolTip('Change the initial zoom on the spectrum')
        self.menuFile.addActions([self.load_new,self.change_zoom])
        
        self.menuView=self.menuBar().addMenu('&View')
        self.view_energies=QAction('&View Energies')
        self.view_energies.setToolTip('Add Vertical Energy Lines')
        self.view_energies.triggered.connect(self.vert_lines)
        self.menuView.addActions([self.view_energies])
        
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
        self.close_spectrum.doubleClicked[QModelIndex].connect(self.update_close)
        
        self.close_.setWidget(self.close_spectrum)
        self.addDockWidget(Qt.RightDockWidgetArea,self.close_)
        
        #add the plot window
        self.plot_window=QWidget()
        layout=QVBoxLayout()
        self._canvas=FigureCanvas(Figure())
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
        self.loaded_spectrum[legend]=[calibr,counts]
        self.loader.appendRow(QStandardItem(legend))
        self.nonplot.append(legend)
        
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
        
    def add_lines(self):
        text=self.line.text().split(sep=',')
        self.e_plot=[float(i) for i in text]
        self.widget.close()
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
        print(self.nonplot)
#        self.unloader.appendRow(QStandardItem(val))
        self.plotted_spectrum.append(item.text())
#        #first clear all the values in the loaded section
        for i in range(len(self.nonplot)):
            self.loader.removeRow(i)
#        self.nonplot.remove(val)
#        for i in self.nonplot:
#            self.loader.appendRow(QStandardItem(i))
        self.replot()

    def update_close(self,index):
        item=self.unloader.itemFromIndex(index)
        val=item.text()
#        self.loader.appendRow(QStandardItem(val))
        print(self.plotted_spectrum)
        #clear all the items in the the unloading widget
        for i in range(len(self.plotted_spectrum)):
            self.unloader.removeRow(i)
        #remove the value from the plotted spectrum and add it to the not plot
        self.plotted_spectrum.remove(val)
#        self.nonplot.append(val)
#        
#        #add the items still plotted back
#        for i in self.plotted_spectrum:
#            self.unloader.appendRow(QStandardItem(i))
        self.replot()
        
    def replot(self):
        self.static_ax.clear()
        self.static_ax.set_yscale('log')
        self.static_ax.set_xlim(self.mini,self.maxi)
        self.static_ax.set_xlabel('Energy [MeV]')
        self.static_ax.set_ylabel('Count Rate [cps]')
        for i in self.e_plot:
            self.static_ax.axvline(i,color='r',linestyle='--',linewidth=0.8)
            
        for i in self.plotted_spectrum:
            spec=self.loaded_spectrum[i]
            self.static_ax.plot(spec[0],spec[1],label=i)
        self.static_ax.legend()
        self._canvas.draw()
        
if __name__=="__main__":
    app=QApplication(sys.argv)
    ex=Viewer()
    sys.exit(app.exec_())