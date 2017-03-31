#!/usr/bin/env python3

"""This module contains environment variables that have been passed to the program as config."""

import os

OAUTH_TOKEN_DISCORD = os.environ["OAUTH_TOKEN_DISCORD"]
API_KEY_IBSEARCH = os.environ.get("API_KEY_IBSEARCH", None)
COMMAND_PREFIX = os.environ.get("COMMAND_PREFIX", None)
EXTENSIONS = tuple(os.environ.get("EXTENSIONS", "cogs.core:cogs.mod:cogs.web").split(":"))
WHITELIST_NSFW = os.environ.get("WHITELIST_NSFW", "").split(":")
