#
# This file is part of sitscwl
# Copyright (C) 2022 INPE.
#
# sitscwl is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

#
# CLI Arguments
# [collection, start_date, end_date, bands, tile, memsize, cpusize, samples_file, ml_model, seed]
#
args <- commandArgs(TRUE)

#
# Defining randomic seed
#
set.seed(args[10])

#
# Loading the base libraries.
#
library(sf)
library(sits)

#
# General definitions
#
collection <- args[1]
start_date <- args[2]
end_date   <- args[3]
bands      <- args[4]

tile       <- args[5]

#
# File System
#
output_path <- paste("data", tile, sep = "/")
dir.create(output_path, recursive = TRUE, showWarnings = TRUE)

#
# Resources
#
memsize    <- as.numeric(args[6])
multicores <- as.numeric(args[7])

#
# Defining Data Cube
#
cube <- sits_cube(
  source     = "BDC",
  collection = collection,
  start_date = start_date,
  end_date   = end_date,
  tiles      = c(tile),
  bands      = strsplit(bands, ",")[[1]]
)

# Fixing data cube resolutions (Temporary)
cube$file_info <- lapply(cube$file_info, function(x) {
    x$xres <- as.numeric(substring(toString(x$xres), 1, 5))
    x$yres <- as.numeric(substring(toString(x$yres), 1, 5))
    x
})

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
                            multicores = multicores,
                            memsize    = memsize)

#
# Classify Smoothed Map
#
probs_smoothed_cube <- sits_smooth(probs_cube,
                                   output_dir = output_path,
                                   memsize    = memsize)

label_cube <- sits_label_classification(probs_smoothed_cube,
                                        output_dir = output_path)
