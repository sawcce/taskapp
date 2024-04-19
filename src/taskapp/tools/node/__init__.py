import subprocess
import semver
from taskapp import matches_semver
from taskapp.project import Project
from taskapp.console import console


class Node:
    vm: str
    requirements: list[tuple[semver.Version, str]]

    def __init__(self) -> None:
        self.requirements = []

    def requires(self, version: str, op: str = "="):
        self.requirements.append((semver.Version.parse(version, True), op))
        return self


    def patch(self, project: Project):
        self.vm = project.cached_or_prompt(
            "node-tools-node-vm",
            "Which node version manager would you like to use?",
            ["none", "nvm", "nvs"],
            lambda x: f"You chose {x} as your node version manager, you can always change it in yaskapp.cache.yaml in data.node-tools-node-vm.",
        )

        versions = self.get_versions_list() or []

        for version, op in self.requirements:
            has_match = False

            for av in versions:
                compare = av.compare(version)

                if matches_semver(op, compare) :
                    has_match = True
                
                if not has_match:
                    raise Exception(f"[bold red]* node requirement {op} {version} not met!")

        console.print(f"[green]* node requirements met!")


    
    def get_versions_list(self):
        match self.vm:
            case "none":
                return fetch_node_version()
            case "nvs":
                return fetch_nvs_versions()
            case "nvm":
                return fetch_nvm_versions()
    

def fetch_node_version():
    v = subprocess.run("node --version", shell=True, capture_output=True).stdout.decode()
    vs = v.strip()[1:]

    return [semver.Version.parse(vs, True)]

def fetch_nvs_versions():
    vs = subprocess.run("nvs list", shell=True, capture_output=True).stdout.decode().strip()
    vsl = vs.split("\n")
    versions: list[semver.Version] = []

    for l in vsl:
        l = l.strip()
        start = l.index("/") + 1
        end = l.index("/", start)
        versions.append(semver.Version.parse(l[start:end].strip()))
    
    return versions

def fetch_nvm_versions():
    vs = subprocess.run("nvm list", shell=True, capture_output=True).stdout.decode().strip()
    vsl = vs.split("\n")
    return list(map(lambda x: semver.Version.parse(x.strip(), True), vsl))