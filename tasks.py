from taskapp.task import task
from taskapp.tools.pip import Pip


@task("greet")
def greet():
    return "Hello Taskapp user."


def prelude():
    Pip().requires("20", "=").patch()
