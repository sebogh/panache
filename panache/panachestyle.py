# -*- coding: utf-8 -*-

from typing import Dict

from panache.panacheyaml import PARENT_, COMMANDLINE_, METADATA_, FILTER_, RUN_, KILL_

class PanacheStyle:

    def __init__(self, name: str, data: Dict = None, source: str = None):

        # style name
        assert name
        self.name = name

        self.parent = None
        self.commandline = dict()
        self.metadata = dict()
        self.filters_run = list()
        self.filters_kill = list()

        # parent
        if data and PARENT_ in data:
            self.parent = data[PARENT_]

        # commandline
        if (data
                and COMMANDLINE_ in data
                and isinstance(data[COMMANDLINE_], dict)):
            self.commandline = data[COMMANDLINE_]

        # metadata
        if (data
                and METADATA_ in data
                and isinstance(data[METADATA_], dict)):
            self.metadata = data[METADATA_]

        # filter
        if (data
                and FILTER_ in data
                and isinstance(data[FILTER_], dict)):
            if (RUN_ in data[FILTER_]
                    and isinstance(data[FILTER_][RUN_], list)):
                self.filters_run = data[FILTER_][RUN_]
            if (KILL_ in data[FILTER_]
                    and isinstance(data[FILTER_][KILL_], list)):
                self.filters_kill = data[FILTER_][KILL_]

        self.source = source
