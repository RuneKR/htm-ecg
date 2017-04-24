#!/usr/bin/python

import numpy as np
from nupic.research.spatial_pooler import SpatialPooler
from nupic.research.temporal_memory import TemporalMemory
from nupic.algorithms.sdr_classifier_factory import SDRClassifierFactory


class Layer(object):
    """One combined layer of spatial and temporal pooling """

    # function called on init of layer
    def __init__(self, config):

        # Calculate the size of input and col space
        inputsize = np.array(config['inputDimensions']).prod()
        colsize = np.array(config['columnDimensions']).prod()

        # setup the pooler and reference to active column holder
        self.sp = SpatialPooler(
            inputDimensions=config['inputDimensions'],
            columnDimensions=config['columnDimensions'],
            potentialRadius=int(config['potentialRadius'] * inputsize),
            numActiveColumnsPerInhArea=int(
                config['amountActiveCols'] * colsize),
            globalInhibition=config['inhibition']
        )

        # reference to active columns set that is output of the spatial pooler
        self.activeColumns = np.zeros(colsize, config['uintType'])

        # setup the temporal pooler
        self.tm = TemporalMemory(
            columnDimensions=config['columnDimensions'],
            cellsPerColumn=config['cellsPerColumn']
        )

        # setup iterations
        self.sp.setIterationLearnNum(config['numIterations'])
        self.sp.setIterationNum(config['numIterations'])

    # learn the pools based upon the data
    def learn(self, data):
        """learn the spatical and temporal pooling on the dataset"""

        # run the spatial pooling
        self.sp.compute(
            data,
            True,
            self.activeColumns
        )

        # run the temporal pooling
        self.tm.compute(self.activeColumns, True)

    # predict the pools based upon the data
    def predict(self, data):
        """learn the spatical and temporal pooling on the dataset"""

        # run the spatial pooling
        self.sp.compute(
            data,
            False,
            self.activeColumns
        )

        # run the temporal pooling
        self.tm.compute(self.activeColumns, False)

        # return the result so it can be used in the next layer

class TopNode(object):
    """Performs classifcation from reference output node """

    # function called on init of layer
    def __init__(self, config):

        # save the references and configuration
        self.classifier = SDRClassifierFactory.create(config)

    def learn(self, target, bucketIdx, actValue, recordNum):
        """Learns to classify the underlying patterns"""

        # get the patterns from target
        patternNZ = target.getActiveCells()

        # The classification
        self.classifier.compute(
            recordNum=recordNum,
            patternNZ=patternNZ,
            classification={
                "bucketIdx": bucketIdx,
                "actValue": actValue
            },
            learn=True,
            infer=False
        )

        # returns that learning has been done
        return True

    def predic(self, target, recordNum):
        """Predicts the sample based upon the underlying patterns"""

        # get the patterns from target
        patternNZ = target.getActiveCells()

        # inference
        result = self.classifier.compute(
            recordNum=recordNum,
            patternNZ=patternNZ,
            learn=False,
            infer=True
        )

        # Print the top three predictions for 1 steps out.
        topPredictions = sorted(
            zip(result[1], result["actualValues"]), reverse=True)[:3]

        # returns the top predictions for sample
        return topPredictions
