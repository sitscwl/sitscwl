#
# This file is part of sitscwl
# Copyright (C) 2022 INPE.
#
# sitscwl is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from sitscwl.compendium import make_classification_compendium
from sitscwl.models import RandomForest
from sitscwl.models import SITSCube

#
# Defining the Data Cube
#
sits_cube = SITSCube(
    collection="CB4_64_16D_STK-1",
    start_date="2018-08-29",
    end_date="2019-08-29",
    bands=["BAND13", "BAND14", "BAND15", "BAND16", "EVI", "NDVI", "CMASK"],
    tiles=["022024"],
)

#
# Defining ML Model
#
ml_model = RandomForest(num_trees=1000)

#
# Creating the SITS Compendium
#
memsize = 16
cpusize = 8

bdc_access_token = ""
compendium_dir = "lulc-bahia-cbers4"
samples = "../data/samples-bahiawest.csv"

make_classification_compendium(
    basedir=compendium_dir,
    cube=sits_cube,
    ml_model=ml_model,
    sample_file=samples,
    memsize=memsize,
    cpusize=cpusize,
    bdc_access_token=bdc_access_token,
)
