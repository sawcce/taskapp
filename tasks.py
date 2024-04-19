from taskapp.project import Project
from taskapp.task import task
from taskapp.tools.pip import Pip
from taskapp.tools.node import Node


@task("greet")
def greet():
    return "Hello Taskapp user."


def prelude(project: Project):
    Pip().patch()
    # node example (unnecessary for this project)
    # Node().requires("19", ">=").requires("8", "<=").patch(project)
