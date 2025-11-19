import sys, os, _bootstrap
from Tools.path_tools import PathTools
from dotenv import load_dotenv
from Tools.parsers.indentation_formatter import indentation_formatter

PROJECT_DIR = _bootstrap.project_resolver
load_dotenv((PROJECT_DIR / "envs/paths.env").path)

with open(PROJECT_DIR.join("Android/store_deployment_data/patchnotes.txt").path, 'r') as f:
    patch_notes = f.read()

with open(os.getenv("PATCH_NOTES_PATH"), 'w') as f:
    f.write(indentation_formatter(patch_notes))

print("Patch notes updated!")
sys.exit(0)