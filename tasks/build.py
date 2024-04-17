from taskapp import run
from taskapp.task import Fail, Glob, task

@task(name="build", prelude=Glob("src/**/*.py"))
def build():
    run("python", "-m", "build")