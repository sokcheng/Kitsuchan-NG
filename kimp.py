#!/usr/bin/env python3

"""
kimp.py

This small library handles image manipulation via HTML templating. It's as basic as it sounds.
"""

import base64
import os

HTML_HEADER = "data:text/html;base64,{0}"
FOLDER_TEMPLATES = "kimp_templates"
# ^ Put templates in this folder. Templates should follow Python formatting string convention.

# The list of templates to use.
templates = {}

# Generate list of templates.
template_listing = os.listdir(FOLDER_TEMPLATES)
for filename in template_listing:
    path = os.path.join(FOLDER_TEMPLATES, filename)
    if os.path.isfile(path):
        with open(path) as f:
            try:
                templates[filename.split(".")[0]] = f.read()
            except:
                pass

def mogrify(template, *arguments):
    """
    This loads a template and creates a meme out of it. Returns None if it doens't work right.
    
    template - The key of the template desired.
    *arguments - The formatting arguments to use.
    """
    result = templates[template].format(*arguments)
    return HTML_HEADER.format(base64.b64encode(result.encode()).decode("ascii"))
