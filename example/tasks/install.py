from taskapp.task import task

# the task decorator does some work behind the scenes
# to allow the use of a different function name
# Feel free to look at the documentation of task
# as the parameters are explained there
@task(name="local")
def local_install():
    print("Installing locally!")

@task(name="system")
def system_install():
    print("Installing system-wide")