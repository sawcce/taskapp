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


def get_full_task_name(module: str, task_name: str) -> str:
    return f"taskapp${module}${task_name}"


def set_task_meta(module_name: str, task_name: str, key: str, value: Any):
    module = sys.modules[module_name]
    full_task_name = get_full_task_name(module_name, task_name)
    meta_key = full_task_name + ".meta"

    if hasattr(module, meta_key):
        meta = getattr(module, meta_key)
        meta[key] = value
    else:
        setattr(module, meta_key, {key: value})


def get_task_meta(task_name: str, module_name: str):
    module = sys.modules[module_name]
    full_task_name = get_full_task_name(module_name, task_name)
    meta_key = full_task_name + ".meta"

    if hasattr(module, meta_key):
        return getattr(module, meta_key)
    else:
        return {}

def matches_semver(op: str, compare_result: int):
    match op:
        case "=":
            return compare_result == 0
        case ">=":
            return compare_result >=0
        case "<=":
            return compare_result <= 0
        case ">":
            return compare_result > 0
        case "<":
            return compare_result < 0