from sitscwl.compendium import sits_classification_compendium
from sitscwl.models import RandomForest
from sitscwl.models import SITSCube

#
# Defining the Data Cube
#
sits_cube = SITSCube(
    collection="CB4_64_16D_STK-1",
    start_date="2018-09-14",
    end_date="2019-07-28",
    bands=["BAND13", "BAND14", "BAND15", "BAND16", "EVI", "NDVI", "CMASK"],
    tiles=["022024"]
)

#
# Defining ML Model
#
ml_model = RandomForest(num_trees=1000)

#
# Creating the SITS Compendium
#

memsize = 8
cpusize = 4

bdc_access_token = ""
compendium_dir = "cbers-bahiawest-lulc"
samples = "data/samples-bahiawest.csv"

sits_classification_compendium(
    basedir=compendium_dir,
    cube=sits_cube,
    ml_model=ml_model,
    sample_file=samples,
    memsize=memsize,
    cpusize=cpusize,
    bdc_access_token=bdc_access_token
)
