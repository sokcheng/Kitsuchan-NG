#!/usr/bin/env python3

# https://stackoverflow.com/questions/1057431/loading-all-modules-in-a-folder-in-python#1057534
from os.path import dirname, basename, isfile
import glob
modules = glob.glob(dirname(__file__)+"/*.py")
__all__ = [ basename(f)[:-3] for f in modules if isfile(f)]
