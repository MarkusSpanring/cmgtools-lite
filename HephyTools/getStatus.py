import os
import sys
import argparse
import time
import json
from subprocess import Popen, PIPE


def colorprint(string, color):
    if color is 'red':
        if ':' in string:
            print string.split(':')[0]+ ':' + '\033[91m' + string.split(':')[1] + '\033[0m'
        else:
            print '\033[91m' + string+ '\033[0m'
    elif color is 'yellow':
        if ':' in string:
            print string.split(':')[0]+':'+ '\033[93m' + string.split(':')[1] + '\033[0m'
        else:
            print '\033[93m' + string+ '\033[0m'

    elif color is 'green':
        if ':' in string:
            print string.split(':')[0]+':'+ '\033[92m' + string.split(':')[1] + '\033[0m'
        else:
            print '\033[92m' + string+ '\033[0m'

    else: print string
def getCrabFolders(paths):

    crab_folders = []
    for path in paths:
        if os.path.exists(path):
            if os.path.isdir( path ):
                for folder in os.listdir(path):
                    if os.path.isdir( '/'.join([ path, folder ]) ) and 'crab_' in folder:

                        crab_folders.append( '/'.join([ path, folder ]) )
    return crab_folders

def readInformationFile():
    if not os.path.exists('job_information.dat'):
        open('job_information.dat','a').close()
        return []  
    else:
        with open('job_information.dat','r') as FSO:
            info_content = FSO.read().splitlines()
        return info_content

def addInformation(folders, information):
    add_folder =[]
    for folder in folders:
        exists = False
        for info in information:
            if folder in info:
                exists = True
        if not exists:
            add_folder.append( folder )

    for folder in add_folder:
        information.append( ';{0};0;0'.format(folder) )

    return information

def removeInformation(folders, information):
    for i,info in enumerate(information):
        exists = False
        for folder in folders:
            if folder in info:
                exists = True
        if not exists:
            information.pop(i)
    return information

def writeDASurl(tag,das_url):

    with open('datasets.json' ,'rb') as FSO:
        dsets=json.load(FSO)

    for sets in dsets.keys():
        for el in dsets[sets].keys():
            if el in tag:
                dsets[sets][el]['das_url'] = das_url

    with open('datasets.json' ,'wb') as FSO:
        json.dump(dsets, FSO,indent=4)



def updateInformationFile(paths, RESUB = True):
    crab_folders = getCrabFolders(paths)
    info_content = readInformationFile()
    if info_content == []:
        for folder in crab_folders:
            info_content.append( ';{0};0;0'.format(folder) )

        with open('job_information.dat','w') as FSO:
            FSO.write( '\n'.join(info_content) )

    else:
        
        info_content = addInformation(crab_folders, info_content)
        info_content = removeInformation(crab_folders, info_content)

        print '{0}\n{1}RUNNING'.format( '-'*80, ' '*25 )

        completed_jobs = []
        failed_jobs = []
        for i,info in enumerate(info_content):

            if info != '':
                splInfo = info.split(';')
                job_name = splInfo[1].split('/')[-1].replace('crab_','')
            else:
                continue

            if splInfo[0] == 'COMPLETED':
                completed_jobs.append( job_name )

            elif splInfo[0] == 'FAILED':
                failed_jobs.append( job_name )

            else:
                status, das_url = getStatus( splInfo[1] )
                if status == 'COMPLETED':
                    splInfo[0] = 'COMPLETED'
                    completed_jobs.append( job_name  )
                    if das_url != '':
                        writeDASurl(job_name, das_url)
                    info_content[i] = ';'.join(splInfo)

                elif status == 'RESUBMIT':
                    if int(splInfo[2]) > 20:
                        splInfo[0] = 'FAILED'
                        failed_jobs.append( job_name )
                        info_content[i] = ';'.join(splInfo)
                    else:
                        if RESUB:
                            resubmitJob( splInfo[1] )
                            splInfo[2] = str( int(splInfo[2]) +1 )
                            info_content[i] = ';'.join(splInfo)
                            print 'resubmitting failed jobs'

                elif status == 'PUBLICATE':
                    if int(splInfo[3]) > 20:
                        splInfo[0] = 'FAILED'
                        failed_jobs.append( job_name )
                        info_content[i] = ';'.join(splInfo)
                    else:
                        if RESUB:
                            resubmitPublication( splInfo[1] )
                            splInfo[3] = str( int(splInfo[3]) +1 )
                            info_content[i] = ';'.join(splInfo)
                            print 'publishing missing files'
   
        with open('job_information.dat','w') as FSO:
            FSO.write('\n'.join(info_content))

        print '{0}\n{1}COMPLETED\n{0}\n{2}'.format('-'*80, ' '*25, '\n'.join(completed_jobs))
        print '{0}\n{1}FAILED\n{0}\n{2}'.format('-'*80, ' '*25, '\n'.join(failed_jobs))




def resubmitJob(path):
            proc = Popen('crab resubmit {0}'.format( path ),stdout = PIPE, shell=True)
            (out, err) = proc.communicate()

def resubmitPublication(path):
            proc = Popen('crab resubmit {0} --publication'.format( path ),stdout = PIPE, shell=True)
            (out, err) = proc.communicate()

def getStatus(path):

    proc = Popen('crab status {0}'.format( path ),stdout = PIPE, shell=True)
    (out, err) = proc.communicate()
    print '{0}\n{1}'.format('-'*80, path.split('/')[-1].replace('crab_','') )
    JOBS = False
    PUBL = False
    JFAIL = False
    PFAIL = False
    JCOMP = False
    das_url = ''

    for line in out.split('\n'):
        
        if 'DAS URL' in line:
            das_url = line.replace('%2F','/').split('input=')[1].split('&instance')[0]
            
        if 'Task status' in line:
            print line
            if 'COMPLETED' in line:
                JCOMP = True
             
        if 'Jobs status:' in line:
            JOBS = True
            
        if 'Publication status:' in line:
            JOBS = False
            PUBL = True

        if line  == '':
            JOBS = False
            PUBL = False

        if JOBS:
            if 'failed' in line:
                JFAIL = True
                colorprint(line, 'red')
            elif 'finished' in line: 
                colorprint(line, 'green')
            elif 'transferring' in line:
                colorprint(line, 'yellow')
            else:
                print line

        if PUBL:
            if 'failed' in line:
                PFAIL = True
                colorprint(line, 'red')
            elif 'finished' in line: 
                colorprint(line, 'green')
                if not '100.0' in line:
                    JCOMP = False
            elif 'transferring' in line:
                colorprint(line, 'yellow')
            else:
                print line


    if JCOMP:
      return 'COMPLETED', das_url
    elif JFAIL:
      return 'RESUBMIT', das_url
    elif PFAIL:
      return 'PUBLICATE', das_url
    else:
      return '', das_url



if __name__ == '__main__':
    user = os.environ['USER']

    
    paths =['{0}/src/CMGTools/H2TauTau/prod/MC/crab_MCSpring16'.format(os.environ['CMSSW_BASE']),
            '{0}/src/CMGTools/H2TauTau/prod/MCSpring16/crab_MCSpring16_reHLT'.format(os.environ['CMSSW_BASE']),
            '{0}/src/CMGTools/H2TauTau/prod/sync/crab_MCSpring16_reHLT'.format(os.environ['CMSSW_BASE']),
            '{0}/src/CMGTools/H2TauTau/prod/sync/crab_MCSpring16_reHLT_2'.format(os.environ['CMSSW_BASE']),
            '{0}/src/CMGTools/H2TauTau/prod/sync/crab_MCSpring16'.format(os.environ['CMSSW_BASE']),                        
            '{0}/src/CMGTools/H2TauTau/prod/DATA/crab_DATA'.format(os.environ['CMSSW_BASE']),
            '{0}/src/CMGTools/TTHAnalysis/cfg/crab_HEPHY/crab_MCSpring16'.format(os.environ['CMSSW_BASE']),
            '{0}/src/CMGTools/TTHAnalysis/cfg/crab_HEPHY/crab_DATA'.format(os.environ['CMSSW_BASE']),
            '{0}/src/CMGTools/TTHAnalysis/cfg/crab_HEPHY/crab_MCSpring16_reHLT'.format(os.environ['CMSSW_BASE'])
           ]

    parser = argparse.ArgumentParser()
    parser.add_argument('--ptime',dest='ptime', help='Time between two status checks.', type=int, metavar = 'INT',default=3000)
    parser.add_argument('--nrep',dest='rep', help='Number of status checks.', type=int, metavar = 'INT',default=1)
    parser.add_argument('--res',dest='resubmit', help='Resubmit failed job?', action='store_true')

    args = parser.parse_args()
    if args.resubmit:
        print 'Resubmiting jobs every {0}sec {1} time(s).'.format(args.ptime, args.rep)
    for i in xrange(args.rep):
        updateInformationFile(paths, RESUB=args.resubmit)
        if args.rep > 1 and i != args.rep-1:
            time.sleep(args.ptime)
