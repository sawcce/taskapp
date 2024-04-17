"""A simple translation script. Available translation are Bread, Coffee and Water"""

from taskapp.task import task, prelude, Fail

items = ["Bread", "Coffee", "Water"]

translations = {
    'Bread': ["Pain"],
    'Coffee': ["Café"],
    'Water': ["Eau"],
}

@task("translate")
def list_items():
    return items

@prelude("wildcard")
def wildcard_prelude(item: str):
    if not item in items:
        reason = f"Item {item} doesn't have a translation"
        return Fail(reason)

@task("wildcard")
def wildcard(item: str):
    return translations[item]