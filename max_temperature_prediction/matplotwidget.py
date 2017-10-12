from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from PyQt5 import QtWidgets
from bgfunc import dirCheck

class matplotwidget(FigureCanvas):
    def __init__(self,parent=None,width=400,height=250,dpi=80):

        self.fig=Figure(figsize=(width,height),dpi=dpi)
        FigureCanvas.__init__(self,self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.ax=self.fig.add_subplot(111)
        fontPath = "C:/Windows/Fonts/malgun.ttf"
        self.fontprop = fm.FontProperties(fname=fontPath)
        graph_path = './graph/'
        dirCheck(graph_path)



    def plotting(self,y,**kwargs):
        self.ax.plot(y,**kwargs)
    def clr(self):
        self.ax.clear()
    def labeling(self,xl,yl):
        self.ax.set_xlabel(xl,fontproperties=self.fontprop)
        self.ax.set_ylabel(yl,fontproperties=self.fontprop)

    def show(self):
        self.ax.legend(loc='best')
        self.draw()

    def savefig(self,dir):
        self.fig.savefig(dir)