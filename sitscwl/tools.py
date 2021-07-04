import json
from abc import ABC
from abc import abstractmethod

from sbg import cwl

from .mapping import guess_type


class CWLBuilder(ABC):

    @abstractmethod
    def add_id(self, id: str):
        pass

    @abstractmethod
    def add_base_command(self, base_command: str):
        pass

    @abstractmethod
    def add_input_schema(self, input_schema: list):
        pass

    @abstractmethod
    def add_output_schema(self, output_schema: list):
        pass

    @abstractmethod
    def add_requirements(self, requirements: list):
        pass

    @abstractmethod
    def add_hints(self, hints: list):
        pass

    @abstractmethod
    def build(self):
        pass


class ToolBuilder(CWLBuilder):

    def __init__(self):
        self._tool = None
        self.reset()

    def reset(self):
        self._tool = cwl.CommandLineTool()

    def add_id(self, id: str):
        self._tool.id = id

        return self

    def add_base_command(self, base_command: str):
        self._tool.base_command = [base_command]

        return self

    # ToDo: Support to extra CWL parameters
    def add_input_schema(self, input_schema: list):
        for element in input_schema:

            # if variable is scatter, remove array type
            if element.get("isScatter", False):
                element["type"] = element["type"].replace("[]", "")

            element_type = guess_type(element["type"])

            self._tool.add_input(
                element_type(required=True),
                element["name"],
                label=element["name"],
                input_binding=cwl.InputBinding(
                    position=element["inputBindingPosition"]
                )
            )

        return self

    def add_output_schema(self, output_schema: list):
        for element in output_schema:
            element_type = guess_type(element["type"])

            self._tool.add_output(
                element_type(required=True),
                element["name"],
                label=element["name"],
                output_binding=cwl.OutputBinding(
                    glob=element["outputBindingGlob"]
                )
            )
        return self

    def add_requirements(self, requirements: list):
        for requirement in requirements:
            self._tool.add_requirement(requirement)

        return self

    def add_hints(self, hints: list):
        for hint in hints:
            self._tool.add_hints(hint)

        return self

    def build(self):
        return self._tool


def tool_builder(id: str, base_command: str, schema: str, requirements: list, hints: list):
    with open(schema, "r") as schema_file:
        schema_definitions: dict = json.load(schema_file)

        return (
            ToolBuilder()
                .add_id(id)
                .add_base_command(base_command)
                .add_input_schema(schema_definitions.get("inputs"))
                .add_output_schema(schema_definitions.get("outputs"))
                .add_requirements(requirements)
                .add_hints(hints)
        ).build()


__all__ = (
    "CWLBuilder",
    "ToolBuilder",
    "tool_builder"
)
