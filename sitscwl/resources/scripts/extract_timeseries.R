#
# This file is part of sitscwl
# Copyright (C) 2022 INPE.
#
# sitscwl is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

#
# CLI Arguments [collection, start_date, end_date, bands, tiles, samples_file, cpusize, seed]
#
args <- commandArgs(TRUE)

#
# Defining randomic seed
#
set.seed(args[8])

#
# Loading the base libraries.
#
library(sf)
library(sits)

#
# General definitions.
#
collection <- args[1]
start_date <- args[2]
end_date   <- args[3]
bands      <- args[4]

tiles      <- args[5]

#
# File System.
#
output_path <- "data"
dir.create(output_path, recursive = TRUE, showWarnings = TRUE)

#
# Resources
#
multicores <- as.numeric(args[7])

#
# Defining Data Cube
#
cube <- sits_cube(
  source     = "BDC",
  collection = collection,
  start_date = start_date,
  end_date   = end_date,
  tiles      = strsplit(tiles, ",")[[1]],
  bands      = strsplit(bands, ",")[[1]]
)

#
# Define Sample files
#
sample_file <- args[6]

#
# Extract Time Series
#
samples <- sits_get_data(cube       = cube,
                         file       = sample_file,
                         multicores = multicores)

#
# Save results
#
saveRDS(samples, "data/samples_with_ts.rds")
