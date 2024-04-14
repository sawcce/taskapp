import subprocess

def run(command: str, *args: str):
    subprocess.run([command, *args]) 

