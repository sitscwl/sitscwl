import json
from typing import Dict
from typing import List

from sbg import cwl

from .tools import tool_builder


def _create_workflow_input_with_intersection_values(tools: dict) -> List:
    """Creates a multiple WorkflowInput using pre-defined tools. This functions assumes that, the
    Workflow inputs with same name should be used as same input
    """

    def _search_for_name(name: str, list_of_inputs: List[Dict]) -> Dict:
        for input in list_of_inputs:
            if input.get("name") == name:
                return input

    inputs = []
    workflow_inputs = []

    # load all inputs
    for tool in tools:
        tool_definitions = tools.get(tool)

        inputs.extend(
            json.load(open(tool_definitions["schema"], "r")).get("inputs")
        )

    # only use "name" intersection
    intersected_names = list(set([d["name"] for d in inputs]))

    for intersected_name in intersected_names:
        input_definition = _search_for_name(intersected_name, inputs)

        # create the workflow input
        workflow_inputs.append(
            cwl.WorkflowInput(
                id=input_definition.get("name"),
                label=input_definition.get("name"),
                type=input_definition.get("type")
            )
        )
    return workflow_inputs


class ClassificationWorkflow(object):
    def __init__(self):
        self._workflow = cwl.Workflow()

    @property
    def workflow(self):
        return self._workflow

    def add_tools(self, tools):

        use_scatter = False

        for tool in tools:
            tool_definitions = tools.get(tool)
            tool_obj = tool_builder(**tool_definitions)

            # search for scatter inputs
            scatter_method = None
            inputs_with_scatter = []

            with open(tool_definitions["schema"], "r") as tool_schema_file:
                tool_schema = json.load(tool_schema_file)

                for input in tool_schema["inputs"]:
                    if input.get("isScatter"):
                        use_scatter = True
                        inputs_with_scatter.append(input.get("name"))

            # get scatter method in case of multiple variables
            if len(inputs_with_scatter) > 1:
                scatter_method = tool_definitions.get("scatter_method")

            self._workflow.add_step(
                tool_obj,
                scatter=None if not inputs_with_scatter else inputs_with_scatter,
                scatter_method=scatter_method
            )

        # variable changed in scatter variable search
        if use_scatter:
            self._workflow.add_requirement(cwl.ScatterFeature())

        # define workflow input with only input intersections
        self._workflow.inputs = _create_workflow_input_with_intersection_values(tools)


from . import TOOLS_DEFINITION

classification_workflow = ClassificationWorkflow()
classification_workflow.add_tools(TOOLS_DEFINITION)

__all__ = (
    "classification_workflow"
)
