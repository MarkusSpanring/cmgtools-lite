import os
import time
import sys
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('-s', help='sample name', type=str, metavar = 'SAMPLE',default="")
parser.add_argument('-t', help='tranche name', type=str, metavar = 'TRANCH',default="")

args = vars(parser.parse_args())


sample = args['s']
tranche = args['t']

cmssw_base = os.environ['CMSSW_BASE']
path  = '{0}/src/CMGTools/HephyTools/datasets.json'.format(cmssw_base)

nJobs = 0

if os.path.isfile(path) and (sample != "" or tranche != ""):
    with open(path,'rb') as FSO:
        dsets = json.load(FSO)

    for t in dsets.keys():
        if tranche == 'show':
            print t
        for s in dsets[t].keys():
            if tranche == t:
                dsets[t][s]['step_1']['status'] = 'open'
                nJobs += 1
            elif s == sample:
                dsets[t][s]['step_1']['status'] = 'open'
                nJobs += 1
            elif sample == 'show':
                print s

    with open(path,'wb') as FSO:
        json.dump(dsets, FSO, indent =4 )

else:
    print "{0} not found or not vailid dataset input".format(path)
    sys.exit()

if tranche == 'show' or sample == 'show':
    sys.exit()

for i in xrange(nJobs):

	ret_val = os.system('crab submit -c crabConf.py')
	if ret_val != 0:
		print 'Problem with calling. Probably no more open jobs'
		sys.exit()
	time.sleep(15)

print 'Submitted %d jobs' %nJobs

