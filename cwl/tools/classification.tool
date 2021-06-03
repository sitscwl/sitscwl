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

    tile:
        type: string
        inputBinding:
            position: 5

    memsize:
        type: int
        inputBinding:
            position: 6

    cpusize:
        type: int
        inputBinding:
            position: 7

    samples:
        type: File
        inputBinding:
            position: 8

    ml_model:
        type: string
        inputBinding:
            position: 9

    bdc_access_token:
        type: string
        inputBinding:
            position: 10

outputs:
    classified_tile:
        type: Directory
        outputBinding:
            glob: "data"
