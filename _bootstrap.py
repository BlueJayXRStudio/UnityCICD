import sys, os
current = os.path.dirname(os.path.abspath(__file__))
# print("bootstrapping from: ", current)
marker = ".is_project_root"
project_root = None
while True:
    marker_path = os.path.join(current, marker)
    if os.path.isfile(marker_path):
        project_root = current
        break
    next = os.path.dirname(current)
    if next == current:
        sys.exit(1)
    current = next

def safe_commonpath(paths):
    try:
        return os.path.commonpath(paths)
    except ValueError:
        return None

sys.path = [
    p for p in sys.path if 
    ("venv" in p and "site-packages" in p) or 
    safe_commonpath([project_root, os.path.abspath(p)]) != project_root
]
sys.path.append(project_root)

from Tools.path_tools import PathTools
project_resolver = PathTools(project_root)