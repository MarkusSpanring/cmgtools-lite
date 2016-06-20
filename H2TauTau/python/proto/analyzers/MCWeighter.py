import math
import numpy
from DataFormats.FWLite import Handle, Runs
from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.HeppyCore.statistics.counter import Counter, Counters

class MCWeighter(Analyzer):

    '''Retrieves the pre-skim *weighed* event count and puts it in the event'''

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(MCWeighter, self).__init__(cfg_ana, cfg_comp, looperName)
        self.mcweight = 1.
        if hasattr(cfg_ana, 'countSign'):
            self.countSign = cfg_ana.countSign
        else:
            self.countSign = False

    def beginLoop(self, setup):
        '''
        Compute the weight just once at the beginning of the loop.
        Warning: this works correctly only the file(s) is(are) 
        completely processed.
        '''
        super(MCWeighter, self).beginLoop(setup)

        # runsHandle = Handle('std::vector<double>')
        # runsLabel = ('genEvtWeightsCounter', 'genWeight', 'H2TAUTAU')

        # Make it compatible with SkimAnalyzerCount
        self.counters.addCounter('SkimReport')
        self.count = self.counters.counter('SkimReport')
        if self.cfg_comp.isMC: 
            self.count.register('Sum Weights')
            self.count.register('Sum Unity Weights')
        else:
            return

        self.runs = Runs(self.cfg_comp.files)
        print 'Files', self.cfg_comp.files

        runsHandle = Handle('double')
        runsLabel = ('genEvtWeightsCounter', '', 'MVAMET')

        runsHandleU = Handle('double')
        runsLabelU = ('genEvtWeightsCounter', 'sumUnityGenWeights', 'MVAMET')

        mcw = []
        mcuw = []
        for run in self.runs:
            run.getByLabel(runsLabel, runsHandle)
            mcw += [runsHandle.product()[0]]
            run.getByLabel(runsLabelU, runsHandleU)
            mcuw += [runsHandleU.product()[0]]

        # self.mcweight = numpy.mean(mcw)

        self.count.inc('Sum Weights', numpy.sum(mcw))
        self.count.inc('Sum Unity Weights', numpy.sum(mcuw))

        # if self.countSign:
            # self.mcweight = numpy.mean([math.copysign(1., x) for x in mcw])

        # print 'aMC@NLO weight', self.mcweight


    def process(self, event):
        event.mcweight = float(self.mcweight)
