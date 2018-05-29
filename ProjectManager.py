#Robert Kowalchuk
import os       #for file management 
import shelve   #for saving configs
import json     #for making configs
import re       #for checking naming conventions
import pprint   

#hardcoded json file name and location
jsonName = 'directory.json'
jsonPath = 'D:\\{}'.format(jsonName)

#getting that json data
with open(jsonPath) as jsonFile:
    jsonData = json.load(jsonFile)
jsonFile.close()


def MakeFolders(data, path):
    ''' recursivly create directories '''
    #update the current path
    path = os.path.join(path, data['name'])
    #print it for testing
    print path
    #if the path doesn't exist then create it
    if not os.path.isdir(path):
        os.makedirs(path)

    #if we have no sub folders then start heading back
    if len(data['children']) == 0:
        return;

    #do the same with the sub folders
    for i in data['children']:
        MakeFolders(i, path)

#make some folders with a hardcoded file path
MakeFolders(jsonData, 'C:\\')

