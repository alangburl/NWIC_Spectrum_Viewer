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
    def __init__(self):
        super().__init__()
        self.setWindowTitle('List Mode Viewer')
        self.font=QFont()
        self.font.setPointSize(12)
        self.size_policy=QSizePolicy.Expanding
        self.menu()
        
        self.showMaximized()
        self.show()
        
    def menu(self):
        self.menuFile=self.menuBar().addMenu('&File')
        self.load_new=QAction('&Load New Data')
        self.load_new.triggered.connect(self.loading)
        self.load_new.setShortcut('CTRL+N')
    
        self.menuFile.addActions([self.load_new])
    def geometry(self):
        
    def loading(self):
        pass
        
if __name__ =="__main__":
    app=QApplication(sys.argv)
    ex=List_Mode_Viewer()
    sys.exit(app.exec_())