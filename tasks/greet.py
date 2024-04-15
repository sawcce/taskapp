from taskapp import task

@task("wildcard")
def wildcard(name: str): return affirmative(name)

@task("wildcard.affirmative")
def affirmative(name: str):
    return f"Hello, {name}."

@task("wildcard.excited")
def excited(name: str):
    return f"Hello, {name}!"

@task("wildcard.unsure")
def unsure(name: str):
    return f"Hello, {name}?"