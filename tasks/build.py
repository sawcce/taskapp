from taskapp import run
from taskapp.task import Fail, Glob, task

@task(name="build", prelude=Glob("src/**/*.py", "pyproject.toml"))
def build():
    run("python", "-m", "build")