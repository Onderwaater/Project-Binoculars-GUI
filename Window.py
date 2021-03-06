import sys, csv, os
import itertools
import inspect
import glob
import BINoculars
from PyQt4.QtGui import *
from PyQt4.QtCore import *

#--------------------------------------------CREATE MAIN WINDOW----------------------------------------
class SimpleGUI(QMainWindow):

    def __init__(self):
        super(SimpleGUI, self).__init__()
        self.initUI()
        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)


    def initUI(self):
        openFile = QAction('Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.ShowFile)

        saveFile = QAction('Save', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.setStatusTip('Save File')
        saveFile.triggered.connect(self.Save)

        Create = QAction('Create', self)
        Create.setStatusTip('Create new configuration')
        Create.triggered.connect(self.New_Config)
         
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(saveFile)
        fileMenu = menubar.addMenu('&New Configuration')
        fileMenu.addAction(Create)
        fileMenu = menubar.addMenu('&RUN')

        palette = QPalette()
        palette.setColor(QPalette.Background,Qt.gray)
        self.setPalette(palette)
        self.setGeometry(250, 200,700,700)
        self.setWindowTitle('Binoculars')
        self.setWindowIcon(QIcon('binoculars.png'))
        self.show()

    def ShowFile(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '')
        self.tab_widget.addTab(Conf_Tab(self),filename)
        widget = self.tab_widget.currentWidget()
        widget.read_data(filename)
           
        
       # d = widget.read_data(filename)
        # for k in d.keys():
           # print "%s:" % k 
           # for i in d[k]:
               # print "    %s" % str(i)    
                    
 


    def Save(self):
        filename = QFileDialog().getSaveFileName(self, 'Enregistrer', '', '*.txt')
        widget = self.tab_widget.currentWidget() 
        widget.save(filename) 
        
    def New_Config(self):
        self.tab_widget.addTab(Conf_Tab(self),'New configuration')

#----------------------------------------------------------------------------------------------------
#-----------------------------------------CREATE TABLE-----------------------------------------------
class Table(QWidget):
    def __init__(self, choice = [], parent = None):
        super(Table, self).__init__()
        
        # create a QTableWidget
        self.table = QTableWidget(1, 3, self)
        self.table.setHorizontalHeaderLabels(['Parameter', 'Value','Comment'])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        
        #create combobox
        self.combobox = QComboBox()
        self.combobox.addItems(QStringList(choice))
         
        #add items
        cell = QTableWidgetItem(QString("Types"))
        cell2 = QTableWidgetItem(QString(""))
        self.table.setItem(0, 0, cell)
        self.table.setCellWidget(0, 1, self.combobox)
        self.table.setItem(0, 2,cell2)

        self.btn_add_row = QPushButton('+', self)
        self.connect(self.btn_add_row, SIGNAL('clicked()'), self.add_row)
        
        layout =QGridLayout()
        layout.addWidget(self.table,0,0,3,10)
        layout.addWidget(self.btn_add_row,0,11)
        self.setLayout(layout)

    def add_row(self):
        self.table.insertRow(self.table.rowCount())


    def getParam(self):
        for index in range(self.table.rowCount()):
            key = self.table.item(index,0).text() 
            comment = self.table.item(index, 2).text()
            if self.table.item(index,1):
                value = self.table.item(index, 1).text()
            else:
                value = self.table.cellWidget(index, 1).currentText()
            if self.table.item == None:
                value = self.table.item(index,1).text("")
            yield key, value, comment
        
    def addData(self, data):
        for item in data:
            if item[0] == 'Types':
                    box = self.table.cellWidget(0,1)
                    box.addItems(QStringList(item[1]))
                    box.setCurrentIndex(box.findText(item[1]))
                    

            else:
                self.add_row()
                row = self.table.rowCount()
                for col in range(self.table.columnCount()):
                    newitem = QTableWidgetItem(item[col])
                    self.table.setItem(row -1, col, newitem)

    

class Dispatcher(Table):
    def __init__(self, parent = None):
        choice = ['Local','OAR']
        super(Dispatcher, self).__init__(choice)
        
        

class Input(Table):
    def __init__(self, parent = None):
        choice = ['test', 'test1']
        super(Input, self).__init__(choice)
        

class Projection(Table):
    def __init__(self, parent = None):
        choice = ['test', 'test1']
        super(Projection, self).__init__(choice)
        

#----------------------------------------------------------------------------------------------------
#-----------------------------------------CREATE CONFIG----------------------------------------------
class Conf_Tab(QWidget):
    def __init__(self, parent = None):

        super(Conf_Tab,self).__init__()
        self.Dis = Dispatcher()
        self.Inp = Input()
        self.Pro = Projection()

        label1 = QLabel('<strong>Dispatcher</strong>')
        label2 = QLabel('<strong>Input</strong>')
        label3 = QLabel('<strong>Projection<strong>')

        self.select = QComboBox()
        self.select.addItems(QStringList(['id03', 'id03_xu', 'bm25']))
        self.run = QPushButton('run')
        self.scan = QLineEdit()
        self.run.setStyleSheet("background-color: darkred")

        Layout = QGridLayout()
        Layout.addWidget(self.select,0,1)
        Layout.addWidget(label1,1,1)
        Layout.addWidget(self.Dis,2,1)
        Layout.addWidget(label2,3,1)
        Layout.addWidget(self.Inp,4,1)
        Layout.addWidget(label3,5,1)
        Layout.addWidget(self.Pro,6,1)
        Layout.addWidget(self.run,7,0)
        Layout.addWidget(self.scan,7,1)
        self.setLayout(Layout)


        path = './BINoculars/backends/'
        allfiles = glob.glob(os.path.join(path, '*.py'))
        backends = dict()

        for file in allfiles:
            try:
                name = os.path.splitext(os.path.basename(file))[0]
                backends[name] = __import__('BINoculars.backends.{0}'.format(name), globals(), locals(), [], -1)
            except ImportError as e:
                print 'Import backend error: {0} with error message {1}'.format(name, e.message)
        print inspect.getmembers(backends['id03'])
        

    def save(self, filename):
        with open(filename, 'w') as fp:
            fp.write('[dispatcher]\n')
            for key, value, comment in self.Dis.getParam():# cycles over the iterator object
                fp.write('{0} = {1} #{2}\n'.format(key, value, comment))
            fp.write('[input]\n')
            for key, value, comment in self.Inp.getParam():
                fp.write('{0} = {1} #{2}\n'.format(key, value, comment))
            fp.write('[projection]\n')
            for key, value, comment in self.Pro.getParam():
                fp.write('{0} = {1} #{2}\n'.format(key, value, comment))
           

    def read_data(self,filename):
        with open(filename, 'r') as inf:
            lines = inf.readlines()
 
        data = {'dispatcher': [], 'input': [], 'projection': []}
        for line in lines:
            if 'dispatcher' in line:
                key = 'dispatcher'
            elif 'input' in line:
                key = 'input'
            elif 'projection' in line: 
                key = 'projection'
            else:
                try:
                    caput, cauda = line.split('#')
                except ValueError:
                # no '#' in line
                    continue
                try:
                    name, value = caput.split('=')
                except ValueError:
                # wrong line
                    continue
                data[key].append([name.strip(' '), value.strip(' '), cauda.strip(' ')])
         
        for key in data:
            if key == 'dispatcher':
                self.Dis.addData(data[key])
            elif key == 'input':
                self.Inp.addData(data[key])
            elif key == 'projection':
                self.Pro.addData(data[key])

                
       
    def get_backend(ID03Input):
        args = inspect.getargspec(ID03Input)
        varnames = args.args
        defaults_values = args.defaults
        if defaults_values != None:
            optionnals_args = dict(izip(varnames[-len(defaults_values):], defaults_values))
            varnames = varnames[:len(defaults_values)+1]
        else:
            optionnals_args = {}
        return(varnames, optionnals_args, args.varargs)   
        
    
    #def get_Projection(function):
        #args = inspect.getargspec(function)
        #varnames = args.args
        #defaults_values = args.defaults
        #if defaults_values != None:
           #optionnals_args = dict(izip(varnames[-len(defaults_values):], defaults_values))
            #varnames = varnames[:len(defaults_values)+1]
        #else:
            #optionnals_args = {}
        #return(varnames, optionnals_args, args.varargs)   
        







