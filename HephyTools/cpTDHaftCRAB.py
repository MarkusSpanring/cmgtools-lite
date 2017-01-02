from __future__ import print_function
import subprocess as sp
import shutil
import multiprocessing as mp
import numpy as np
import shlex
import argparse
import time
import os
import sys



#Copy, Merge and Count Handler
class CMCHandler():
    def __init__(self, source, dest):
        self.source = source
        self.dest = dest
        if os.path.exists('copy.log'):
            os.remove('copy.log')
        self.getTrees()

    def getTrees(self):
        
        sub_folders = []
        for i in xrange(6):
            proc = sp.Popen(["dpns-ls {0}".format(self.source)], stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
            (out, err) = proc.communicate()
            strout = out.split('\n')
            strout.remove('')

            if '0000' in strout:
                sub_folders = strout
                break

            if len(strout) > 1:
                for ind, fldr in enumerate(strout): 
                    if ind == 0:
                        latest = ind
                    else:
                        if int( strout[ind].replace('_','') ) > int( strout[latest].replace('_','') ):
                            latest = ind
                strout = [ strout[latest] ]

            self.source += '/{0}'.format( strout[0] )

        files = {}
        for folder in sub_folders:
            path = "{0}/{1}".format( self.source, folder )
            proc = sp.Popen(['dpns-ls {0}'.format( path ) ], stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
            (out, err) = proc.communicate()
            files[folder] ={}
            files[folder]['path'] = path
            files[folder]['files'] = out.split('\n')[:-1]

        
        self.files = files

    def validateCopy(self):
        src_files = []
        dest_files = []

        for fldr in self.files.keys():
            for f in self.files[fldr]['files']:
                nfile = ''.join([s for s in f if s.isdigit()])
                if nfile == '': nfile = '0'
                if 'tree' in f:
                    src_files.append( int(nfile,0) )


        for f in os.listdir( self.dest ):
            nfile = ''.join([s for s in f if s.isdigit()])
            if nfile == '': nfile = '0'
            if 'tree_unmerged' in f:
                dest_files.append( int(nfile,0) )

        src_files.sort()
        dest_files.sort()

        for i in dest_files:
            src_files.pop( src_files.index(i) )

        return src_files




    def copyFiles(self,ftype, sub = 'all',ignore = False , recreate = False, max_proc = 4):

        if os.path.exists(self.dest) and recreate:
            print( '{0} will be created anew'.format(self.dest) )
            shutil.rmtree( self.dest )
            os.mkdir( self.dest )
        elif os.path.exists(self.dest) and not ignore:
            print( '{0} already exists'.format(self.dest) )
            sys.exit()
        elif not os.path.exists(self.dest):
            os.mkdir( self.dest )
        elif ftype != 'tree' and ftype != 'Skim' and ftype != 'RLTInfo':
            print( 'Use \'Skim\' or \'tree_\' as ftype!!!' )
            sys.exit()

        
        trees = self.files
        cp_cmd = 'lcg-cp -v srm://hephyse.oeaw.ac.at'
        cmd_list = []
        for folder in trees:
            path = trees[folder]['path']

            if sub == 'all' or sub == folder:
                for file in trees[folder]['files']:
                    if ftype in file:
                        cmd_list.append('{0}/{1}/{2} {3}/{4}'.format(
                                            cp_cmd,
                                            path,
                                            file,
                                            self.dest,
                                            file.replace('tree_','tree_unmerged_')
                                            )
                                        )

        print( 'Start copying {0} files'.format(ftype) )
        self.applyCmdMulti( cmd_list,  max_proc=max_proc)
        print( '\nFinished' )

    def getSkimCount(self):
        strSrch = 'Sum Unity Weights'
        events = 0
        for file in os.listdir(self.dest):
            if 'Skim' in file:

                with open('{0}/{1}'.format(self.dest, file) ,'r') as FSO:
                    strLines = FSO.readlines()
                for strLine in strLines:
                    if strSrch in strLine:
                        strLine = strLine.split('\t')
                        if strSrch in strLine[1]:
                            events += float(strLine[1].replace( strSrch, '' ))

        with open( '{0}/NEvents.txt'.format(self.dest), 'w' ) as FSO:
            FSO.write('Total Number of events: {0}'.format( events ))

        print( 'Created NEvents.txt' )
        return events



    def mergeTrees(self):
        unmerged = []
        for file in os.listdir(self.dest):
            if 'unmerged' in file:
                nfile = int(''.join([s for s in file if s.isdigit()]))
                unmerged.append( [file, nfile ] ) 

        unmerged = np.array(unmerged)
        unmerged = unmerged[ np.array(unmerged[:,1],dtype='int').argsort() ]

        off = 1
        if len(unmerged) < int(unmerged[-1,1]):
            index = len(unmerged)
        else:
            index = int(unmerged[-1,1])

        cmd_list =[]
        strCmd = ''

        mtree = 1
        for i in xrange( index ):
            
            if unmerged[i,1] != str(i+off):
                while unmerged[i,1] != str(i+off):
                    off+=1

            strCmd += ' {0}/{1}'.format(self.dest, unmerged[i,0] )

            if str(i+off)[-1] == '9':

                cmd_list.append('hadd {0}/tree_merged_{1}.root {2}'.format(self.dest, mtree, strCmd ) )
                mtree += 1
                strCmd = ''

            elif i == index-1:
                cmd_list.append('hadd {0}/tree_merged_{1}.root {2}'.format(self.dest, mtree, strCmd ) )

        print( 'Start merging files' )
        self.applyCmdMulti( cmd_list, max_proc=4 )



    def exec_cmd(self,cmd, q):
        shlCmd = shlex.split(cmd)
            
        log = open('copy.log', 'a')
        p = sp.Popen(shlCmd,stdout = log, stderr = log, shell=False)

        p.wait()
        q.put(object)


    def applyCmdMulti(self,cmd_list, max_proc=4):
        count = 0
        done_queue = mp.Queue()
        nCmd = 50./float( len(cmd_list) )
        for i, cmd in enumerate(cmd_list):
            if i > max_proc:
                done_queue.get(block=True)
            proc = mp.Process(target=self.exec_cmd, args=(cmd, done_queue))
            proc.start()
            if i == len(cmd_list)-1:
                proc.join()

            count += nCmd
            print('\r[{0}>{1}]  ( {2}/{3} )'.format('='*int(count),' '*(50-int(count) ), i+1, len(cmd_list) ), end='')

    def cleanup(self, rtype = 'mc'):
        
        skimfiles = []
        tree_files = []
        rltfiles = []
        for file in os.listdir(self.dest):
            if 'unmerged' in file:
                tree_files.append(file)
            if 'Skim' in file:
                skimfiles.append(file)
            if 'RLTInfo' in file:
                rltfiles.append(file)


        print('\nRemoving unneeded Files')
        ntree = 50./ float( len(tree_files) )

        count = 0.

        for file in tree_files:
            count += ntree

            print('\r[{0}>{1}]'.format('='*int(count),' '*(50-int(count) )), end='')    
            os.remove('/'.join( [self.dest,file] ) )
        print('   Finished. ')
        
        if rtype == 'mc':

            if not os.path.exists( '/'.join([self.dest,'Skimreport']) ):
                os.mkdir( '/'.join([self.dest,'Skimreport']) )

            print('\nMoving Skimfiles')
            count = 0.
            for file in skimfiles:
                count += ntree
                print('\r[{0}>{1}]'.format('='*int(count),' '*(50-int(count) )), end='')
                shutil.move( '/'.join([self.dest,file]), '/'.join([self.dest,'Skimreport',file]))
            print('   Finished')

        if rtype == 'data':

            if not os.path.exists( '/'.join([self.dest,'RLTInfo']) ):
                os.mkdir( '/'.join([self.dest,'RLTInfo']) )

            print('\nMoving RLTInfo files')
            count = 0.
            for file in rltfiles:
                count += ntree
                print('\r[{0}>{1}]'.format('='*int(count),' '*(50-int(count) )), end='')
                shutil.move( '/'.join([self.dest,file]), '/'.join([self.dest,'RLTInfo',file]))
            print('   Finished')





if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--sample', dest = 'sample', help='Tag of dataset to copy', type=str, metavar = 'TAG', required = True)
    parser.add_argument('--user', dest='user', help='dpns-Username who createt dataset', type=str, metavar = 'dpns-USERNAME', required = True)
    parser.add_argument('-f', dest='force', help='Force overwrite', action='store_true')
    parser.add_argument('-m', dest='merge', help='Merge only', action='store_true')
    parser.add_argument('-t', dest='type', help='', type=str, metavar = 'RUNTYPE',choices = ['mc','data'], default = 'mc')

    args = parser.parse_args()

    source = '/dpm/oeaw.ac.at/home/cms/store/user/{0}/cmgTuples/{1}'.format( args.user, args.sample )
    dest = '/data/higgs/data_2016/cmgTuples/{0}'.format( args.sample )

    ch = CMCHandler(source, dest)
    if not merge:
        ch.copyFiles(ftype = 'tree',
                     recreate = args.force)

    miss = ch.validateCopy()
    if miss != []:
        print( 'There are files missing: {0}'.format( miss ) )
        sys.exit()

    if rtype == 'mc':
        ch.copyFiles(ftype = 'Skim',
                     ignore = True,
                     max_proc=8)
   
    

        ch.getSkimCount()

    elif rtype == 'data':
        ch.copyFiles(ftype = 'RLTInfo',
                     ignore = True,
                     max_proc=8)
    
    ch.mergeTrees()   
    ch.cleanup(rtype = args.type)




