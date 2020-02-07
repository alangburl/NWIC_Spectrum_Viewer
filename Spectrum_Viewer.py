from Load_New import Load_New as New

#prefined imports
import sys,os
import numpy as np
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QPushButton,QWidget,QGridLayout,
                             QSizePolicy,QComboBox,QLineEdit,QTextEdit,
                             QMessageBox,QInputDialog,QMainWindow,QAction
                             ,QDockWidget,QTableWidgetItem,QVBoxLayout,
                             QTabWidget,QSystemTrayIcon,QListView,
                             QAbstractItemView,QCompleter)
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
#        t = np.linspace(0, 10, 501)
#        self._static_ax.plot(t, np.tan(t), ".")
##        self._static_ax.tight_layout()
#        self._static_ax.set_ylabel('Value')
    
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
    
    def zoom_change(self):
        print('change_zoom')
        
    def update_add(self,index):
        item=self.loader.itemFromIndex(index)
        val=item.text()
        self.unloader.appendRow(QStandardItem(item))
        self.plotted_spectrum.append(item.text())
#        #first clear all the values in the loaded section
        for i in range(len(self.nonplot)):
            self.loader.removeRow(i)
        print(val)
        self.nonplot.remove(val)
        for i in self.nonplot:
            self.loader.appendRow(QStandardItem(item.text()))
        self.replot()

    def update_close(self,index):
        item=self.unloader.itemFromIndex(index)
        val=item.text()
        #clear all the items in the the unloading widget
        for i in range(len(self.plotted_spectrum)):
            self.unloader.removeRow(i)
        #remove the value from the plotted spectrum and add it to the not plot
        self.plotted_spectrum.remove(val)
        self.nonplot.append(val)
        self.loader.appendRow(QStandardItem(val))
        #add the items still plotted back
        for i in self.plotted_spectrum:
            self.unloader.appendRow(QStandardItem(i))
        self.replot()
        
    def replot(self):
        self.static_ax.clear()
        self.static_ax.set_yscale('log')
        self.static_ax.set_xlim(0,14)
        self.static_ax.set_xlabel('Energy [MeV]')
        self.static_ax.set_ylabel('Count Rate [cps]')
        for i in self.plotted_spectrum:
            spec=self.loaded_spectrum[i]
            self.static_ax.plot(spec[0],spec[1],label=i)
        self.static_ax.legend()
        self._canvas.draw()
        
if __name__=="__main__":
    app=QApplication(sys.argv)
    ex=Viewer()
    sys.exit(app.exec_())