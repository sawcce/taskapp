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


def get_module_name(level: int) -> str:
    f = list(sys._current_frames().values())[0]
    back = f
    for _ in range(level):
        if back.f_back == None:
            raise Exception(f"Couldn't retrieve module name with {level=}")

        back = back.f_back
    return back.f_globals["__name__"]


def get_full_task_name(module: str, task_name: str) -> str:
    return f"taskapp${module}${task_name}"


def set_task_meta(task_name: str, key: str, value: Any):
    module_name = get_module_name(level=3)
    module = sys.modules[module_name]
    full_task_name = get_full_task_name(module_name, task_name)
    meta_key = full_task_name + ".meta"

    if hasattr(module, meta_key):
        meta = getattr(module, meta_key)
        meta[key] = value
    else:
        setattr(module, meta_key, {key: value})


def get_task_meta(task_name: str, level: int = 3, module_name: str | None = None):
    if module_name == None:
        module_name = get_module_name(level)

    module = sys.modules[module_name]
    full_task_name = get_full_task_name(module_name, task_name)
    meta_key = full_task_name + ".meta"

    if hasattr(module, meta_key):
        return getattr(module, meta_key)
    else:
        return {}
