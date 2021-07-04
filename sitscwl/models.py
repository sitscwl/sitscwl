from typing import List


class SITSCube:

    def __init__(self, collection: str, start_date: str, end_date: str, bands: List, tiles: List):
        self.collection = collection
        self.start_date = start_date
        self.end_date = end_date
        self.bands = bands
        self.tiles = tiles


class SITSMachineLearningModel(dict):
    name = None

    def __str__(self):
        arguments = ','.join(
            [
                f'{key}={self[key]}' for key in self.keys()
            ]
        )

        return f"{self.name}({arguments})"


class RandomForest(SITSMachineLearningModel):
    name = "sits_rfor"


class SupportVectorMachines(SITSMachineLearningModel):
    name = "sits_svm"


class LinearDiscriminantAnalysis(SITSMachineLearningModel):
    name = "sits_lda"


class QuadraticDiscriminantAnalysis(SITSMachineLearningModel):
    name = "sits_qda"


class MultinomialLogitWithLassoAndRidge(SITSMachineLearningModel):
    name = "sits_mlr"


class ExtremeGradientBoosting(SITSMachineLearningModel):
    name = "sits_xgboost"


class DeepLearning(SITSMachineLearningModel):
    name = "sits_deeplearning"


class DeepResidualNetworks(SITSMachineLearningModel):
    name = "sits_ResNet"


class DeepLearning1DConvolutionalNeuralNetwork(SITSMachineLearningModel):
    name = "sits_TempCNN"


__all__ = (
    "SITSCube",
    "SITSMachineLearningModel",

    "RandomForest",
    "SupportVectorMachines",
    "LinearDiscriminantAnalysis",
    "QuadraticDiscriminantAnalysis",
    "MultinomialLogitWithLassoAndRidge",
    "ExtremeGradientBoosting",
    "DeepLearning",
    "DeepResidualNetworks",
    "DeepLearning1DConvolutionalNeuralNetwork"
)
