from Probability_New import Load_New

import sys
import numpy as np
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QSizePolicy,QLineEdit,
                             QMainWindow,QAction,QVBoxLayout
                             ,QLabel,QFileDialog,QTextEdit,
                             QInputDialog,QSlider,QHBoxLayout,QDockWidget)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt,QModelIndex
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)

class Plotter(QMainWindow):
    legends=[]
    base_names=[]
    database={}
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
        self.figure.tight_layout()
    def menu(self):
        self.menuFile=self.menuBar().addMenu('&File')
        self.load_new=QAction('&Load New Spectrum')
        self.load_new.triggered.connect(self.new_graph)
        self.load_new.setShortcut('Ctrl+O')
        self.load_new.setToolTip('Load a new calibrated spectrum')
        
        self.save_figure=QAction('&Save Spectrum Image')
        self.save_figure.triggered.connect(self.save_fig)
        self.save_figure.setShortcut('Ctrl+S')
        self.save_figure.setEnabled(False)
        
        self.clear=QAction('&Clear Graph')
        self.clear.triggered.connect(self.clear_graph)
        self.clear.setEnabled(False)
    
        self.menuFile.addActions([self.load_new,self.save_figure,self.clear])
        
    def geometry(self):
        self.prop_label=QLabel('Detection Probability: 99%')
        self.prop_label.setSizePolicy(self.size_policy, self.size_policy)
        self.prop_label.setFont(self.font)
        
        self.prob=QSlider(Qt.Horizontal)
        self.prob.setSizePolicy(self.size_policy,self.size_policy)
        self.prob.setFont(self.font)
        self.prob.setMinimum(0)
        self.prob.setMaximum(100)
        self.prob.setSingleStep(1)
        self.prob.setValue(99)
        self.prob.setTickInterval(10)
        self.prob.setTickPosition(QSlider.TicksBelow)
        self.prob.valueChanged.connect(self.label_update)
        
        self.plot_window=QWidget()
        layout=QVBoxLayout()
        self.figure=Figure()
        self._canvas=FigureCanvas(self.figure)
        self.toolbar=NavigationToolbar(self._canvas,self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self._canvas)
        self.plot_window.setLayout(layout)
        
        topper=QDockWidget('Adjustments')
        
        horwidget=QWidget()
        hlayout=QHBoxLayout()
        hlayout.addWidget(self.prop_label)
        hlayout.addWidget(self.prob)
        horwidget.setLayout(hlayout)
        topper.setWidget(horwidget)
        self.addDockWidget(Qt.TopDockWidgetArea, topper)
        
        self.setCentralWidget(self.plot_window)
        self.static_ax = self._canvas.figure.subplots()
        self.static_ax.set_xlim(0,1800)
        self.static_ax.set_xlabel('Time [s]')
        self.static_ax.set_ylabel('Probability of Detection [%]')
        
    
    def new_graph(self):
        self.adder=Load_New()
        self.adder.add.clicked.connect(self.new_)
        
    def new_(self):
        self.adder.process()
        
        time,probability=self.adder.time,self.adder.probability
        self.base_names.append(self.adder.name)
        self.database[self.adder.name]=[time,probability]
        self.replot()
        
        
    def replot(self):
        self.static_ax.clear()
        self.static_ax.set_xlim(0,1800)
        self.static_ax.set_xlabel('Time [s]')
        self.static_ax.set_ylabel('Probability of Detection [%]')
        # self.static_ax.set_ylim(0,100)
        markers=['c+','rx','k*','m1','y.','g8','b2','mh','co','k+']
        j=0
        eva=int(self.prob.value())
        for i in self.base_names:
            time,probability=self.database[i]
            try:
                detect_time=np.interp(int(eva),probability,time)

                self.legends.append('{}: {:.2f}s'.format(i,detect_time))
                self.static_ax.plot(time,probability,markers[j],
                label='{}: Time to {}% detection probability: {:.2f}s'.format(
                    i,eva,detect_time))
                j+=1
            except:
                pass
        self.static_ax.axhline(eva,color='r',linestyle='--',linewidth=0.5)
        self.static_ax.legend(prop={'size':18})
        self._canvas.draw()
        self.clear.setEnabled(True)
        self.save_figure.setEnabled(True) 
        
    def save_fig(self):
        options='Portable Network Graphics (*.png);;'
        options_='Joint Photographic Experts Group(*.jpg)'
        options=options+options_
        file_name,ok=QFileDialog.getSaveFileName(self,'Image Save',""
                                              ,options)
        
        if file_name and ok:
            self.figure.savefig(file_name,dpi=600,figsize=(10,10))
    
    def clear_graph(self):
        self.static_ax.clear()
        self.static_ax.set_xlim(0,1800)
        self.static_ax.set_xlabel('Time [s]')
        self.static_ax.set_ylabel('Probability of Detection [%]')
        self.static_ax.set_ylim(0,100)
        self._canvas.draw()
        self.clear.setEnabled(False)
        self.save_figure.setEnabled(False)
        
    def label_update(self):
        val=self.prob.value()
        self.prop_label.setText('Detection Probability: {}%'.format(val))
        self.replot()
        
if __name__=="__main__":
    app=QApplication(sys.argv)
    ex=Plotter()
    sys.exit(app.exec_())
    
    