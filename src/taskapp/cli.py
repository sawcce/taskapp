import sys, os
from typing import Any
from taskapp.project import Route, Runner, parse_project, Project
import importlib.util


class CliRunner(Runner):
    def __init__(self) -> None:
        pass

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

        print(f'Loading module at path: "{path}"...')

        module_name = ".".join(["taskroot"] + matched.path[1:])
        spec = importlib.util.spec_from_file_location(module_name, path)

        if spec == None:
            raise Exception("Couldn't generate module spec!")

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)  # type: ignore

        method_name = f"taskapp${module_name}${matched.name}"

        if len(matched.identifier) > 0:
            method_name = f"taskapp${module_name}$" + ".".join(matched.identifier)

        if hasattr(module, method_name) and callable(getattr(module, method_name)):
            execution_result = getattr(module, method_name)(
                project, params, module_name, *wild_matches
            )
            if execution_result:
                print("Task yielded:")
                print(execution_result)
                return execution_result
            else:
                print("Task yielded no result")
        else:
            print("Couldn't find task declaration!")
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

    print(f'Running the Task Apparatus on the "{project.name}" project')
    project.execute(computed_args, params)


if __name__ == "__main__":
    main()
