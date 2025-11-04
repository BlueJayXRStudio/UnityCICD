import os
import subprocess
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)

processes = [
    subprocess.Popen(
        ["python", os.path.join(PARENT_DIR, "MacOS/build.py")],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    ),
    subprocess.Popen(
        ["python", os.path.join(PARENT_DIR, "Android/adb_deploy.py")],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    ),
]

for i, p in enumerate(processes):
    stdout, _ = p.communicate()  # waits + reads safely
    print(f"Process {i} exited with code {p.returncode} \n")
    print(stdout)