#
# This file is part of sitscwl
# Copyright (C) 2022 INPE.
#
# sitscwl is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from pathlib import Path
from typing import Union

from pkg_resources import resource_filename


def resource_path(resource_name: Union[str, Path]) -> Path:
    """Resource path in the package.

    Args:
        resource_name (Union[str, Path]): Resource base name.

    Returns:
        Path: Specified resource path.
    """
    return Path(resource_filename(__name__, resource_name))
