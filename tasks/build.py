from taskapp import task, run

@task(name="build")
def build():
    run("python", "-m", "build")