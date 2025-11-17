import sys, os, _bootstrap
from tkinter import Tk, filedialog
from Tools.path_tools import PathTools

project_resolver = PathTools(_bootstrap.project_root)

root = Tk()
root.withdraw()
root.update()
workflow = filedialog.askopenfilename(
    title="Select a file",
    initialdir=project_resolver.preview_join_resolved("Orchestration"),
    filetypes=[("Text files", "*.yml"), ("All files", "*.*")]
)

def terminate(status):
    root.destroy()
    sys.exit(status)

if workflow:
    base, ext = os.path.splitext(workflow)
    if ext == ".yml":
        print(workflow)
        terminate(0)
terminate(1)
