import sys, os
from taskapp.project import parse_project, Project 
import importlib.util


def main():
    args = sys.argv[1:]
    print(args)
    cwd = os.getcwd()

    project_data = parse_project(cwd)
    project = Project(project_data)
    matched = project.match(args)

    print(f'Running the Task Apparatus on the "{project.name}" project')

    # TODO: Handle catch routes
    if matched:
        # This means we're calling the route 'anonymously', e.g.
        # test route => test route route
        if len(args) != len(matched.path) + len(matched.identifier):
            raise Exception("Wrong amount of arguments!")

        path = os.path.join(cwd, "tasks", *matched.path[:-2])
        path = os.path.join(path, matched.path[len(matched.path) - 1] + ".py")

        print(f'Loading module at path: "{path}"...')

        spec = importlib.util.spec_from_file_location(".".join(matched.path[:-1]), path)

        if spec == None:
            raise Exception("Couldn't generate module spec!")
            
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module) # type: ignore

        method_name = matched.name

        if len(matched.identifier) > 0:
            method_name = "_".join(matched.identifier)

        if hasattr(module, method_name) and callable(getattr(module, method_name)):
            execution_result = getattr(module, method_name)()
            if execution_result:
                print("Task yielded:")
                print(execution_result)
            else:
                print("Task yielded no result")
    else:
        print(f"Description: {project.description}")
        print("Available commands:")
        for route in project.routes:
            print(f"-> {route.name}")


if __name__ == "__main__":
    main()
