from abc import ABC
from abc import abstractmethod

from sbg import cwl

from .mapping import guess_type


class Builder(ABC):

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


class ToolBuilder(Builder):

    def __init__(self):
        self._tool = None
        self.reset()

    def reset(self):
        self._tool = cwl.CommandLineTool()

    def add_id(self, id: str):
        self._tool.id = id

    def add_script(self):
        self._tool.add_input(
            cwl.File(required=True),
            "script",
            label="script",
            input_binding=cwl.InputBinding(
                shell_quote=False,
                position=0
            )
        )

    def add_base_command(self, base_command: str):
        self._tool.base_command = [base_command]

    def add_input_schema(self, input_schema: list):
        for element in input_schema:
            element_type = guess_type(element["type"])

            self._tool.add_input(
                element_type(required=True),
                element["name"],
                label=element["name"],
                input_binding=cwl.InputBinding(
                    shell_quote=0,
                    position=element["inputBindingPosition"]
                )
            )

    def add_output_schema(self, output_schema: list):
        for element in output_schema:
            element_type = guess_type(element["type"])

            self._tool.add_input(
                element_type(required=True),
                element["name"],
                label=element["name"],
                input_binding=cwl.OutputBinding(
                    glob=element["outputBindingGlob"]
                )
            )


def tool_builder(id: str, base_command: str, schema: dict) -> str:
    pass
