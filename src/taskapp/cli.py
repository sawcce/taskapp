import sys, os
from taskapp.project import parse_project, Project 
import importlib.util


def main():
    args = sys.argv[1:]
    cwd = os.getcwd()

    project_data = parse_project(cwd)
    project = Project(project_data)
    matched = project.match(args)
    print(matched)

    print(f'Running the Task Apparatus on the "{project.name}" project')

    # TODO: Handle catch routes
    if matched:
        matched, wild_matches = matched

        if len(args) != len(matched.path) + len(matched.identifier) - 1:
            raise Exception("Wrong amount of arguments!")

        path = os.path.join(cwd, *matched.path[:-1])
        path = os.path.join(path, matched.path[len(matched.path) - 1] + ".py")

        print(f'Loading module at path: "{path}"...')

        module_name = ".".join(["taskroot"] + matched.path[1:])
        spec = importlib.util.spec_from_file_location(module_name, path)

        if spec == None:
            raise Exception("Couldn't generate module spec!")
            
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module) # type: ignore

        print(matched)
        print(module_name)

        method_name = f"taskapp${module_name}${matched.name}"
        print(method_name)

        if len(matched.identifier) > 0:
            method_name = f"taskapp${module_name}$" + ".".join(matched.identifier)

        if hasattr(module, method_name) and callable(getattr(module, method_name)):
            execution_result = getattr(module, method_name)(*wild_matches)
            if execution_result:
                print("Task yielded:")
                print(execution_result)
            else:
                print("Task yielded no result")
        else:
            print("Couldn't find task declaration!")

    else:
        print(f"Description: {project.description}")
        print("Available commands:")
        for route in project.routes:
            print(f"-> {route.name}")


if __name__ == "__main__":
    main()
