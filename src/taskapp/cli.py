import sys, os
from types import ModuleType
from typing import Any, Callable
from taskapp.console import console
from taskapp.project import Route, Runner, parse_project, Project
from pathlib import Path
import importlib.util

# TODO: Handle nested routes with the same name

class CliRunner(Runner):
    modules: dict[str, ModuleType]
    project: Project
    prelude: Callable | None

    def __init__(self) -> None:
        self.modules = {}
        self.prelude = None

        tasks_path = Path("tasks.py")
        if tasks_path.is_file():
            spec = importlib.util.spec_from_file_location("taskroot", "tasks.py")

            if spec == None:
                raise Exception("Couldn't generate module spec!")

            module = importlib.util.module_from_spec(spec)
            sys.modules["taskroot"] = module
            spec.loader.exec_module(module)  # type: ignore

            if hasattr(module, "prelude"):
                prelude = getattr(module, "prelude")
                if not callable(prelude):
                    console.log("[red bold] project prelude should be callable")
                self.prelude = prelude

    
    def init_prelude(self):
        if not self.prelude:
            return
        
        try:
            self.prelude()
        except Exception as e:
            console.print("[bold red]Encountered an error in prelude:")
            console.print(e.args[0])
            return False

    def run(
        self,
        project: Project,
        params: dict[str, Any],
        matched: Route,
        wild_matches: list[str],
    ) -> Any:
        cwd = os.getcwd()
        path = os.path.join(cwd, *matched.path[:-1])
        path = os.path.join(path, matched.path[len(matched.path) - 1] + ".py")

        module_name = ".".join(["taskroot"] + matched.path[1:])

        if self.modules.get(module_name) == None:
            console.print(f'[grey42]Loading module at path: "{path}"...')

            spec = importlib.util.spec_from_file_location(module_name, path)

            if spec == None:
                raise Exception("Couldn't generate module spec!")

            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)  # type: ignore
            self.modules[module_name] = module
        else:
            module = self.modules[module_name]

        console.print(f"[cyan]Running task: [bold]{matched.name}")
        method_name = f"taskapp${module_name}${matched.name}"

        if len(matched.identifier) > 0:
            method_name = f"taskapp${module_name}$" + ".".join(matched.identifier)

        if hasattr(module, method_name) and callable(getattr(module, method_name)):
            execution_result = getattr(module, method_name)(
                project, params, module_name, *wild_matches
            )
            if execution_result:
                console.print(f'[bold]Execution result[/bold]: "{execution_result}"')
                return execution_result
        else:
            console.print("[bold red]Couldn't find task declaration!")
        pass


def main():
    args = sys.argv[1:]
    computed_args = []
    params = {}

    for arg in args:
        if arg.startswith("--"):
            parts = arg[2:].split("=")
            key = parts[0]

            if len(parts) == 1:
                value = True
            else:
                value = parts[1]
            params[key] = value
        else:
            computed_args += [arg]

    cwd = os.getcwd()

    runner = CliRunner()
    project_data = parse_project(cwd)
    project = Project(project_data, runner)
    runner.project = project

    console.print(
        f'[bold]Running the Task Apparatus on the [blue]"{project.name}"[/blue] project'
    )

    if runner.init_prelude() == False:
        console.print("[red]Aborting execution.")
    else:
        project.execute(computed_args, params)


if __name__ == "__main__":
    main()
