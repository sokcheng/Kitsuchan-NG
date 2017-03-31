#!/usr/bin/env python3

"""This module contains environment variables that have been passed to the program as config."""

import os

API_KEY_DISCORD = os.environ["API_KEY_DISCORD"]
API_KEY_IBSEARCH = os.environ["API_KEY_IBSEARCH"]
COMMAND_PREFIX = os.environ.get("COMMAND_PREFIX", None)
WHITELIST_NSFW = os.environ.get("WHITELIST_NSFW", "").split(":")
