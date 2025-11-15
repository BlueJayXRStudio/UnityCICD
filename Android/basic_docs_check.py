"""
Very unstable. Don't use. Explore higher parameter models or fine-tuned models.
"""
import requests
from pathlib import Path

this_file = Path(__file__).resolve()

with open(this_file.parent / "store_deployment_data" / "patchnotes.txt", 'r') as f:
    response = requests.post(
        "http://localhost:8500/check",
        json={"text": f"Here's the document I want you to inspect:\n\n{f.read()}"}
    )
print(response.text)