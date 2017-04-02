#!/usr/bin/env python3

"""This module contains environment variables that have been passed to the program as config."""

import json
import logging

FILENAME = "config.json"
DEFAULT_EXTENSIONS = ("cogs.core", "cogs.utilities", "cogs.moderation", "cogs.web", "cogs.reactions")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

manager = {
               "OAUTH_TOKEN_DISCORD": "",
               "WHITELIST_NSFW": [],
           }

def load():
    """Load config settings from FILENAME."""
    try:
        with open(FILENAME) as f:
            new_settings = json.load(f)
        for key, value in new_settings.items():
            # This if/elif block checks types. If a setting is of the wrong type, it is skipped.
            if (key is "WHITELIST_NSFW" and not isinstance(value, list)):
                continue
            elif (key is "OAUTH_TOKEN_DISCORD" and not isinstance(value, str)):
                continue
            elif (key is "API_KEY_IBSEARCH" and not isinstance(value, str)):
                continue
            elif (key is "COMMAND_PREFIX" and not isinstance(value, str)):
                continue
            elif (key is "EXTENSIONS" and not isinstance(value, list)):
                continue
            manager[key] = value
    except FileNotFoundError as error:
        logger.critical("Config file not found!")
        raise error
    except IOError as error:
        logger.critical("Config file could not be read!")
        raise error
    except json.decoder.JSONDecodeError as error:
        logger.critical("Config file is not valid JSON!")
        raise error

def save():
    """Save config settings to FILENAME."""
    try:
        with open(FILENAME, "w") as f:
            json.dump(manager, f)
    except IOError as error:
        logger.warning("Could not write config!")

try:
    load()
except (FileNotFoundError or IOError or json.decoder.JSONDecodeError):
    save()
