#Robert Kowalchuk
''' use this to make a json file that represents the correct folder structure that was premade in the file explorer!'''
import os
import json
import pprint

def path_to_dict(path):
    d = {'name': os.path.basename(path)}
    if os.path.isdir(path):
        d['children'] = [path_to_dict(os.path.join(path,x)) for x in os.listdir(path)]
    return d

with open('D:\\directory.json', 'w') as outfile:
    json.dump(path_to_dict('D:\\Test_Project'), outfile)
outfile.close()
print 'Probably done!'

