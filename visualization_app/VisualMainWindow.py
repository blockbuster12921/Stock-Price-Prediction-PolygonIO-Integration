from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

import matplotlib
matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

import pandas as pd
import seaborn as sb
from matplotlib import pyplot as plt
import mplfinance as mpl

class VisualMainWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super(VisualMainWindow, self).__init__(*args, **kwargs)
        self.mainLayout = QVBoxLayout(self)

        # Create the objects
        self.controlButtonGroupBox = self.createControlButtonGroupBox()
        self.featureGroupBox = self.createFeatureGroupBox()
        self.displayCanvas = MplCanvas()

        # Add all the objects into the main layout
        self.mainLayout.addWidget(self.controlButtonGroupBox)
        self.mainLayout.addWidget(self.featureGroupBox)
        self.mainLayout.addWidget(self.displayCanvas)

        # Set the custom design
        self.setCustomStyle()

    def createControlButtonGroupBox(self):
        groupBox = QGroupBox()
        groupBoxLayout = QHBoxLayout(groupBox)
        groupBox.setFixedHeight(70)

        # Create the items 
        self.loadPushButton = QPushButton('Load')
        groupBoxLayout.addWidget(self.loadPushButton)
        spaceItem = QSpacerItem(150, 10, QSizePolicy.Expanding)
        groupBoxLayout.addSpacerItem(spaceItem)
        self.linePlotButtonGroup = QButtonGroup()
        self.candleChartButtonGroup = QButtonGroup()
        self.linePlotButtons = []
        self.candleChartButtons = []
        linePlotButtonNames = ['1H', '24H', '1W', '1M', '1Y', '3Y']
        candleChartButtonNames = ['1M', '5M', '15M', '1H', '8H', '1D', '1W']
        for i in range(6):
            self.linePlotButtons.append(QPushButton(linePlotButtonNames[i], checkable=True))
            self.linePlotButtonGroup.addButton(self.linePlotButtons[i])
            groupBoxLayout.addWidget(self.linePlotButtons[i])
        for i in range(7):
            self.candleChartButtons.append(QPushButton(candleChartButtonNames[i], checkable=True))
            self.candleChartButtonGroup.addButton(self.candleChartButtons[i])
            groupBoxLayout.addWidget(self.candleChartButtons[i])
            self.candleChartButtons[i].setHidden(True)
        
        selectPushButtonGroup = QButtonGroup()
        self.linePlotSelectPushButton = QPushButton('Line', checkable=True)
        self.candleChartSelectPushButton = QPushButton('Chart')
        selectPushButtonGroup.addButton(self.linePlotSelectPushButton)
        selectPushButtonGroup.addButton(self.candleChartSelectPushButton)
        groupBoxLayout.addWidget(self.linePlotSelectPushButton)
        groupBoxLayout.addWidget(self.candleChartSelectPushButton)

        # Connect the signals and slots of pushbuttons
        self.loadPushButton.clicked.connect(self.slotLoadPushButtonClicked)
        self.linePlotSelectPushButton.clicked.connect(self.slotLinePlotSelectPushButtonClicked)
        self.candleChartSelectPushButton.clicked.connect(self.slotCandleChartSelectPushButtonClicked)
        self.linePlotButtonGroup.buttonClicked[int].connect(self.slotLinePlotButtonClicked)
        self.candleChartButtonGroup.buttonClicked[int].connect(self.slotCandleChartButtonClicked)
        return groupBox
    
    def createFeatureGroupBox(self):
        groupBox = QGroupBox()
        groupBoxLayout = QHBoxLayout(groupBox)
        groupBox.setFixedHeight(70)

        # Create the items
        self.featureNameLabels = []
        self.featureValueLabels = []
        featureNames = ['Open', 'High', 'Low', 'Close', 'Volume']
        featureValues = ['0', '0', '0', '0', '0']
        for i in range(5):
            self.featureNameLabels.append(QLabel(featureNames[i]))
            self.featureValueLabels.append(QLabel(featureValues[i]))
            groupBoxLayout.addWidget(self.featureNameLabels[i])
            groupBoxLayout.addWidget(self.featureValueLabels[i])
        return groupBox
        # self.createLinePlotButtonGroupBox()


    # Define Slots of PushButtons
    def slotLoadPushButtonClicked(self):
        print('slotLoadPushButtonClicked')
        self.fileName, _ = QFileDialog.getOpenFileNames(self,\
            "QFileDialog.getOpenFileNames()", "","Excel Files (*.csv;*.xlsx))")
        self.df = pd.read_csv(self.fileName[0])
        self.df = self.df[['time stamp', 'open', 'high', 'low', 'close']]
        self.plotLinePlot()
        # sb.lineplot(data=self.df, x='time stamp', y='close')
        # plt.show()
        

    def slotLinePlotSelectPushButtonClicked(self):
        print('slotLinePlotSelectPushButtonClicked')
        for i in range(len(self.linePlotButtons)):
            self.linePlotButtons[i].setHidden(False)
        for i in range(len(self.candleChartButtons)):
            self.candleChartButtons[i].setHidden(True)
        self.plotLinePlot()


    def slotCandleChartSelectPushButtonClicked(self):
        print('slotCandleChartSelectPushButtonClicked')
        for i in range(len(self.linePlotButtons)):
            self.linePlotButtons[i].setHidden(True)
        for i in range(len(self.candleChartButtons)):
            self.candleChartButtons[i].setHidden(False)
        self.plotCandleStickChart()

    def slotLinePlotButtonClicked(self, i):
        print("111111")
        print(i)

    def slotCandleChartButtonClicked(self, i):
        print("22222")
        print(i)

    # Plot the lineplot and candlestick chart
    def plotLinePlot(self):
        df_lp = self.df[['time stamp', 'close']]
        df_lp.index = pd.to_datetime(df_lp['time stamp'])
        self.displayCanvas.axes.clear()
        self.displayCanvas.axes.plot(df_lp['close'])
        self.displayCanvas.draw()
        print(len(self.df))
    
    def plotCandleStickChart(self):
        print('plotCandleStickChart')
        df_cs = self.df[['open', 'high', 'low', 'close']]
        df_cs.index = pd.to_datetime(self.df['time stamp'])
        # self.displayCanvas.axes.clear()
        # self.displayCanvas.axes.plot(df_cs)
        self.displayCanvas.draw()

    # Define the custom design
    def setCustomStyle(self):
        self.setStyleSheet("QWidget{font-size: 18pt;}")

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)    
            


app = QApplication(sys.argv)
w = VisualMainWindow()
w.show()
app.exec_()


# The design can be similar to the kucoin.com