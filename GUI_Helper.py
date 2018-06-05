#Robert Kowalchuk
''' THis python file contains classes and code to make PyQT widgets '''

import sys
from PyQt4 import QtCore
from PyQt4 import QtGui


#used for binding 


class MainWindow(QtGui.QMainWindow):
    ''' This is the main window  '''
    def __init__(self, *args):
        super(MainWindow, self).__init__(*args)
        self.setGeometry(100, 100, 300, 700)
        self.setWindowTitle('Project Manager')
        self.show()

        #create layouts specific to the main window
        self.mainLayout = QtGui.QVBoxLayout()
        #this mainWidget is needed to set a new layout to the main window
        self.mainWidget = QtGui.QWidget()
        self.projectLayout = QtGui.QHBoxLayout()
        self.assetLayout = QtGui.QHBoxLayout()
        
        #Widget creation
        self.assetSearch = SearchWidget('Asset')
        self.projectList = ListWidget('Project')
        self.assetList = ListWidget('Asset')
        self.projectOptions = OptionWidget('Project')
        self.assetOption = OptionWidget('Asset')
        
        #set layouts and add widgets in order
        self.setCentralWidget(self.mainWidget)
        self.mainWidget.setLayout(self.mainLayout)
        self.mainLayout.addLayout(self.projectLayout)
        self.mainLayout.addWidget(self.assetSearch)
        self.mainLayout.addLayout(self.assetLayout)
        self.projectLayout.addWidget(self.projectList)
        self.assetLayout.addWidget(self.assetList)
        self.projectLayout.addWidget(self.projectOptions)
        self.assetLayout.addWidget(self.assetOption)


        
class VBoxWidget(QtGui.QWidget):
    ''' This is a base widget that has a verticle box layout '''
    def __init__(self, Name = None, *args):
        super(VBoxWidget, self).__init__(*args)

        self.name = Name

        self.mainLayout = QtGui.QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.label = QtGui.QLabel('yes')
        self.mainLayout.addWidget(self.label)

class HBoxWidget(QtGui.QWidget):
    ''' This is a base widget that has a horizontal box layout '''
    def __init__(self, Name = None, *args):
        super(HBoxWidget, self).__init__(*args)

        self.name = Name

        self.mainLayout = QtGui.QHBoxLayout()
        self.setLayout(self.mainLayout)

class SearchWidget(VBoxWidget):
    ''' This is more of a custom widget for selecting search categories '''
    def __init__(self, Name = None, *args):
        super(SearchWidget, self).__init__(Name, *args)

        self.label.setText('Filter {} '.format(Name))

        self.searchTerm = QtGui.QComboBox()
        self.mainLayout.addWidget(self.searchTerm)

        self.updateTerms(('All','Textures','Made by X', 'Character Specific'))

    def updateTerms(self, Terms = None):
        self.searchTerm.clear
        for i in Terms:
            self.searchTerm.addItem(i)

class ListWidget(VBoxWidget):
    ''' This is a list widget with functions that aid it '''
    def __init__(self, Name = None, *args):
        super(ListWidget, self).__init__(Name, *args)

        self.label.setText('{} List '.format(Name))

        self.list = QtGui.QListWidget(self)
        
        self.mainLayout.addWidget(self.list)

        self.updateList(('Fireball','Tall Hat','Fishing Rod','Scamp'))

    def updateList(self, Items = None):
        #TODO : maybe make this fast because it's going to be called all day everyday
        #for now we just delete all entries and then add in the values
        self.list.clear()
        for i in Items:
            self.list.addItem(i)


class OptionWidget(VBoxWidget):
    ''' This is a custom widget that displays the widgets needed for options '''
    def __init__(self, Name = None, *args):
        super(OptionWidget, self).__init__(Name, *args)
        
        self.label.setText('{} Options '.format(Name))
        self.items = ('No','Yes')

        #we need an open asset button and delete asset button
        self.btnOpen = QtGui.QPushButton('Load {}'.format(self.name))
        self.btnRename = QtGui.QPushButton('Rename {}'.format(self.name))
        self.btnDelete = QtGui.QPushButton('Delete {}'.format(self.name))
        self.mainLayout.addWidget(self.btnOpen)
        self.mainLayout.addWidget(self.btnRename)
        self.mainLayout.addWidget(self.btnDelete)

        #need to bind some of these buttons
        self.bindBtns()

    def bindBtns(self):
        self.btnRename.clicked.connect(self.getRename)
        self.btnDelete.clicked.connect(self.getDelete)

    def getRename(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Text Input Dialog','Enter New {} Name'.format(self.name))
        if ok and text:
            print text

    def getDelete(self):
        item, ok = QtGui.QInputDialog.getItem(self, 'Select Input Dialog', 'Delete {}?'.format(self.name), self.items, 0, False)
        if ok and item:
            print item
        

        
        
    
app = QtGui.QApplication(sys.argv)
gui = MainWindow()
sys.exit(app.exec_())