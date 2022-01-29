#
# This file is part of sitscwl
# Copyright (C) 2022 INPE.
#
# sitscwl is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

import json

from sbg import cwl

from sitscwl.resource import resource_path

#
# General definitions.
#

# Brazil Data Cube STAC Service URL.
BDC_STAC_URL = "https://brazildatacube.dpi.inpe.br/stac/"

#
# SITS definitions
#
SITS_CPU_HINT = 4
SITS_MEM_HINT = 4096

SITS_ENVIRONMENT_IMAGE = "brazildatacube/sits:0.12.0"

SITS_R_SCRIPTS = {
    "script_extract_timeseries": resource_path(
        "resources/scripts/extract_timeseries.R"
    ),
    "script_classification": resource_path("resources/scripts/classification.R"),
}

#
# SITS workflow steps schema
#

# Steps connection schema.
SITS_STEP_CONNECTIONS = resource_path("resources/schema/connections.json")

# Classify data cube step schema.
SITS_STEP_SCHEMA_CLASSIFY = resource_path("resources/schema/classification_tool.json")

# Extract time series step schema.
SITS_STEP_SCHEMA_EXTRACT_TS = resource_path(
    "resources/schema/extract_timeseries_tool.json"
)


#
# Definition tools
#
TOOLS_DEFINITION = {
    "extract_timeseries": {
        "base_command": "Rscript",
        "id": "ExtracTimeseriesTool",
        "schema": SITS_STEP_SCHEMA_EXTRACT_TS,
        "requirements": [
            cwl.Docker(docker_pull=SITS_ENVIRONMENT_IMAGE),
            cwl.EnvVar(
                cwl.EnvironmentDef("BDC_ACCESS_TOKEN", "$inputs.bdc_access_token")
            ),
        ],
        "hints": [cwl.Resource(cores_min=SITS_CPU_HINT, ram_min=SITS_MEM_HINT)],
    },
    "classification": {
        "base_command": "Rscript",
        "id": "ClassificationTool",
        "schema": SITS_STEP_SCHEMA_CLASSIFY,
        "requirements": [
            cwl.Docker(docker_pull=SITS_ENVIRONMENT_IMAGE),
            cwl.EnvVar(
                cwl.EnvironmentDef("BDC_ACCESS_TOKEN", "$inputs.bdc_access_token")
            ),
        ],
        "hints": [cwl.Resource(cores_min=SITS_CPU_HINT, ram_min=SITS_MEM_HINT)],
    },
}

TOOLS_CONNECTIONS = json.load(SITS_STEP_CONNECTIONS.open())

#
# CWL Supported types
#

SCHEMA_TYPE_MAPPING = {
    "File": cwl.File,
    "string": cwl.String,
    "float": cwl.Float,
    "int": cwl.Int,
    "Directory": cwl.Dir,
    "string[]": lambda **kwargs: cwl.Array(cwl.String(), **kwargs),
}
"""Supported types."""
