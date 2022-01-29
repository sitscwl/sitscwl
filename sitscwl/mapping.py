#
# This file is part of sitscwl
# Copyright (C) 2022 INPE.
#
# sitscwl is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from sitscwl import constant


def guess_cwl_type(type_name):
    """Inference a CWL.Type

    Args:
        type_name (str): Type name.
    Returns:
        object: CWL type.
    """
    if type_name not in set(list(constant.SCHEMA_TYPE_MAPPING.keys())):
        raise RuntimeError(f"Invalid type for this workflow: {type_name}")

    return constant.SCHEMA_TYPE_MAPPING[type_name]
