import PhysicsTools.HeppyCore.framework.config as cfg
import os
import json




#####COMPONENT CREATOR

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

dataDir = "$CMSSW_BASE/src/CMGTools/RootTools/data"

#####################################################################################################
def getComponent(Datasets, name, readCache):
    return kreator.makeComponentHEPHY(name, Datasets[name], "PRIVATE", ".*root", "phys03",1.0, readCache= readCache)

def getDataComponent(Datasets, name, readCache, json):
    return kreator.makeDataComponentHEPHY(name, Datasets[name], "PRIVATE", ".*root", "phys03",
                                          readCache = readCache,
                                          json = json)
#####################################################################################################

user = os.environ['CMSSW_BASE']
component_path = '{0}/src/CMGTools/HephyTools/das_urls.json'.format(user)

if os.path.isfile(component_path):
        with open(component_path,'rb') as FSO:
                Datasets = json.load(FSO)
else:
    raise Warning('File {0} not found!!!'.format(component_path) )
#####################################################################################################


if __name__ == '__main__':
    for key in Datasets.keys():
        getComponent(Datasets, key,False)
else:
#####################################################################################################    
    tag  = getComponent(Datasets,"tag",False)
    
#####################################################################################################

    

