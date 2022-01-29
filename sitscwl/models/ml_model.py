#
# This file is part of sitscwl
# Copyright (C) 2022 INPE.
#
# sitscwl is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#


class SITSMachineLearningModel(dict):
    name = None

    def __str__(self):
        arguments = ",".join([f"{key}={self[key]}" for key in self.keys()])

        return f"{self.name}({arguments})"


class RandomForest(SITSMachineLearningModel):
    name = "sits_rfor"


class SupportVectorMachines(SITSMachineLearningModel):
    name = "sits_svm"


class MultinomialLogitWithLassoAndRidge(SITSMachineLearningModel):
    name = "sits_mlr"


class ExtremeGradientBoosting(SITSMachineLearningModel):
    name = "sits_xgboost"


class MultiLayerPerceptron(SITSMachineLearningModel):
    name = "sits_mlp"


class DeepResidualNetworks(SITSMachineLearningModel):
    name = "sits_ResNet"


class TemporalConvolutionalNeuralNetwork(SITSMachineLearningModel):
    name = "sits_TempCNN"
