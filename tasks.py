from taskapp import task


@task("greet")
def greet():
    return "Hello Taskapp user!"