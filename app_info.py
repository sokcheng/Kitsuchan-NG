#!/usr/bin/env python3

"""Contains application information.

Yes, it's slightly bad practice to put this in a Python file."""

NAME = "Kitsuchan-NG"
URL = "https://github.com/n303p4/Kitsuchan-NG"
DESCRIPTION = (f"This is a running instance of [{NAME}]({URL}), a modular Discord bot. Originally "
               "designed with anime images and basic utility in mind, it has become a fairly "
               f"flexible bot with decent extensibility. {NAME} surely isn't finished yet; please "
               "report any bugs you observe!")
VERSION = (0, 4, 24, "r", "Arctic")
VERSION_STRING = "{0}.{1}.{2}{3} \"{4}\"".format(*VERSION)
