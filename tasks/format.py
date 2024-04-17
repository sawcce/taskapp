import glob
from pathlib import Path
from taskapp import run
from taskapp.task import Prelude, prelude, task


@prelude(name="all")
def all_prelude():
    files = glob.glob("src/**/*.py")
    routes = list(map(lambda file: f"format {file}", files))

    return Prelude(routes=routes)


@task(name="all")
def phony():
    pass

@prelude(name="wildcard")
def wildcard_prelude(file: str):
    return Prelude(dependencies=[file])

@task(name="wildcard")
def wildcard(file: str):
    run("python", "-m", "black", file)