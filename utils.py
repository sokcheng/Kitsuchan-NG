#!/usr/bin/env python3

"""Contains small helper functions."""

import hashlib
import base64
import random

def to_hash(string):
    """Generate an SHA-512 hash for a string."""
    bytes = string.encode("utf-8")
    the_hash = hashlib.sha512()
    the_hash.update(bytes)
    hash_string = the_hash.hexdigest()
    return hash_string

def random_color():
    """Generate a random int representing a random color."""
    return random.randint(0x000000, 0xFFFFFF)
