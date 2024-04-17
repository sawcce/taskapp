from taskapp.task import task

@task("greet")
def greet():
    return "Hello Taskapp user."