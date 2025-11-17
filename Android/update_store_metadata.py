import sys, os, _bootstrap
from Tools.path_tools import PathTools
from Tools.ref_container import RefContainer
from Validation.VersionValidation.version_validation import simple_increment_version
import yaml

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
base_resolver = PathTools(BASE_DIR)

current_store_metadata = None
with open(base_resolver.preview_join_resolved("store_deployment_data/version_info.yml"), "r") as f:
    current_store_metadata = yaml.safe_load(f)

ref_container = RefContainer()
simple_increment_version(current_store_metadata["version_code"], ref_container)
if not ref_container.item:
    sys.exit(1)

current_store_metadata["version_code"] = ref_container.item
current_store_metadata["bundle_code"] = current_store_metadata["bundle_code"] + 1

with open(base_resolver.preview_join_resolved("store_deployment_data/version_info.yml"), "w") as f: 
    yaml.safe_dump(current_store_metadata, f)

sys.exit(0)