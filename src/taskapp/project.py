from pathlib import Path
from typing import Any, Callable
from yaml import dump, load, Loader
from os import path
import pprint
from taskapp.console import console
from rich.prompt import Prompt
import semver


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

        args = name[start + 1 : end].split(",")

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

    def init_basic(
        self,
        route_data,
        root: list[str] = ["tasks"],
        caught: bool = False,
        identifier: list[str] = [],
    ):
        name, data = parse_route_name(route_data)
        if name == "*":
            name = "wildcard"
            self.wildcard = True

        self.name = name
        self.__dict__.update(data)

        if caught and self.caught:
            raise Exception("A caught route whos parents catches is redundant")
        elif caught or self.caught or self.wildcard:
            self.path = root
            self.identifier = identifier + [name]
        else:
            self.path = root + [name]

    def init_composite(
        self,
        route_data,
        root: list[str] = ["tasks"],
        caught: bool = False,
        identifier: list[str] = [],
    ):
        items = list(route_data.items())
        name, data = parse_route_name(items[0][0])
        if name == "*":
            name = "wildcard"
            self.wildcard = True
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
            self.subroutes += [
                Route(
                    subroute,
                    root=root,
                    caught=self.catch or caught,
                    identifier=identifier,
                )
            ]

    def __init__(
        self,
        route_data,
        root: list[str] = ["tasks"],
        caught: bool = False,
        identifier: list[str] = [],
    ) -> None:
        self.subroutes = []
        self.identifier = []

        if isinstance(route_data, str):
            self.init_basic(route_data, root, caught, identifier)
        elif isinstance(route_data, dict):
            self.init_composite(route_data, root, caught, identifier)

    def __repr__(self) -> str:
        return pprint.pformat(self.__dict__)


class Runner:
    def run(
        self,
        project: "Project",
        params: dict[str, Any],
        match: Route,
        wild_matches: list[str],
    ):
        pass


class Project:
    name: str
    description: str
    routes: list[Route]
    runner: Runner
    cache_path: str = "taskapp.cache.yaml"
    cache: dict[str, Any]

    def __init__(self, project_data, runner: Runner):
        self.name = project_data["name"]
        self.description = project_data["description"]
        self.routes = []
        self.runner = runner
        self.init_cache()

        for route_data in project_data["routes"]:
            self.routes.append(Route(route_data))

    def init_cache(self):
        file_path = Path(self.cache_path)

        if not file_path.is_file():
            self.cache = cache_template()
        else:
            self.cache = load(file_path.read_text(), Loader)

    def match(
        self, args, routes=None, level: int = 0, wild_matches: list[str] = []
    ) -> tuple[Route, list[str]] | None:
        if len(args) == 0:
            return None
        if routes == None:
            routes = self.routes

        for route in routes:
            if args[0] == route.name or route.wildcard:
                if route.wildcard:
                    wild_matches = wild_matches[:] + [args[0]]

                if len(args) == 1:
                    return route, wild_matches
                result = self.match(args[1:], route.subroutes, level + 1, wild_matches)

                if result:
                    return result

    def execute(self, route: str | list[str], params: dict[str, Any]):
        args = route

        if isinstance(route, str):
            args = route.split(" ")

        matched = self.match(args)
        if matched:
            matched, wild_matches = matched
            self.runner.run(self, params, matched, wild_matches)
            if len(args) != len(matched.path) + len(matched.identifier) - 1:
                raise Exception("Wrong amount of arguments!")
        else:
            console.print(f"Description: {self.description}")
            console.print("Available root commands:")
            for av_route in self.routes:
                console.print(f"-> {av_route.name}")

    def get_children(self):
        return self.routes

    def get_value(self):
        return "Project"

    def get_cache(self):
        return self.cache

    def write_cache(self):
        file_path = Path(self.cache_path)
        file_path.write_text(dump(self.cache))

    def cached_last_modification(
        self, module_name: str, task_name: str, path: str
    ) -> int | None:
        data = self.cache["files"].get(f"{module_name}::{task_name}:{path}")
        if data == None:
            self.cache_modification(
                module_name, task_name, path, last_modification(path)
            )

        return data

    def cache_modification(
        self, module_name: str, task_name: str, path: str, time: float | int
    ):
        self.cache["files"][f"{module_name}::{task_name}:{path}"] = time

    def cache_data(self):
        if (d := self.cache.get("data")) != None:
            return d
        self.cache["data"] = {}
        return self.cache["data"]

    def cached_or_prompt(
        self,
        key: str,
        message: str,
        options: list[str],
        post_message: Callable | None = None,
        force: bool = False,
    ):
        val = self.cache_data().get(key)
        if val != None and not force:
            return val

        choice = Prompt.ask(message, choices=options, show_default=True)
        self.cache_data()[key] = choice

        if post_message != None:
            console.print(post_message(choice))

        return choice


class Version:
    version: semver.Version

    def __init__(self, version: str) -> None:
        self.version = semver.Version.parse(version, True)

    def matches(self, other: "Version", op: str):
        diff = other.version.compare(self.version)
        match op:
            case "=":
                return diff == 0
            case ">=":
                return diff >= 0
            case "<=":
                return diff <= 0
            case ">":
                return diff > 0
            case "<":
                return diff < 0


class PackageSpec:
    names: list[str]
    version: Version
    parameters: dict[str, Any]


def cache_template():
    return {"files": {}, "data": {}}


# TODO: Optimize cache
default_cache_path = "taskapp.cache.yaml"


def last_modification(path: str) -> int:
    file_path = Path(path)
    return file_path.stat().st_mtime_ns
