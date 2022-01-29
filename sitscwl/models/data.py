#
# This file is part of sitscwl
# Copyright (C) 2022 INPE.
#
# sitscwl is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

from typing import List


class SITSCube:
    def __init__(
        self, collection: str, start_date: str, end_date: str, bands: List, tiles: List
    ):
        self.collection = collection
        self.start_date = start_date
        self.end_date = end_date
        self.bands = bands
        self.tiles = tiles
