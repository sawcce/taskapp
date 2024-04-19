from taskapp.project import Project
from taskapp.task import task
from taskapp.tools.pip import Pip


@task("greet")
def greet():
    return "Hello Taskapp user."


def prelude(project: Project):
    Pip().requires("20", "=").patch()
