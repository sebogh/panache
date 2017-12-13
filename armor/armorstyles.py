# -*- coding: utf-8 -*-

import os
import glob
import logging
import yaml

from armor.armorstyle import ArmorStyle
from armor.armoryaml import STYLEDEF_, COMMANDLINE_, METADATA_, FILTER_

class ArmorStyles:

    def __init__(self):
        self.styles = dict()

    def load(self, style_dir):

        # for each '*.yaml'-file in the data directory
        for path in glob.glob(os.path.join(style_dir, '*.yaml')):

            with open(path, 'r', encoding='utf-8') as f:

                # try to load YAML-data from file
                try:

                    # load YAML-data
                    data = yaml.load(f)

                    # if YAML contains style definitions
                    if STYLEDEF_ in data:

                        # add each new one
                        for style_name in data[STYLEDEF_]:

                            if style_name not in self.styles:

                                logging.info("Adding definition of style '%s' (found in '%s')."
                                             % (style_name, path))

                                self.styles[style_name] = \
                                    ArmorStyle(style_name, data[STYLEDEF_][style_name], path)

                            else:

                                logging.warning("Ignoring duplicate definition of '%s' (found in'%s')."
                                                % (style_name, path))

                except:

                    pass

    def update(self, update):

        style_name = update.name
        path = update.source

        if style_name not in self.styles:

            logging.info("Adding definition of style '%s' (found in '%s')." % (style_name, path))

            self.styles[style_name] = update

        else:
            style = self.styles[style_name]

            logging.info("Merging definition of style '%s' (found in '%s')." % (style_name, path))

            style.parent = update.parent
            style.commandline = {**style.commandline, **update.commandline}
            style.metadata = {**style.metadata, **update.metadata}
            style.filters_run = style.filters_run + update.filters_run
            style.filters_kill = style.filters_run + update.filters_kill

    def resolve(self, style_name):

        if not style_name:
            return {COMMANDLINE_: dict(), METADATA_: dict(), FILTER_: list()}

        if style_name not in self.styles:
            logging.warning("Unknown style '%s'" % style_name)
            return {COMMANDLINE_: dict(), METADATA_: dict(), FILTER_: list()}

        style = self.styles[style_name]

        # compute the parent
        parent = self.resolve(style.parent)

        # merge styles
        commandline = {**parent[COMMANDLINE_], **style.commandline}
        metadata = {**parent[METADATA_], **style.metadata}
        filters = list(filter(lambda x: x in style.filters_kill, parent[FILTER_] + style.filters_run))

        return {COMMANDLINE_: commandline, METADATA_: metadata, FILTER_: filters}