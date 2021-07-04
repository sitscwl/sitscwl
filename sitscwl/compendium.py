import json
import os
import pathlib
import shutil
from abc import ABC
from abc import abstractmethod
from typing import List

from sitscwl.models import SITSMachineLearningModel, SITSCube


def _remove_first_dir(path):
    return str(
        pathlib.Path(
            *pathlib.Path(path).parts[1:]
        )
    )


class PackageBuilder(ABC):

    @abstractmethod
    def add_sample_file(self, sample_file):
        pass

    @abstractmethod
    def add_ml_model(self, ml_model):
        pass

    @abstractmethod
    def add_collection(self, collection):
        pass

    @abstractmethod
    def add_start_date(self, start_date):
        pass

    @abstractmethod
    def add_end_date(self, end_date):
        pass

    @abstractmethod
    def add_bands(self, bands):
        pass

    @abstractmethod
    def add_tiles(self, tiles):
        pass

    @abstractmethod
    def add_memsize(self, memsize):
        pass

    @abstractmethod
    def add_cpusize(self, cpusize):
        pass

    @abstractmethod
    def add_bdcstac_url(self, bdcstac_url):
        pass

    @abstractmethod
    def add_bdc_access_token(self, bdc_access_token):
        pass

    @abstractmethod
    def from_cube(self, cube):
        pass

    @abstractmethod
    def build(self):
        pass


class SITSPackageBuilder(PackageBuilder):

    def __init__(self, basedir):
        self._basedir = basedir
        self._package_configurations = {}

    def add_sample_file(self, sample_file):
        if not os.path.isfile(sample_file):
            raise FileNotFoundError(f"{sample_file} not found!")

        if ".shp" in sample_file:
            raise NotImplemented("Shapefile support is not implemented yet. Instead, use a csv file")

        self._package_configurations["sample_file"] = {
            "class": "File",
            "path": sample_file
        }

        return self

    def add_ml_model(self, ml_model: SITSMachineLearningModel):
        if not isinstance(ml_model, SITSMachineLearningModel):
            raise TypeError("ml_model must be a SITSMachineLearningModel")

        self._package_configurations["ml_model"] = str(ml_model)

        return self

    def add_collection(self, collection: str):
        self._package_configurations["collection"] = collection

        return self

    # ToDo: Validate
    def add_start_date(self, start_date: str):
        self._package_configurations["start_date"] = start_date

        return self

    # ToDo: Validate
    def add_end_date(self, end_date: str):
        self._package_configurations["end_date"] = end_date

        return self

    def add_bands(self, bands: List):
        if not isinstance(bands, list):
            # ToDo: Create a decorator for this
            raise TypeError("bands must be a list")

        self._package_configurations["bands"] = ",".join(bands)
        return self

    def add_tiles(self, tiles: List):
        if not isinstance(tiles, list):
            raise TypeError("bands must be a list")

        self._package_configurations["tile"] = tiles
        self._package_configurations["sample_tiles"] = ",".join(tiles)
        return self

    def add_memsize(self, memsize: str):
        self._package_configurations["memsize"] = memsize

        return self

    def add_cpusize(self, cpusize):
        self._package_configurations["cpusize"] = cpusize

        return self

    def add_bdcstac_url(self, bdcstac_url):
        self._package_configurations["bdc_url"] = bdcstac_url

        return self

    def add_bdc_access_token(self, bdc_access_token):
        self._package_configurations["bdc_access_token"] = bdc_access_token

        return self

    def from_cube(self, cube):
        if not isinstance(cube, SITSCube):
            raise TypeError("cube must be a SITSCube")

        for propertie in list(filter(lambda x: '__' not in x, dir(cube))):
            propertie_value = getattr(cube, propertie)

            if propertie_value:
                self._package_configurations[propertie] = propertie_value

        return self

    def build(self):

        #
        # Creating base directory
        #
        os.makedirs(self._basedir, exist_ok=True)

        #
        # Copy sample files
        #
        original_sample_file = self._package_configurations["sample_file"]["path"]

        samples_dir = os.path.join(self._basedir, "data")
        os.makedirs(samples_dir, exist_ok=True)

        target_samples_file = os.path.join(samples_dir, os.path.basename(original_sample_file))
        shutil.copy(original_sample_file, target_samples_file)

        self._package_configurations["sample_file"]["path"] = _remove_first_dir(target_samples_file)

        #
        # Configuring bands and tiles
        #
        bands = self._package_configurations["bands"]
        tiles = self._package_configurations["tiles"]

        if isinstance(bands, list):
            self._package_configurations["bands"] = ",".join(bands)

        if not self._package_configurations.get("sample_tiles", False):
            self._package_configurations["sample_tiles"] = ",".join(tiles)

        #
        # Copying R scripts
        #
        from . import SITS_R_SCRIPTS

        package_dir = os.path.dirname(__file__)
        scripts_dir = os.path.join(self._basedir, "scripts")

        os.makedirs(scripts_dir, exist_ok=True)

        for key in SITS_R_SCRIPTS.keys():
            source = os.path.join(package_dir, SITS_R_SCRIPTS[key])
            target = os.path.join(scripts_dir, os.path.basename(SITS_R_SCRIPTS[key]))

            shutil.copy(source, target)

            self._package_configurations[key] = {
                "class": "File",
                "path": _remove_first_dir(target)
            }

        #
        # Save inputs and workflow file
        #

        # inputs
        with open(os.path.join(self._basedir, "inputs.json"), "w") as file:
            json.dump(self._package_configurations, file)

        # workflow
        from .workflow import classification_workflow
        classification_workflow.workflow.dump(
            os.path.join(self._basedir, "workflow.cwl")
        )


def sits_classification_compendium(basedir, cube, sample_file, ml_model, memsize, cpusize, bdc_access_token):
    from . import BDC_STAC_URL

    (
        SITSPackageBuilder(basedir)
            .from_cube(cube)
            .add_sample_file(sample_file)
            .add_ml_model(ml_model)
            .add_memsize(memsize)
            .add_cpusize(cpusize)
            .add_bdcstac_url(BDC_STAC_URL)
            .add_bdc_access_token(bdc_access_token)
    ).build()


__all__ = (
    "PackageBuilder",
    "SITSPackageBuilder",
    "sits_classification_compendium"
)
