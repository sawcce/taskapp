import subprocess
from taskapp import matches_semver
from taskapp.console import console
import re
import semver
import pip

class Pip:
    requirement: tuple[semver.Version, str] | None = None

    def __init__(self) -> None:
        pass

    def requires(self, version: str, requirement: str = "=") -> "Pip":
        self.requirement = semver.Version.parse(version, True), requirement
        return self
    
    def patch(self):
        version = semver.Version.parse(pip.__version__,True)

        if not self.requirement:
            console.print(f"[green]* pip requirement met!")
            return True
        
        compare = version.compare(self.requirement[0])
        matches = matches_semver(self.requirement[1], compare)

        if matches:
            console.print(f"[green]* pip requirement {self.requirement[1]} {self.requirement[0]} met!")
        else:
            raise Exception(f"[red bold]* pip requirement {self.requirement[1]} {self.requirement[0]} not met!")
