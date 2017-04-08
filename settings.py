#!/usr/bin/env python3

"""This module handles I/O operations to configuration files."""

import os
import json
import logging

FILE_CONFIG = "config.json"
FOLDER_COGS = "cogs"
DEFAULT_EXTENSIONS = []
# Dynamically create the default list of cogs.
if os.path.isdir(FOLDER_COGS):
    for fname in os.listdir(FOLDER_COGS):
        if os.path.isfile(os.path.join(FOLDER_COGS, fname)):
            DEFAULT_EXTENSIONS.append("%s.%s" % (FOLDER_COGS, fname.replace(".py", "")))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

manager = {}

def load(filename:str=FILE_CONFIG):
    """Load config from a file. If no filename is specified, it modifies settings.manager.
    Otherwise, it returns the config it just loaded.
    
    filename - The name of the file you wish to write to, defaults to FILE_CONFIG."""
    logger.info("Loading config file.")
    try:
        with open(filename) as f:
            new_settings = json.load(f)
        # Treat things differently here. If the filename is the stock FILE_CONFIG, then the load
        # command should modify the global manager and return None.
        if filename == FILE_CONFIG:
            for key, value in new_settings.items():
                manager[key] = value
        # Otherwise, it returns the new_settings so they can be used in a cog-based extension.
        else:
            return new_settings
    except FileNotFoundError as error:
        logger.warning("Config file not found!")
        raise error
    except IOError as error:
        logger.critical("Config file could not be read!")
        raise error
    except json.decoder.JSONDecodeError as error:
        logger.critical("Config file is not valid JSON!")
        raise error

def save(filename:str=FILE_CONFIG, manager=manager):
    """Save JSON config settings to a file.
    
    filename - The name of the file you wish to write to, defaults to FILE_CONFIG.
    manager - The JSON data you want to write, defaults to settings.manager.
    """
    logger.info("Saving/creating config file.")
    try:
        with open(filename, "w") as f:
            json.dump(manager, f)
    except IOError as error:
        logger.warning("Could not write config!")
