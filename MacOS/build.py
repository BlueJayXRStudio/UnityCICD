import subprocess
import sys

result = subprocess.run(
    ["python3", "test.py"],
    capture_output=True,
    # check=True,
    text=True
)

if result.returncode == 0:
    result = subprocess.run(
        ["/usr/bin/env", "bash", "build_script"],
        capture_output=True,
        # check=True,
        text=True
    )
    if result.returncode == 0:
        print("build successful")
        sys.exit(0)
sys.exit(1)
