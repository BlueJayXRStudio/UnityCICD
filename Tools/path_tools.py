import os, _bootstrap

def scanfiles(dir):
    """ Generate file paths for given directory (non-recursive) """
    for item in os.listdir(dir):
        path = os.path.join(dir, item)
        if os.path.isfile(path):
            yield path

def scandirs(dir):
    """ Generate directory paths for given directory (non-recursive) """
    for item in os.listdir(dir):
        path = os.path.join(dir, item)
        if os.path.isdir(path):
            yield path

class PathTools:
    """ A minimal take on pathlib """
    def __init__(self, path):
        self.path = path # keep unresolved
    
    def resolved(self):
        return PathTools(os.path.abspath(self.path))

    def preview_join_resolved(self, path):
        return os.path.abspath(os.path.join(self.path, path))
    
    def preview_join(self, path):
        return os.path.join(self.path, path)
    
    def join(self, path):
        return PathTools(os.path.join(self.path, path))
    
    def join_path(self, _path_tools: PathTools):
        return PathTools(os.path.join(self.path, _path_tools.path))

    def parent(self):
        return PathTools(os.path.dirname(self.path))

    def __str__(self):
        return self.path
    
    def __truediv__(self, other):
        return self.join(other)

