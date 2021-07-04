import itertools
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

    def add_tools(self, tools, connections):

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
                scatter_method=scatter_method,
                unique_names=False  # unique_names is added on https://github.com/M3nin0/sevenbridges-cwl/blob/master/sbg/cwl/v1_0/wf/workflow.py
            )

        # check connections
        def _remove_duplications(x, valid_connection):
            if isinstance(x['source'], list) and len(x['source']) > 1:
                for source in x['source']:
                    if source == valid_connection.replace(".", "/"):
                        x['source'] = source
            return x

        for connection in connections:
            self._workflow.add_connection(connection["source"], connection["target"])

            # remove duplicated 'in' values from steps!
            # the 'duplicated' values is inserted with connections, so it's necessary remove them
            for idx, step in enumerate(self._workflow.steps):
                self._workflow.steps[idx]['in'] = list(
                    map(_remove_duplications, step['in'], itertools.repeat(connection["source"]))
                )

        # variable changed in scatter variable search
        if use_scatter:
            self._workflow.add_requirement(cwl.ScatterFeature())

        # define workflow input with only input intersections
        self._workflow.inputs = _create_workflow_input_with_intersection_values(tools)


from . import TOOLS_DEFINITION
from . import TOOLS_CONNECTIONS

classification_workflow = ClassificationWorkflow()
classification_workflow.add_tools(TOOLS_DEFINITION, TOOLS_CONNECTIONS)

__all__ = (
    "classification_workflow"
)
