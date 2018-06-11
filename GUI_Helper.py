#Robert Kowalchuk
''' THis python file contains classes and code to make PyQT widgets '''

import sys
from PyQt4 import QtCore
from PyQt4 import QtGui
import ProjectManager

#used for binding 

#maybe should take in information from another class that handles reading/creating directory stuff from json

class MainWindow(QtGui.QMainWindow):
    ''' This is the main window  '''
    def __init__(self, ProjectManager = None, *args):
        super(MainWindow, self).__init__(*args)

        self.projectManager = ProjectManager

        self.setGeometry(100, 100, 300, 700)
        self.setWindowTitle('Project Manager')
        self.show()

        self.popUpItems = ('No','Yes')

        #create layouts specific to the main window
        self.mainLayout = QtGui.QVBoxLayout()
        #this mainWidget is needed to set a new layout to the main window
        self.mainWidget = QtGui.QWidget()
        self.projectLayout = QtGui.QHBoxLayout()
        self.assetLayout = QtGui.QHBoxLayout()
        
        #Widget creation
        #self.assetSearch = SearchWidget('Asset')
        self.projectList = ListWidget('Project', self.projectManager.projectList)
        self.assetList = ListWidget('Asset', self.projectManager.assetList)
        self.projectOptions = OptionWidget('Project')
        self.assetOptions = OptionWidget('Asset')
        
        #set layouts and add widgets in order
        self.setCentralWidget(self.mainWidget)
        self.mainWidget.setLayout(self.mainLayout)
        self.mainLayout.addLayout(self.projectLayout)
        #self.mainLayout.addWidget(self.assetSearch)
        self.mainLayout.addLayout(self.assetLayout)
        self.projectLayout.addWidget(self.projectList)
        self.assetLayout.addWidget(self.assetList)
        self.projectLayout.addWidget(self.projectOptions)
        self.assetLayout.addWidget(self.assetOptions)
        
        #bind
        self.projectList.list.itemClicked.connect(self.projectListItemClicked)
        self.assetList.list.itemClicked.connect(self.assetListItemClicked)

        self.projectOptions.btnOpen.clicked.connect(self.projectOptionsLoadClicked)
        self.projectOptions.btnRename.clicked.connect(self.projectOptionsRenameClicked)
        self.projectOptions.btnDelete.clicked.connect(self.projectOptionsDeleteClicked)
        self.projectOptions.btnCreate.clicked.connect(self.projectOptionsCreateClicked)

        self.assetOptions.btnOpen.clicked.connect(self.AssetOptionsLoadClicked)
        self.assetOptions.btnRename.clicked.connect(self.AssetOptionsRenameClicked)
        self.assetOptions.btnDelete.clicked.connect(self.AssetOptionsDeleteClicked)
        self.assetOptions.btnCreate.clicked.connect(self.AssetOptionsCreateClicked)

    
        
    #project related bind methods
    def projectListItemClicked(self, item):
        #find the project that is selected and save it
        for p in self.projectManager.projectList:
            if p.name == item.text():
                self.projectManager.currentProject = p
                #update asset rules
                self.projectManager.updateAssetRules(self.projectManager.currentProject.path)

    def projectOptionsLoadClicked(self):
        self.updateAssetList()

    def projectOptionsRenameClicked(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Text Input Dialog','Enter New {} Name'.format(self.projectManager.currentProject.name))
        if ok and text:
            #rename asset with new name
            self.projectManager.renameProject(self.projectManager.currentProject.path, text)
            #redo asset list
            self.updateProjectList()

    def projectOptionsDeleteClicked(self):
        item, ok = QtGui.QInputDialog.getItem(self, 'Select Input Dialog', 'Delete {}?'.format(self.projectManager.currentProject.name), self.popUpItems, 0, False)
        if ok and item:
            if item == self.popUpItems[1]:
                #delete the project
                self.projectManager.deleteProject(self.projectManager.currentProject.path)
                #update project list
                self.updateProjectList()
                self.updateAssetList()

    def projectOptionsCreateClicked(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Text Input Dialog','Enter New Project Name')
        if ok and text:
            #make new project
            self.projectManager.createProject(str(text))
            #update project list
            self.updateProjectList()

    #asset related bind methods
    def assetListItemClicked(self, item):
        #Find the asset that is slected and save it
        for a in self.projectManager.assetList:
            if a.name == item.text():
                #open it
                self.projectManager.currentAsset = a
                print 'Name {}, Type {}, Path {}'.format(self.projectManager.currentAsset.name,self.projectManager.currentAsset.type,self.projectManager.currentAsset.path)

    def AssetOptionsLoadClicked(self):
        self.projectManager.openFile(self.projectManager.currentAsset.path)

    def AssetOptionsRenameClicked(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Text Input Dialog','Enter New {} Name'.format(self.projectManager.currentAsset.name))
        if ok and text:
            #rename asset with new name
            self.projectManager.renameAsset(self.projectManager.currentAsset.path, text)
            #redo asset list
            self.updateAssetList()

    def AssetOptionsDeleteClicked(self):
        item, ok = QtGui.QInputDialog.getItem(self, 'Select Input Dialog', 'Delete {}?'.format(self.projectManager.currentAsset.name), self.popUpItems, 0, False)
        if ok and item:
            if item == self.popUpItems[1]:
                #delete asset from system
                self.projectManager.deleteAsset(self.projectManager.currentAsset.path)
                #we need to redo asset list
                self.updateAssetList()

    def AssetOptionsCreateClicked(self):
        
        item, ok = QtGui.QInputDialog.getItem(self, 'Select Input Dialog', 'Make asset type . . .', self.projectManager.currentAssetTypes, 0, False)
        if ok and item:
            text, okok = QtGui.QInputDialog.getText(self, 'Text Input Dialog','Enter New {} Name'.format(item))
            if okok and text:
                #create asset
                self.projectManager.createAsset(str(text), str(item))
                #redo asset list
                self.updateAssetList()

    #helper methods
    def updateProjectList(self):
        #clear current projectList
        self.projectManager.projectList = []
        #update projectlist with projects
        self.projectManager.updateProjectList()
        #set projectList with those names
        self.projectList.updateList(self.projectManager.projectList)

    def updateAssetList(self):
        #clear the current assetlist
        self.projectManager.assetList = []
        #update the assetlist with that project
        if self.projectManager.currentProject != None:
            self.projectManager.updateAssetList(self.projectManager.currentProject, self.projectManager.currentProject.path)
        #set the assetList with those names 
        self.assetList.updateList(self.projectManager.assetList)

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
    def __init__(self, Name = None, Items = None, *args):
        super(ListWidget, self).__init__(Name, *args)

        self.label.setText('{} List '.format(Name))

        self.list = QtGui.QListWidget(self)
        
        self.mainLayout.addWidget(self.list)

        self.updateList(Items)

    def updateList(self, Items = None):
        #TODO : maybe make this fast because it's going to be called all day everyday
        #for now we just delete all entries and then add in the values
        self.list.clear()
        for i in Items:
            self.list.addItem(i.name)


class OptionWidget(VBoxWidget):
    ''' This is a custom widget that displays the widgets needed for options '''
    def __init__(self, Name = None, *args):
        super(OptionWidget, self).__init__(Name, *args)
        
        self.label.setText('{} Options '.format(Name))

        #we need an open asset button and delete asset button
        self.btnOpen = QtGui.QPushButton('Load {}'.format(self.name))
        self.btnRename = QtGui.QPushButton('Rename {}'.format(self.name))
        self.btnDelete = QtGui.QPushButton('Delete {}'.format(self.name))
        self.btnCreate = QtGui.QPushButton('Create {}'.format(self.name))
        self.mainLayout.addWidget(self.btnOpen)
        self.mainLayout.addWidget(self.btnRename)
        self.mainLayout.addWidget(self.btnDelete)
        self.mainLayout.addWidget(self.btnCreate)
        