import PhysicsTools.HeppyCore.framework.config as cfg
import os
import json




#####COMPONENT CREATOR

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

dataDir = "$CMSSW_BASE/src/CMGTools/RootTools/data/"

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
    json_path = dataDir + 'Cert_271036-276811_13TeV_PromptReco_Collisions16_JSON.txt'
    VBF  = getComponent(Datasets,"VBF",False)
#    SingleMuonRun2016B_PromptReco_v2MINIAOD_DATA_160921 = getDataComponent(Datasets, 'SingleMuonRun2016B_PromptReco_v2MINIAOD_DATA_160921',False,json_path)
#    SingleMuonRun2016C_PromptReco_v2MINIAOD_DATA_160926 = getDataComponent(Datasets, 'SingleMuonRun2016C_PromptReco_v2MINIAOD_DATA_160926',False,json_path)
#    SingleMuonRun2016D_PromptReco_v2MINIAOD_DATA_160926 = getDataComponent(Datasets, 'SingleMuonRun2016D_PromptReco_v2MINIAOD_DATA_160926',False,json_path)
#    SingleElectronRun2016B_PromptReco_v2MINIAOD_DATA_160926  = getDataComponent(Datasets, 'SingleElectronRun2016B_PromptReco_v2MINIAOD_DATA_160926',False,json_path)
#    SingleElectronRun2016C_PromptReco_v2MINIAOD_DATA_160926  = getDataComponent(Datasets, 'SingleElectronRun2016C_PromptReco_v2MINIAOD_DATA_160926',False,json_path)
#    SingleElectronRun2016D_PromptReco_v2MINIAOD_DATA_160926  = getDataComponent(Datasets, 'SingleElectronRun2016D_PromptReco_v2MINIAOD_DATA_160926',False,json_path)
#TauRun2016B_PromptReco_v2MINIAOD_DATA_161005  = getDataComponent(Datasets, 'TauRun2016B_PromptReco_v2MINIAOD_DATA_161005',False,json_path) 
#TauRun2016C_PromptReco_v2MINIAOD_DATA_161005  = getDataComponent(Datasets, 'TauRun2016C_PromptReco_v2MINIAOD_DATA_161005',False,json_path)
#TauRun2016D_PromptReco_v2MINIAOD_DATA_161005  = getDataComponent(Datasets, 'TauRun2016D_PromptReco_v2MINIAOD_DATA_161005',False,json_path)
    #tag  = getComponent(Datasets,"tag",False)
    
#####################################################################################################

