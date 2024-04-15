import subprocess
import sys
from typing import Any

current_meta: dict[str, Any] = {}

def get_meta():
    return current_meta

def get_cwd():
    return current_meta.get("cwd") 

def run(command: str, *args: str):
    subprocess.run([command, *args], shell=True, cwd=get_cwd())

def task(name: str, dir: str | None = None):
    """
        A decorator to define a task, the actual function name is meaningless.  \n
        name: corresponds to the task name. \n
        dir: specifies the `cwd` used by taskapp methods (like `run`) when executing the task. \n
    """
    def wrapper(definition):
        f = list(sys._current_frames().values())[0]
        if f.f_back == None:
            raise Exception("Expected module name")

        module_name = f.f_back.f_globals["__name__"]
        tn = f"taskapp${module_name}${name}"

        meta = {}
        setattr(sys.modules[module_name], f"{tn}.meta", meta)

        if dir:
            meta['cwd'] = dir

        def wrapped(*args):
            old_meta = sys.modules["taskapp"].current_meta
            sys.modules["taskapp"].current_meta = meta # type: ignore
            result = definition(*args)
            sys.modules["taskapp"].current_meta = old_meta # type: ignore
            return result

        setattr(sys.modules[module_name], tn, wrapped)

        return lambda x: None
    return wrapper