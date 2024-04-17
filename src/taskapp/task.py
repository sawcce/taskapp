import sys
from typing import Any, Self

from taskapp import get_full_task_name, get_task_meta, set_task_meta


class Prelude:
    dependencies: list[str] = []
    """File dependencies associated with this prelude"""
    fail: Any | None = None
    """If not set to None, this field indicates that the 
        prevents the task from executing. This field 
        shoud contain the reason of the fail."""   
    
    def __init__(self, reason: Any | None = None) -> None:
        self.fail = reason
    
def Fail(reason: Any): # type: ignore
    return Prelude(reason)

def prelude(name: str):
    def wrapper(definition):
        set_task_meta(name, "prelude", definition)
        return definition
    return wrapper

def task(name: str, dir: str | None = None, prelude: list[str] | None = None):
    """
        A decorator to define a task, the actual function name is meaningless.  \n
        name: corresponds to the task name. \n
        dir: specifies the `cwd` used by taskapp methods (like `run`) when executing the task. \n
        prelude: a list of routes that need to be called before this task is ran
    """
    def wrapper(definition):
        f = list(sys._current_frames().values())[0]
        if f.f_back == None:
            raise Exception("Expected module name")

        module_name = f.f_back.f_globals["__name__"]
        tn = get_full_task_name(module_name, name)

        set_task_meta(name, 'cwd', dir)

        if prelude:
            set_task_meta(name, 'cwd', lambda *args: prelude)

        def wrapped(module_name, *args):
            old_meta = sys.modules["taskapp"].current_meta
            task_meta = get_task_meta(name, module_name=module_name)
            sys.modules["taskapp"].current_meta =  task_meta# type: ignore

            if (prelude := task_meta.get("prelude")) != None:
                prelude_result = prelude(*args)
                if isinstance(prelude_result, Prelude):
                    if prelude_result.fail != None:
                        print(f"Couldn't execute task because: {prelude_result.fail}")
                        sys.modules["taskapp"].current_meta = old_meta # type: ignore
                        return
                    if len(prelude_result.dependencies) > 0:
                        print(f"[TODO] Task dependencies: {prelude_result.dependencies}")
                elif prelude_result == None:
                    pass

            result = definition(*args)

            sys.modules["taskapp"].current_meta = old_meta # type: ignore
            return result

        setattr(sys.modules[module_name], tn, wrapped)

        return lambda x: None
    return wrapper