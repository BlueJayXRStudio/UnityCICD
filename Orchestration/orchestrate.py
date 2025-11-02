# WIP: Integrating Android build and automatic deploy to Meta Horizon alpha channel
import subprocess

# Please run from this directory
result = subprocess.run(
    ["python", "build.py"],
    # capture_output=True,
    # check=True,
    text=True,
    cwd="../MacOS"
)

# print(result.stdout)