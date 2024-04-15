from yaml import load, Loader
from os import path
import pprint

def parse_project(root: str):
    project_path = path.join(root, "task.app.yaml")

    with open(project_path) as file:
        yaml_contents = file.read()
    
    project = load(yaml_contents, Loader=Loader)
    return project


def parse_route_name(name: str):
    try:
        start = name.index("(")
        end = name.index(")")
        data = {}

        args = name[start+1:end].split(",")

        for arg in args:
            split = list(map(lambda x: x.strip(), arg.split(":")))
            if len(split) == 1 and split[0] == "!":
                data[arg] = False
            elif len(split) == 1:
                data[arg] = True
            else:
                data[arg[0]] = split[1]

        return (name[:start], data)
    except ValueError:
        return (name, {})

class Route:
    name: str
    path: list[str]
    identifier: list[str]
    caught: bool = False
    wildcard: bool = False
    standalone: bool = False
    """Means that the route can be called without any subroute"""
    catch: bool = False
    """Dictates whether or not this route is a file or directory"""
    subroutes: list["Route"]

    def init_basic(self, route_data, root: list[str] = ["tasks"], caught: bool = False, identifier: list[str] = []):
        name, data = parse_route_name(route_data)
        if name == "*":
           self.wildcard = True 
        self.name = name
        self.__dict__.update(data)

        if caught and self.caught:
            raise Exception("A caught route whos parents catches is redundant")
        elif caught or self.caught:
            self.path = root
            self.identifier = identifier + [name]
        else:
            self.path = root + [name]

    def init_composite(self, route_data, root: list[str] = ["tasks"], caught: bool = False, identifier: list[str] = []):
        items = list(route_data.items())
        name, data = parse_route_name(items[0][0])
        self.name = name
        self.__dict__.update(data)

        if len(items) != 1:
            raise Exception("Wrong amount of items")
        
        if self.catch and caught:
            raise Exception("Cannot have nested catch routes!")
        elif self.caught:
            raise Exception("A caught route cannot have subroutes!")
        elif self.catch:
            self.path = root + [name]
            root = root[:] + [name]
        elif caught:
            self.path = root[:]
            # self.path[len(self.path) - 1].append(name)
            self.identifier = identifier + [name]
            identifier = self.identifier
        else:
            self.path = root + [name]
            root = self.path

        for subroute in items[0][1]:
            self.subroutes += [Route(subroute, root=root, caught=self.catch or caught, identifier=identifier)]

    def __init__(self, route_data, root: list[str] = ["tasks"], caught: bool = False, identifier: list[str] = []) -> None:
        self.subroutes = []
        self.identifier = []

        if isinstance(route_data, str):
            self.init_basic(route_data, root, caught, identifier)
        elif isinstance(route_data, dict):
            self.init_composite(route_data, root, caught, identifier)

    def __repr__(self) -> str:
        return pprint.pformat(self.__dict__)

class Project:
    name: str
    description: str
    routes: list[Route]

    def __init__(self, project_data):
        self.name = project_data["name"]
        self.description = project_data["description"]
        self.routes = []

        for route_data in project_data["routes"]:
            self.routes.append(Route(route_data))
    
    def match(self, args, routes = None, nest_level: int = 0):
        if len(args) == 0:
            return None
        if routes == None:
            routes = self.routes

        for route in routes:
            if args[0] == route.name:
                if len(args) == 1:
                    return route
                result = self.match(args[1:], route.subroutes, nest_level + 1)

                if result:
                    return result