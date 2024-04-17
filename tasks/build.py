from taskapp import run
from taskapp.task import task

@task(name="build")
def build():
    run("python", "-m", "build")