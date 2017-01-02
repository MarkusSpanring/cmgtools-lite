import os
import time
import sys
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('--sample',dest='sample', help='sample name', type=str, metavar = 'SAMPLE',default="")
parser.add_argument('--tranche',dest='tranche', help='tranche name', type=str, metavar = 'TRANCH',default="")
parser.add_argument('--show', dest='show', help='Show available samples', action='store_true')

args = parser.parse_args()



cmssw_base = os.environ['CMSSW_BASE']
path  = '{0}/src/CMGTools/HephyTools/datasets.json'.format(cmssw_base)

nJobs = 0

if os.path.isfile(path):
    with open(path,'rb') as FSO:
        dsets = json.load(FSO)

    for t in dsets.keys():
        if args.show:
            print 'Tranche: {0}'.format(t)
        for s in dsets[t].keys():
            if args.show:
                print '\t {0}'.format(s)
            if args.tranche == t:
                dsets[t][s]['step_1']['status'] = 'open'
                dsets[t][s]['das_url'] = ''
                nJobs += 1
            elif args.sample == s:
                dsets[t][s]['step_1']['status'] = 'open'
                dsets[t][s]['das_url'] = ''
                nJobs += 1

    with open(path,'wb') as FSO:
        json.dump(dsets, FSO, indent =4 )

else:
    print "{0} not found or not vailid dataset input".format(path)
    sys.exit()

if args.show:
    sys.exit()

for i in xrange(nJobs):

	ret_val = os.system('crab submit -c crabConf.py')
	if ret_val != 0:
		print 'Problem with calling. Probably no more open jobs'
		sys.exit()
	time.sleep(15)

print 'Submitted %d jobs' %nJobs

