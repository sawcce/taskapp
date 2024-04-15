from taskapp import task


@task("affirmative")
def type1(name: str):
    return f"Hello, {name}!"