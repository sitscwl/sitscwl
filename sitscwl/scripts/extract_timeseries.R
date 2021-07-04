set.seed(777)

library(sf)
library(sits)

#
# CLI Arguments [collection, start_date, end_date, bands, tiles, samples_file, bdc_url, bdc_access_token]
#
args <- commandArgs(TRUE)

#
# Defining Access Token
#
Sys.setenv("BDC_ACCESS_KEY" = args[8])

#
# General definitions
#
collection <- args[1]
start_date <- args[2]
end_date <- args[3]
bands <- args[4]

tiles <- args[5]

#
# File System
#
output_path <- "data"
dir.create(output_path, recursive = TRUE, showWarnings = TRUE)

#
# Defining Data Cube
#
cube <- sits_cube(
  source = "BDC",
  name = "cube",
  url = args[7],
  collection = collection,
  start_date = start_date,
  end_date = end_date,
  tiles = strsplit(tiles, ",")[[1]],
  bands = strsplit(bands, ",")[[1]]
)

#
# Define Sample files
#
sample_file <- args[6]

#
# Extract Time Series
#
samples <- sits_get_data(cube = cube, file = sample_file)

#
# Save results
#
saveRDS(samples, "data/samples_with_ts.rds")
