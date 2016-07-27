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
        src_files = {'tree':[], 'Skim':[]}
        dest_files = {'tree':[], 'Skim':[]}
        miss_files = {'tree':[], 'Skim':[], 'merg':[]}
        for fldr in self.files.keys():
            for f in self.files[fldr]['files']:
                if 'tree' in f or 'Skim' in f: 
                    nfile = int(''.join([s for s in f if s.isdigit()]))
                    if 'tree' in f:
                        src_files['tree'].append(nfile)
                    elif 'Skim' in f:
                        src_files['Skim'].append(nfile)


        if self.getFiledDiff(src_files['tree'], src_files['Skim'], 'treefiles', 'Skimfiles'):
            return False

        for f in os.listdir( self.dest ):
            nfile = int(''.join([s for s in f if s.isdigit()]))
            if 'tree' in f:
                dest_files['tree'].append(nfile)
            elif 'Skim' in f:
                dest_files['Skim'].append(nfile)

        if self.getFiledDiff(dest_files['tree'], dest_files['Skim'], 'treefiles', 'Skimfiles'):
            return False

        if self.getFiledDiff(src_files['tree'], dest_files['tree'], 'source files', 'dest files'):
            return False

        return True


    def getFiledDiff(self, files_1, files_2, strF1 = 'files_1', strF2 = 'files_2'):
        if sorted(files_1) == sorted(files_2):
            return False
        else:

            if len(files_1) >= len(files_2):
                print('Missing {0}:'.format(strF2 ))
                print(list(set(files_1) - set(files_2)))
            else:
                print('Missing {0}:'.format(strF1) )
                print(list(set(files_2) - set(files_1)))

            return True      



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
        elif ftype != 'tree' and ftype != 'Skim':
            print( 'Use \'Skim\' or \'tree_\' as ftype!!!' )
            sys.exit()

        
        trees = self.files
        cp_cmd = 'lcg-cp srm://hephyse.oeaw.ac.at'
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

        # if ftype == 'tree':
        print( 'Start copying {0} files'.format(ftype) )
        self.applyCmdMulti( cmd_list,  max_proc=max_proc)
        print( '\nFinished' )
        # elif ftype == 'Skim':
        #     self.ApplyCmd( cmd_list )



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
        p = sp.Popen(shlCmd, shell=False)
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
            if 'lcg-cp' in cmd: print('\r[{0}>{1}]  {2}'.format('='*int(count),' '*(50-int(count) ), i+1), end='')
            #if (i+1) % 75 == 0:
            #    print('')
            #    count = 0
                

    def cleanup(self):
        
        skimfiles = []
        tree_files = []
        for file in os.listdir(self.dest):
            if 'unmerged' in file:
                tree_files.append(file)
            if 'Skim' in file:
                skimfiles.append(file)

        if not os.path.exists( '/'.join([self.dest,'Skimreport']) ):
            os.mkdir( '/'.join([self.dest,'Skimreport']) )

        print('Removing unneeded Files')
        ntree = 100./ float( len(tree_files) )
        nskim = 100./ float( len(skimfiles) )
        tmp = 0.
        for file in tree_files:
            tmp += ntree
            if tmp > 1.0:
                print('*', end='')
                tmp = 0.
            os.remove('/'.join( [self.dest,file] ) )
        print('   Finished')

        print('\nMoving Skimfiles')
        tmp = 0.
        for file in skimfiles:
            tmp += nskim
            if tmp > 1.0:
                print('*', end='')
                tmp=0.
            shutil.move( '/'.join([self.dest,file]), '/'.join([self.dest,'Skimreport',file]))
        print('   Finished')





if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', help='Tag of dataset to copy', type=str, metavar = 'TAG', required = True)
    parser.add_argument('-f', help='Force overwrite', action='store_true')

    args = vars(parser.parse_args())

    Dset = args['d']

    source = '/dpm/oeaw.ac.at/home/cms/store/user/mspanrin/cmgTuples/{0}'.format( Dset )
    dest = '/data/higgs/data_2016/cmgTuples/{0}'.format( Dset )

    ch = CMCHandler(source, dest)
    ch.copyFiles(ftype = 'tree',
                 recreate = args.get('f',False))

    ch.copyFiles(ftype = 'Skim',
                 ignore = True,
                 max_proc=8)
   
    # if ch.validateCopy():
    #     print('All files copied from DPM')
    # else:
    #     sys.exit()    

    ch.getSkimCount()
    ch.mergeTrees()
    ch.cleanup()




