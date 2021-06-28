from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from pyqtgraph import *
from pyqtgraph import PlotWidget, PlotItem
import pyqtgraph as pg
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
import pathlib
import numpy as np
from MainWindow import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.timer1 = QtCore.QTimer()
        self.timer2 = QtCore.QTimer()
        self.timer3 = QtCore.QTimer()
        self.ui.open1.triggered.connect(lambda : self.load(0))
        self.ui.open2.triggered.connect(lambda : self.load(1))
        self.ui.open3.triggered.connect(lambda : self.load(2))
        self.ui.Print.triggered.connect(self.print) 
        self.ui.Exit.triggered.connect(lambda : self.close_app())
        self.ui.Play1.clicked.connect(lambda : self.play(0))
        self.ui.Play2.clicked.connect(lambda : self.play(1))
        self.ui.Play3.clicked.connect(lambda : self.play(2))
        self.ui.Pause1.clicked.connect(lambda : self.pause(0))
        self.ui.Pause2.clicked.connect(lambda : self.pause(1))
        self.ui.Pause3.clicked.connect(lambda : self.pause(2))
        self.ui.Clear1.triggered.connect(lambda : self.clear(0))
        self.ui.Clear2.triggered.connect(lambda : self.clear(1))
        self.ui.Clear3.triggered.connect(lambda : self.clear(2))
        self.ui.Zoom_In1.triggered.connect(lambda : self.zoomIn(0))
        self.ui.Zoom_Out1.triggered.connect(lambda : self.zoomOut(0))
        self.ui.Zoom_In2.triggered.connect(lambda : self.zoomIn(1))
        self.ui.Zoom_Out2.triggered.connect(lambda : self.zoomOut(1))
        self.ui.Zoom_In3.triggered.connect(lambda : self.zoomIn(2))
        self.ui.Zoom_Out3.triggered.connect(lambda : self.zoomOut(2))
        self.ui.ZoomIn1.clicked.connect(lambda : self.zoomIn(0))
        self.ui.ZoomOut1.clicked.connect(lambda : self.zoomOut(0))
        self.ui.ZoomIn2.clicked.connect(lambda : self.zoomIn(1))
        self.ui.ZoomOut2.clicked.connect(lambda : self.zoomOut(1))
        self.ui.ZoomIn3.clicked.connect(lambda : self.zoomIn(2))
        self.ui.ZoomOut3.clicked.connect(lambda : self.zoomOut(2))
        
        self.ui.Scrollr1.clicked.connect(lambda :  self.scroll(1,0))
        self.ui.Scrolll1.clicked.connect(lambda : self.scroll(2,0))
        self.ui.Scrollu1.clicked.connect(lambda :  self.scroll(3,0))
        self.ui.Scrolld1.clicked.connect(lambda :  self.scroll(4,0))

        self.ui.Scrollr2.clicked.connect(lambda : self.scroll(1,1))
        self.ui.Scrolll2.clicked.connect(lambda :  self.scroll(2,1))
        self.ui.Scrollu2.clicked.connect(lambda :  self.scroll(3,1))
        self.ui.Scrolld2.clicked.connect(lambda :  self.scroll(4,1))

        self.ui.Scrollr3.clicked.connect(lambda : self.scroll(1,2))
        self.ui.Scrolll3.clicked.connect(lambda :  self.scroll(2,2))
        self.ui.Scrollu3.clicked.connect(lambda :  self.scroll(3,2))
        self.ui.Scrolld3.clicked.connect(lambda :  self.scroll(4,2))

        self.pen1 = pg.mkPen(color=(0, 0, 255))
        self.pen2 = pg.mkPen(color=(0, 255, 0))
        self.pen3 = pg.mkPen(color=(255, 0, 0))
        self.Pen = [self.pen1 , self.pen2 , self.pen3]
        self.Timer=[self.timer1 , self.timer2 , self.timer3]
        self.GraphicsView=[self.ui.graphicsView , self.ui.graphicsView_2 , self.ui.graphicsView_3]
      
    def read_file(self, Channel_ID):
        for i in range(3):
            if Channel_ID == i:
                path = QFileDialog.getOpenFileName()[0]
                if pathlib.Path(path).suffix == ".csv":
                    self.data = np.genfromtxt(path, delimiter=',')
                    self.x = list(self.data[:, 0])
                    self.y = list(self.data[:, 1])
                    self.Spectrogram(self.x, self.y , i )
     
    def load(self , Channel_ID):
        for i in range(3):
            if Channel_ID == i: 
                self.read_file(i)
                self.data_line =self.GraphicsView[i].plot(self.x, self.y, pen=self.Pen[i])
                self.GraphicsView[i].plotItem.setLimits(xMin=0, xMax=12, yMin=-0.6, yMax=0.6)
                self.IDX= 0
                self.Timer[i].setInterval(100)
                self.Timer[i].timeout.connect(lambda : self.update_plot_data(i))
                self.Timer[i].start()
    
    def update_plot_data(self , Channel_ID):
        for i in range(3):
            if Channel_ID == i:
                x = self.x[:self.IDX]
                y = self.y[:self.IDX]
                self.IDX += 10
                if self.IDX > len(self.x):
                    self.IDX = 0
                if self.x[self.IDX] > 0.5:
                    self.GraphicsView[i].setLimits(xMin=min(x, default=0), xMax=max(x, default=0))  # disable paning over xlimits
                self.GraphicsView[i].plotItem.setXRange(max(x, default=0) - 0.5, max(x, default=0))
                self.data_line.setData(x, y)   

    def pause(self , Channel_ID) :
        for i in range (3):
            if Channel_ID == i:
                self.Timer[i].stop()

    def play(self , Channel_ID) :
        for i in range (3):
            if Channel_ID == i:
                self.Timer[i].start()

    def clear(self , Channel_ID) :
        for i in range(3):
            if Channel_ID == i:
                self.GraphicsView[i].clear()
                self.pause(i)   

    def zoomIn(self , Channel_ID):
        for i in range(3):
            if Channel_ID == i:
                xrange, yrange = self.GraphicsView[i].viewRange()
                self.GraphicsView[i].setYRange(yrange[0]/2, yrange[1]/2, padding=0)
                self.GraphicsView[i].setXRange(xrange[0]/2, xrange[1]/2, padding=0)

    def zoomOut(self, Channel_ID):
        for i in range(3):
            if Channel_ID == i:
                xrange, yrange = self.GraphicsView[i].viewRange()
                self.GraphicsView[i].setYRange(yrange[0]*2, yrange[1]*2, padding=0)
                self.GraphicsView[i].setXRange(xrange[0]*2, xrange[1]*2, padding=0) 

    def Scroll(self , RIGHT_LEFT_UP_DOWN , Channel_ID):
        rangeX = 0 
        rangeY = 0

        if RIGHT_LEFT_UP_DOWN == 1:
            rangeX = 0.5 
            self.GraphicsView[Channel_ID].getViewBox().translateBy(x=rangeX, y=rangeY)
        elif RIGHT_LEFT_UP_DOWN == 2:
            rangeX = -0.5 
            self.GraphicsView[Channel_ID].getViewBox().translateBy(x=rangeX, y=rangeY)
        elif RIGHT_LEFT_UP_DOWN == 3:
            rangeY = +0.9
            self.GraphicsView[Channel_ID].getViewBox().translateBy(x=rangeX, y=rangeY)
        elif RIGHT_LEFT_UP_DOWN == 4:
            rangeY = -0.9 
            self.GraphicsView[Channel_ID].getViewBox().translateBy(x=rangeX, y=rangeY)
    
    def Spectrogram(self, x , y , Channel_ID ):
        for i in range(3):
            if Channel_ID == i:
                plt.subplot(3,2,2*i+1)
                plt.plot(x,y)
                plt.subplot(3,2,2*i+2)
                plt.specgram(y,Fs=200)  

    def print(self):
        plt.savefig('Spectrogram.pdf')

    def close_app(self):
        sys.exit()

if __name__ == '__main__':      
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
       
