# -*- coding: utf-8 -*-
from __future__ import print_function

import json

from argh.decorators import arg

from lain_cli.utils import TwoLevelCommandBase, save_config, save_global_config
from lain_sdk.yaml.conf import user_config
from six import iteritems


class ConfigCommands(TwoLevelCommandBase):

    @classmethod
    def subcommands(self):
        return [self.show, self.save, self.save_global]

    @classmethod
    def namespace(self):
        return "config"

    @classmethod
    def help_message(self):
        return "config operating"

    @classmethod
    def show(cls):
        """
        show configs of different phase, also some global configs
        """
        configs = user_config.get_config()
        for (k, v) in iteritems(configs):
            if not isinstance(v, dict):
                continue
        print(json.dumps(configs, sort_keys=True, indent=4))

    @classmethod
    @arg('prop', help="property for the special phase, e.g: domain, sso_url")
    def save(cls, phase, prop, value):
        """
        create new phase, save new config for different phase.
        e.g: lain config save local domain lain.local
        """
        save_config(phase, prop, value)
        cls.show()

    @classmethod
    def save_global(cls, prop, value):
        """
        save global config, mainly private_docker_registry
        """
        save_global_config(prop, value)
        cls.show()
