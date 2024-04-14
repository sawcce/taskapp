"""
    Handles the process of installing the package for dev purposes
"""

from taskapp import run

def local():
    """Installs the cli and package locally using pip"""
    run("pip", "install", "-e", ".")

def local_demo():
    """Demonstrates nested routes in a 'catch' route"""
    return "Hey!"