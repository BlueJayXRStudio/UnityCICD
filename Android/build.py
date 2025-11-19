import sys, os, _bootstrap
from Validation.VersionValidation.version_validation import simple_increment_version
from Tools.ref_container import RefContainer
from dotenv import load_dotenv
import yaml
import subprocess

PROJECT_DIR = _bootstrap.project_resolver
load_dotenv(PROJECT_DIR.join("envs/paths.env").path)
load_dotenv(PROJECT_DIR.join("envs/secrets.env").path)

with open(PROJECT_DIR.join("Android/store_deployment_data/version_info.yml").path) as f:
    config = yaml.safe_load(f)

ref_container = RefContainer()
simple_increment_version(config["version_code"], ref_container)

if not ref_container.item:
    sys.exit(1)

result = subprocess.run(
    [
        os.getenv("UNITY_PATH"),
        "-batchMode", "-quit",
        "-projectPath", os.getenv("PROJECT_PATH_ANDROID"),
        "-executeMethod", "AndroidBuildCommand.BuildAndroidApp",
        f"buildPath={PROJECT_DIR.join("Android/builds/app.apk").path}",
        f"KeystoreName={os.getenv("KeystoreName")}",
        f"KeystorePass={os.getenv("KeystorePass")}",
        f"KeyaliasName={os.getenv("KeyaliasName")}",
        f"KeyaliasPass={os.getenv("KeyaliasPass")}",
        f"VersionCode={ref_container.item}",
        f"BundleCode={int(config["bundle_code"])+1}"
    ],
    # capture_output=True,
    # check=True,
    text=True
)

sys.exit(result.returncode)