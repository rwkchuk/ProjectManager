#Robert Kowalchuk
import os       #for file management 
import shutil
import shelve   #for saving configs
import json     #for making configs
import re       #for checking naming conventions
import pprint   

#create json from directory, create directory from json, read json for info
class Manager():
    def __init__(self, *args):

        # CHANGE ME if you don't have a D drive (just change the D to the drive you do have)
        self.masterPath = 'D:\\ProjectManager\\Projects'
        self.projectList = []
        self.assetList = []
        self.currentProject = None
        self.currentAsset = None
        self.currentAssetRules = []
        self.currentAssetTypes = []
        self.setup()
        print os.path.abspath('.')

    def setup(self):
        ''' calling everything we need for set up and what not '''
        self.checkMasterPath()
        self.updateProjectList()
        if len(self.projectList) != 0:
            #TODO : this will probably fall apart if ProjectDir is modified
            self.updateAssetRules(self.projectList[0].path)
            self.updateAssetList(self.projectList[0], self.projectList[0].path)
        

    def checkMasterPath(self):
        ''' Mainly checking if project manager folder exists and if not creates it '''
        if not os.path.exists(self.masterPath):
            os.makedirs(self.masterPath)
        else:
            print 'We good'
            
    def updateProjectList(self):
        ''' check masterPath path for projects and adds them to the list or removes them '''
        tempList = os.listdir(self.masterPath)
        for i in tempList:
            tempProject = Project(i, os.path.join(self.masterPath, i))
            self.projectList.append(tempProject)
        

    def updateAssetList(self, project = None, Path = None):
        ''' recursivly adds each file as an asset to the assetList '''
        if not os.path.isfile(Path):
            for i in os.listdir(Path):
                self.updateAssetList(project, os.path.join(Path, i))
        else:
            #this if the asset doesn't fall within the config then ass it anyways with a default None type
            if self.isAssetType(project, Path):
                for i in self.currentAssetRules:
                    if os.path.join(project.path, i['path']) == os.path.dirname(Path):
                        #we want to set the type occording to the AssetConfig before making this asset
                        self.assetList.append(Asset(os.path.basename(Path), Path, i['type']))
                        return
            else:
                self.assetList.append(Asset(os.path.basename(Path), Path))
        return

    def updateAssetRules(self, Path = None):
        ''' given a path to the current project updates the asset rules from the AssetConfig '''
        #TODO : this will break with ProjectDir is changed
        Path = os.path.join(Path,'Temp\\AssetConfig.json')
        tempData = self.getJsonData(Path)
        for i in tempData['AssetRules']:
            self.currentAssetRules.append(i)
            self.currentAssetTypes.append(i['type'])
          


    def isAssetType(self, project = None, assetPath = None):
        ''' this checks if any of the config types match the file path of the asset '''
        for i in self.currentAssetRules:
            if os.path.join(project.path, i['path']) == os.path.dirname(assetPath):
                return True
        return False

    def openFile(self, Path = None):
        ''' opens a file using this machines default application '''
        os.startfile(Path)

    def deleteProject(self, Path = None):
        ''' removes project from system '''
        shutil.rmtree(Path)
        print '{} deleted'.format(Path)
        self.currentProject = None

    def deleteAsset(self, Path = None):
        ''' remove asset from the system '''
        if os.path.isfile(Path):
            os.remove(Path)
            print '{} deleted'.format(Path)
            self.currentAsset = None
            
    def renameProject(self, OldPath = None, NewName = None):
        ''' renames the project '''
        if os.path.isdir(OldPath):
            NewPath = os.path.join(os.path.dirname(OldPath), str(NewName))
            os.rename(OldPath, NewPath)
            print NewPath

    def renameAsset(self, OldPath = None, NewName = None):
        ''' renames the asset '''
        if os.path.isfile(OldPath):
            #TODO : this was made before Assets had a type so this code might be doable without splits?
            OldName = os.path.basename(OldPath)
            NewName = NewName +'.' + OldName.split('.')[1]
            print NewName
            NewPath = os.path.join(os.path.dirname(OldPath), str(NewName))
            os.rename(OldPath, NewPath)
            print NewPath
            
    def createProject(self, Name = None):
        ''' creates a project within the master file path and sets it with a default directory structure '''
        #this will just be taking a name and making a dir for it under master
        #if not os.path.exists(os.path.join(self.masterPath, Name)):
        #    os.makedirs(os.path.join(self.masterPath, Name))
        jsonData = self.getJsonData(os.path.join('.','ProjectDir.json'))
        self.makeFolders(jsonData, self.masterPath)
        self.renameProject(os.path.join(self.masterPath,'EMPTYProject'), Name)
        
    def createAsset(self, Name = None, Type = None):
        ''' create an asset onto the system '''
        Path = None
        for i in self.currentAssetRules:
            #we want to find what type of asset we are making
            if i['type'] == Type:
                #making the basename for the asset
                Name = Name + i['extension']
                print Name
                #making the full path for the asset
                Path = os.path.join(os.path.join(self.currentProject.path, i['path']), Name)
                #creating the asset
                with open(Path, 'w') as outfile:
                    outfile.close()
                return

    def getJsonData(self, Path = None):
        ''' used to read and return json data '''
        data = None
        with open(Path) as file:
            data = json.load(file)
        file.close()
        return data

    def setJsonData(self, FilePath = None, DataDump = None):
        ''' used to push data to a json file '''
        with open(FilePath, 'w') as outfile:
            json.dump(DataDump, outfile)
        outfile.close()

    def makeFolders(self, Data = None, Path = None):
        ''' recursivly create directories '''
        #update the current path
        Path = os.path.join(Path, Data['name'])
        #print it for testing
        print Path
        #if the path doesn't exist then create it
        #TODO : make this more dynamic since we might not always be dealing with json
        if Data['type'] == 'Asset':
            self.setJsonData(Path, self.getJsonData(os.path.join('.','AssetConfig.json')))
        else:
            if not os.path.isdir(Path):
                os.makedirs(Path)

        #if we have no sub folders then start heading back
        if len(Data['children']) == 0:
            return;

        #do the same with the sub folders
        for i in Data['children']:
            self.makeFolders(i, Path)





    def pathToDirectory(self, Path = None):
        ''' Used to create a dictionary of containers from the paths/file directories provided that can then be dumped into a json file '''
        d = {'name': os.path.basename(Path)}
        if os.path.isfile(Path):
            d['Type'] = 'Asset'
            d['children'] = []
        else:
            d['Type'] = 'Folder'
            d['children'] = [self.pathToDirectory(os.path.join(Path,x)) for x in os.listdir(Path)]
        return d





class Info(object):
    ''' base class that holds a name and path '''
    def __init__(self, Name = None, Path = None, *args):
        self.name = Name
        self.path = Path

    def update(self):
        temp = 0
    
class Project(Info):
    ''' Holds info for a project '''
    def __init__(self, Name = None, Path = None, *args):
        super(Project, self).__init__(Name, Path, *args)
        
    def update(self):
        super(Project, self).update()
        print 0

class Asset(Info):
    ''' Holds info for an asset '''
    def __init__(self, Name = None, Path = None, Type = 'None', *args):
        super(Asset, self).__init__(Name, Path, *args)
        #TODO : think of a dynamic way to get asset type from config into creation of assets
        self.type = Type



