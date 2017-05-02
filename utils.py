#!/usr/bin/env python3

"""Contains small helper functions. These DO NOT have discord.py dependencies."""

import hashlib
import math
import random

# Instantiate a SystemRandom object to produce cryptographically secure random numbers.
systemrandom = random.SystemRandom()

def to_hash(string):
    """Generate an SHA-512 hash for a string."""
    bytes = string.encode("utf-8")
    the_hash = hashlib.sha512()
    the_hash.update(bytes)
    hash_string = the_hash.hexdigest()
    return hash_string

def random_color():
    """Generate a random int representing a random color."""
    return systemrandom.randint(0x000000, 0xFFFFFF)

# https://stackoverflow.com/questions/2189800/length-of-an-integer-in-python/2189827#2189827
def digits(number:float):
    """Compute the number of digits in a number."""
    return int(math.log10(number))+1
