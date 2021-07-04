import json
import os

from sbg import cwl

_base_path = os.path.dirname(__file__)

TOOLS_DEFINITION = {
    "extract_timeseries": {
        "base_command": "Rscript",
        "id": "ExtracTimeseriesTool",
        "schema": os.path.join(_base_path, "schema/extract_timeseries_tool.json"),
        "requirements": [
            cwl.Docker(docker_pull="brazildatacube/sits:0.12.0")
        ],
        "hints": [
            cwl.Resource(cores_min=4, ram_min=4096)
        ]
    },
    "classification": {
        "base_command": "Rscript",
        "id": "ClassificationTool",
        "schema": os.path.join(_base_path, "schema/classification_tool.json"),
        "requirements": [
            cwl.Docker(docker_pull="brazildatacube/sits:0.12.0")
        ],
        "hints": [
            cwl.Resource(cores_min=4, ram_min=4096)
        ]
    }
}

TOOLS_CONNECTIONS = json.load(
    open(
        os.path.join(_base_path, "schema/connections.json")
    )
)

"""Workflow tools definitions"""

BDC_STAC_URL = "https://brazildatacube.dpi.inpe.br/stac/"
"""Brazil Data Cube definitions"""

SITS_R_SCRIPTS = {
    "script_extract_timeseries": "scripts/extract_timeseries.R",
    "script_classification": "scripts/classification.R"
}
