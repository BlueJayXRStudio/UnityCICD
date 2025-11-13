import os
import hashlib
import json
from io import StringIO

def hash_file(path, algo="sha256", chunk_size=1024*1024):
    hash_obj = getattr(hashlib, algo)()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()

def hash_string_stream(_str, algo="sha256", chunk_size=1024*1024):
    hash_obj = getattr(hashlib, algo)()
    stream = StringIO(_str)
    while True:
        chunk = stream.read(chunk_size)
        if not chunk:
            break
        hash_obj.update(chunk.encode("utf-8"))
    return hash_obj.hexdigest()

def save_hashes(path, hashes):
    with open(path, 'w') as f:
        json.dump(list(hashes), f)

def load_hashes(path):
    with open(path, 'r') as f:
        res = set(json.load(f))
    return res

def rebuild_hashes(dir, output_path, algo="sha256", chunk_size=1024*1024):
    hashes = set()
    for item in os.listdir(dir):
        path = os.path.join(dir, item)
        if os.path.isfile(path):
            hashes.add(hash_file(path, algo, chunk_size))
    save_hashes(output_path, hashes)

