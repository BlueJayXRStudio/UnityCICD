import subprocess

# Please run from this directory
result = subprocess.run(
    ["python3", "build.py"],
    # capture_output=True,
    # check=True,
    text=True,
    cwd="../MacOS"
)

# print(result.stdout)