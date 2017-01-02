#! /usr/bin/env pythonOB
import imp, os, sys
import json
from optparse import OptionParser

# datasets to run as defined from run_susyMT2.cfg
# number of jobs to run per dataset decided based on splitFactor and fineSplitFactor from cfg file
# in principle one only needs to modify the following two lines:



#####################################################################################################
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

def timestamp():
    from time import localtime


    lt = localtime()
    y = str(lt.tm_year).replace('20','')
    m = str(lt.tm_mon) if lt.tm_mon>9 else '{0}{1}'.format('0',lt.tm_mon)
    d = str(lt.tm_mday) if lt.tm_mday>9 else '{0}{1}'.format('0',lt.tm_mday)

    return ''.join([y,m,d])

def showSamples():
    cmssw_base = os.environ['CMSSW_BASE']
    with open('{0}/src/CMGTools/HephyTools/datasets.json'.format(cmssw_base) ,'rb') as FSO:
        dsets=json.load(FSO)
    
    for tranche in dsets.keys():
        for sample in dsets[tranche].keys():
            if dsets[tranche][sample]['das_url'] != '':
                print sample


def getDataset(input_tag):
    cmssw_base = os.environ['CMSSW_BASE']
    with open('{0}/src/CMGTools/HephyTools/datasets.json'.format(cmssw_base) ,'rb') as FSO:
        dsets=json.load(FSO)

    Datasets = {}
    for sets in dsets.keys():
        for el in dsets[sets].keys():
            

            if dsets[sets][el]['das_url'] != '':
                if el == input_tag:
                 
                    Datasets[el] ={'url': dsets[sets][el]['das_url']}
                    Datasets[el]['prod_label'] = dsets[sets][el]['prod_label']


    if Datasets == {}: 
        print 'No url availabe for {0}'.format(input_tag) 
        sys.exit()


    return Datasets

def getComponent(Datasets, name, readCache):
    return kreator.makeComponentHEPHY('{0}_{1}_{2}'.format(name, Datasets[name]['prod_label'], timestamp()), Datasets[name]['url'], "PRIVATE", ".*root", "phys03",1.0, readCache= readCache)

def getDataComponent(Datasets, name, readCache):
    dataDir = "$CMSSW_BASE/src/CMGTools/RootTools/data/"
    json = dataDir + 'Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.txt'

    return kreator.makeDataComponentHEPHY('{0}_{1}_{2}'.format(name, Datasets[name]['prod_label'], timestamp()), Datasets[name]['url'], "PRIVATE", ".*root", "phys03",
                                          readCache = readCache,
                                          json = json)
#####################################################################################################




parser = OptionParser(usage="python launch.py --sample SAMPLE]",
                      description="Launch heppy jobs with CRAB3. Components correspond to the variables defined in heppy_samples.py (their name attributes)")
parser.add_option("--sample", dest="tag", help="Tag of sample")
parser.add_option("--cmg_version", dest="cmg_version", help="CMG version", default="CMGTools-from-CMSSW_8_0_20")
parser.add_option("--unitsPerJob", dest="unitsPerJob", help="Nr. of units (files) / crab job", type="int", default=1)
parser.add_option("--totalUnits", dest="totalUnits", help="Total nr. of units (files)", type="int", default=None)
parser.add_option("--inputDBS", dest="inputDBS", help="dbs instance", default="phys03")
parser.add_option("--lumiMask", dest="lumiMask", help="lumi mask (for data)", default=None)
parser.add_option("--show", dest="show", help="Show availabele samples", action = 'store_true')
( options, args ) = parser.parse_args()

if options.show:
    showSamples()
    sys.exit()

Datasets = getDataset(options.tag)

if Datasets[options.tag]['prod_label'] == 'DATA':

    selectedComponents = [getDataComponent(Datasets,options.tag, False)]
else:
    selectedComponents = [getComponent(Datasets,options.tag, False)]

os.system("scram runtime -sh")
os.system("source /cvmfs/cms.cern.ch/crab3/crab.sh")

os.environ["CMG_PROD_LABEL"]  = Datasets[options.tag]['prod_label']
os.environ["CMG_REMOTE_DIR"]  = '{0}_{1}_{2}'.format(options.tag, Datasets[options.tag]['prod_label'] ,timestamp())
os.environ["CMG_VERSION"] = options.cmg_version
os.environ["CMG_UNITS_PER_JOB"] = str(options.unitsPerJob)
os.environ["CMG_LUMI_MASK"] = options.lumiMask if options.lumiMask else "None"
if options.totalUnits:
    os.environ["CMG_TOTAL_UNITS"] = str(options.totalUnits)
else:
    if "CMG_TOTAL_UNITS" in os.environ:
        del os.environ["CMG_TOTAL_UNITS"]
if options.inputDBS:
    os.environ["INPUT_DBS"] = options.inputDBS

    
#from PhysicsTools.HeppyCore.framework.heppy import split
import pickle
for comp in selectedComponents:
#    print "generating sample_"+comp.name+".pkl"
    print "Processing ",comp.name
    workArea = 'crab_{0}'.format( Datasets[options.tag]['prod_label'] )
    if not os.path.exists( workArea ):
        os.mkdir(workArea)
    
    fout = open("{0}/sample_{1}.pkl".format(workArea, comp.name),"wb")
    pickle.dump(comp,fout)
    fout.close()
    #    os.environ["DATASET"] = str(comp.name)
    os.environ["CMG_DATASET"] = comp.dataset
    #os.environ["CMG_DATASET"] = "/SingleMuon/jbrandst-SingleMuon_160320-49dd414a1ce672fee88ca4308f209634/USER"
    #os.environ["CMG_DATASET"]  = "/SingleElectron/jbrandst-SingleElectron_160320-49dd414a1ce672fee88ca4308f209634/USER"
    os.environ["CMG_COMPONENT_NAME"] = comp.name
    #    os.system("python tmp.py > tmp.lis")
    os.system("source /cvmfs/cms.cern.ch/crab3/crab.sh")
    os.system("which crab")
    os.system("crab submit -c heppy_crab_config_env.py --wait")


os.system("rm -f python.tar.gz")
os.system("rm -f cmgdataset.tar.gz")
os.system("rm -f cafpython.tar.gz")
