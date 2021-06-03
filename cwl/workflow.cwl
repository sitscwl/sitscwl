class: Workflow
cwlVersion: v1.0

requirements:
  ScatterFeatureRequirement: {}

inputs:
  script_classification: File
  script_extract_timeseries: File

  #
  # Data Cube definitions
  #
  collection: string

  start_date: string
  end_date  : string

  tile: string[]
  tiles: string

  bands: string

  #
  # Computational Resources
  #
  memsize: int
  cpusize: int

  #
  # Classification Model Training
  #
  sample_file: File

  #
  # ML Model
  #
  ml_model: string

  #
  # Brazil Data Cube Access
  #
  bdc_access_token: string

outputs:
  result_extract_timeseries:
    type: File
    outputSource: extract_timeseries/sample_with_extracted_ts

  result_classification:
    type: Directory[]
    outputSource: classification/classified_tile

steps:
  extract_timeseries:
    run: tools/extract_timeseries.tool
    in:
      script: script_extract_timeseries

      collection: collection
      
      start_date: start_date
      end_date: end_date

      bands: bands
      tiles: tiles

      sample_file: sample_file

      bdc_access_token: bdc_access_token
    out:
      - sample_with_extracted_ts

  classification:
    run: tools/classification.tool
    scatter: tile
    in:
      script: script_classification

      collection: collection
      bands: bands

      tile: tile

      start_date: start_date
      end_date  : end_date

      memsize: memsize
      cpusize: cpusize

      ml_model: ml_model
      samples: extract_timeseries/sample_with_extracted_ts

      bdc_access_token: bdc_access_token
    out:
      - classified_tile
