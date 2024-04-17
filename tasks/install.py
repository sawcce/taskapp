"""
    Handles the process of installing the package for dev purposes
"""

from taskapp import run
from taskapp.task import task

@task(name="local")
def local():
    """Installs the cli and package locally using pip"""
    run("pip", "install", "-e", ".")

@task(name="local.demo")
def demo():
    """Demonstrates nested routes in a 'catch' route"""
    return "Hey!"

@task(name="wildcard")
def wildcard(match: str):
    return match