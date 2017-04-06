#!/usr/bin/env python3

"""This module contains environment variables that have been passed to the program as config."""

import os
import json
import logging

FILENAME = "config.json"
FOLDER_COGS = "cogs"
DEFAULT_EXTENSIONS = []
# This dynamically creates the default list of cogs.
for fname in os.listdir(FOLDER_COGS):
    if os.path.isfile(os.path.join(FOLDER_COGS, fname)):
        DEFAULT_EXTENSIONS.append("%s.%s" % (FOLDER_COGS, fname.replace(".py", "")))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

manager = {}

def load(filename:str=FILENAME):
    """Load config settings from filename.
    
    filename - The name of the file you wish to write to."""
    logger.info("Loading config file.")
    try:
        with open(filename) as f:
            new_settings = json.load(f)
        for key, value in new_settings.items():
            # This if/elif block checks types. If a setting is of the wrong type, it is skipped.
            if (key == "WHITELIST_NSFW" and not isinstance(value, list)):
                continue
            elif (key == "OAUTH_TOKEN_DISCORD" and not isinstance(value, str)):
                continue
            elif (key == "API_KEY_IBSEARCH" and not isinstance(value, str)):
                continue
            elif (key == "COMMAND_PREFIX" and not isinstance(value, str)):
                continue
            elif (key == "EXTENSIONS" and not isinstance(value, list)):
                continue
            manager[key] = value
    except FileNotFoundError as error:
        logger.warning("Config file not found!")
        raise error
    except IOError as error:
        logger.critical("Config file could not be read!")
        raise error
    except json.decoder.JSONDecodeError as error:
        logger.critical("Config file is not valid JSON!")
        raise error

def save(filename:str=FILENAME, manager=manager):
    """Save config settings to FILENAME.
    
    filename - The name of the file you wish to write to.
    manager - The JSON data you want to write."""
    logger.info("Saving/creating config file.")
    try:
        with open(filename, "w") as f:
            json.dump(manager, f)
    except IOError as error:
        logger.warning("Could not write config!")

try:
    load()
except (FileNotFoundError or IOError or json.decoder.JSONDecodeError):
    save()
