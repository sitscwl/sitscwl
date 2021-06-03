cwlVersion: v1.0
class: CommandLineTool

baseCommand: Rscript

hints:
    DockerRequirement:
      dockerPull: m3nin0/sits:0.10.0

requirements:

  ResourceRequirement:
    ramMin: 4096
    coresMin: 4

inputs:
    script:
        type: File
        inputBinding:
            position: 0

    collection:
        type: string
        inputBinding:
            position: 1

    start_date:
        type: string
        inputBinding:
            position: 2

    end_date:
        type: string
        inputBinding:
            position: 3

    bands:
        type: string
        inputBinding:
            position: 4

    tiles:
        type: string
        inputBinding:
            position: 5

    sample_file:
        type: File
        inputBinding:
            position: 6

    bdc_access_token:
        type: string
        inputBinding:
            position: 7

outputs:
    sample_with_extracted_ts:
        type: File
        outputBinding:
            glob: "data/samples_with_ts.rds"
