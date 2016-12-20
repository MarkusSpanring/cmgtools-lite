from WMCore.Configuration import Configuration
import os
import sys
################################################################################
class DatasetChooser():
    def __init__(self, datasets_path, pref_dataset = ''):
        
        if os.path.exists(datasets_path):
            self.datasets_path = datasets_path
        else:
            raise Warning('File {0} not found!!!'.format(dataset_path))

    def timestamp(self):
        from time import localtime


        lt = localtime()
        y = str(lt.tm_year).replace('20','')
        m = str(lt.tm_mon) if lt.tm_mon>9 else '{0}{1}'.format('0',lt.tm_mon)
        d = str(lt.tm_mday) if lt.tm_mday>9 else '{0}{1}'.format('0',lt.tm_mday)

        return ''.join([y,m,d])

    def GetOpenJob(self):
        from json import load, dump
        from sys import exit

        with open(self.datasets_path ,'rb') as FSO:
            dsets=load(FSO)

        for sets in dsets.keys():
            for el in dsets[sets].keys():
                if dsets[sets][el]['step_1']['status'] == 'open':
                    self.strDatacard = dsets[sets][el]['datacard']
                    self.strTag = '{0}_{1}_{2}'.format(el, dsets[sets][el]['prod_label'], self.timestamp() )

                    self.strProdLabel = dsets[sets][el]['prod_label']
                    dsets[sets][el]['step_1']['status'] = 'done'
                    dsets[sets][el]['step_1']['time'] = self.timestamp()
                    with open(self.datasets_path ,'wb') as FSO:
                        dump(dsets, FSO,indent=4)
                    return

        raise Warning('No more jobs')

#################################################################################

cmssw_base = os.environ['CMSSW_BASE']
job = DatasetChooser('{0}/src/CMGTools/HephyTools/datasets.json'.format(cmssw_base) )
job.GetOpenJob()

tag = job.strTag
dataset = job.strDatacard
prodLabel = job.strProdLabel

print tag
print dataset
print prodLabel

# tag = "SUSYGluGluToHToTauTau_MCSpring16_pythia8_160622"
# dataset = '/SUSYGluGluToHToTauTau_M-160_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/MINIAODSIM'
# prodLabel = 'MCSpring16'

config = Configuration()
config.section_("General")
config.General.requestName = tag
config.General.workArea = 'crab_{0}'.format( prodLabel ) 
config.General.transferLogs = True

config.section_("JobType")
config.JobType.pluginName  = 'Analysis'
# Name of the CMSSW configuration file
config.JobType.psetName    = 'runMVAMET.py'
config.JobType.inputFiles = ['Spring16_25nsV6_MC.db']

config.section_("Data")
config.Data.inputDataset = dataset
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.totalUnits = -1
config.Data.publication = True
#config.Data.publication = False
# This string is used to construct the output dataset name
config.Data.outputDatasetTag = tag
#!!!
config.Data.ignoreLocality = True

# These values only make sense for processing data
#    Select input data based on a lumi mask
#config.Data.lumiMask = 'Cert_271036-276384_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt'
#    Select input data based on run-ranges
#config.Data.runRange = ''

config.section_("Site")
# Where the output files will be transmitted to
config.Site.storageSite = 'T2_AT_Vienna'
#config.Site.whitelist = ["T2_UK_SGrid_Bristol","T2_DE_DESY", "T2_US_Wisconsin"]
#config.Site.whitelist = ["T2_AT_Vienna"]
#config.Site.blacklist = ['T2_US_Purdue', 'T2_BE_IIHE', 'T2_US_Wisconsin', 'T2_UK_SGrid_Bristol', 'T2_US_Nebraska']
