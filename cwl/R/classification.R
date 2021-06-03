set.seed(777)

library(sf)
library(sits)

#
# CLI Arguments [collection, start_date, end_date, tile, memsize, cpusize, samples file, bdc_access_token]
#
args <- commandArgs(TRUE)

#
# Defining Access Token
#
Sys.setenv("BDC_ACCESS_KEY" = args[10])

#
# General definitions
#
collection  <- args[1]
start_date  <- args[2]
end_date    <- args[3]
bands       <- args[4]

tile        <- args[5]

#
# File System
#
output_path <- "data"
dir.create(output_path, recursive = TRUE, showWarnings = TRUE)

#
# Resources
#
memsize     <- as.numeric(args[6])
multicores  <- as.numeric(args[7])

#
# Defining Data Cube
#
cube <- sits_cube(
  type        = "BDC",
  name        = "cube",
  url         = "https://brazildatacube.dpi.inpe.br/stac/",
  collection  = collection,
  start_date  = start_date,
  end_date    = end_date,
  tiles       = c(tile),
  bands       = strsplit(bands, ",")[[1]]
)

#
# Extract Samples Time Series
#
samples <- readRDS(args[8])

#
# Training ML  Model
#
ml_model <- sits_train(data      = samples,
                       ml_method = eval(parse(
                          text = args[9]
                       )))

#
# Classify the Data Cube
#
probs_cube <- sits_classify(cube,
                            ml_model   = ml_model,
                            output_dir = output_path,
                            memsize    = memsize)

#
# Classify Smoothed Map
#
probs_smoothed_cube <- sits_smooth(probs_cube,
                                   output_dir = output_path)

label_cube <- sits_label_classification(probs_smoothed_cube,
                                        output_dir = output_path)
