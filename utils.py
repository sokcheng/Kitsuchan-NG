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

# https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python
def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]
