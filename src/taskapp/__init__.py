import pprint
import subprocess
import sys
import inspect

def run(command: str, *args: str):
    subprocess.run([command, *args]) 

def task(name: str):
    def wrapper(definition):
        f = list(sys._current_frames().values())[0]
        if f.f_back == None:
            raise Exception("Expected module name")

        module_name = f.f_back.f_globals['__name__']
        tn = f"taskapp${module_name}${name}"
        setattr(sys.modules[module_name], tn, definition)
        return definition
    return wrapper