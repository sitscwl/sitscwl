#
# This file is part of sitscwl
# Copyright (C) 2020 INPE.
#
# sitscwl is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""sitscwl mapping operations."""

from sbg import cwl


def string_array(**kwargs) -> cwl.Array:
    """string[] type
    """
    return cwl.Array(cwl.String(), **kwargs)


"""Specific types conversion functions"""

SCHEMA_TYPE_MAPPING = {
    "File": cwl.File,
    "string": cwl.String,
    "float": cwl.Float,
    "int": cwl.Int,
    "Directory": cwl.Dir,
    "string[]": string_array
}
"""Type supported"""


def guess_type(type_name):
    if type_name not in set(list(SCHEMA_TYPE_MAPPING.keys())):
        raise RuntimeError(f"Invalid type for this workflow: {type_name}")

    return SCHEMA_TYPE_MAPPING[type_name]


"""Type Mapper for JSON and CWL"""
