from sitscwl.compendium import sits_classification_compendium
from sitscwl.models import RandomForest
from sitscwl.models import SITSCube

#
# Defining the Data Cube
#
sits_cube = SITSCube(
    collection="MOD13Q1-6",
    start_date="2018-09-14",
    end_date="2019-07-28",
    bands=["NDVI", "EVI",
           "blue_reflectance", "red_reflectance",
           "NIR_reflectance", "MIR_reflectance"],
    tiles=["012010"]
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
compendium_dir = "lulc-matogrosso-mod13q1"
samples = "../data/samples-matogrosso.csv"

sits_classification_compendium(
    basedir=compendium_dir,
    cube=sits_cube,
    ml_model=ml_model,
    sample_file=samples,
    memsize=memsize,
    cpusize=cpusize,
    bdc_access_token=bdc_access_token
)
