"""A simple translation script. Available translation are Bread, Coffee and Water"""

from taskapp import task

items = ["Bread", "Coffee", "Water"]

translations = {
    'Bread': ["Pain"],
    'Coffee': ["Café"],
    'Water': ["Eau"],
}

@task("translate")
def list_items():
    return items

@task("wildcard")
def wildcard(item: str):
    return translations[item]