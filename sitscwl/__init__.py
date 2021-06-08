from sbg import cwl

TOOLS_DEFINITION = {
    "classification_tool": {
        "base_command": "Rscript",
        "id": "ClassificationTool",
        "script": "scripts/classification.R",
        "schema": "schema/classification_tool.json",
        "environment": cwl.Docker(docker_pull="m3nin0/sits:0.10"),
        "resources": [
            cwl.Resource(cores_min=4, ram_min=4096)
        ]
    }
}
