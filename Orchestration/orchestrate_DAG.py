import sys, os, _bootstrap
import subprocess, threading, time
from Tools.path_tools import PathTools
import yaml
from collections import defaultdict, deque
from Orchestration.check_cycles import CheckCycles

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
WORKFLOW_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "workflows")
path_resolver = PathTools(BASE_DIR)
project_resolver = PathTools(PARENT_DIR)
workflow_path_resolver = PathTools(WORKFLOW_DIR)

config = None
with open(path_resolver.preview_join_resolved("workflows/full_pipeline_adb_deploy.yml"), "r") as f:
    config = yaml.safe_load(f)

# use for cycles detection
graph = defaultdict(lambda: set())
in_degree = {}
# use for parallelized job queueing
graph_reversed = defaultdict(lambda: set())
in_degree_reversed = {}

for job in config['jobs'].items():
    job_name = job[0]
    in_degree[job_name] = 0
    in_degree_reversed[job_name] = 0

for job in config['jobs'].items():
    job_name = job[0]
    # print("job name: ", job_name)
    job_commands = job[1]['run']
    # print("job commands: ", job_commands)
    job_requirements = job[1]['needs']
    # print("job requirements: ", job_requirements)
    
    for dependency in job_requirements:
        graph[job_name].add(dependency)
        in_degree[dependency] += 1
        graph_reversed[dependency].add(job_name)
        in_degree_reversed[job_name] += 1

cycle_detector = CheckCycles(in_degree, graph)

no_cycles, topo_sorted = cycle_detector.check_cycles()
print("No cycles detected" if no_cycles else "Cycles detected")
print(topo_sorted)

if not no_cycles:
    sys.exit(1)

### RUN JOBS ###
MAX_PARALLEL_JOBS = 2

queue = deque()
for node, degree in in_degree_reversed.items():
    if degree == 0:
        queue.append(node)

lock = threading.Lock()
cond = threading.Condition(lock)
_count = 0
_stop = False

def worker():
    global _count
    global _stop

    while True:
        with cond:
            while not queue and _count < len(in_degree_reversed) and not _stop:
                print("Waiting for a job...")
                cond.wait()
            if _count != len(in_degree_reversed) and not _stop:
                job_name = queue.popleft()
                print(job_name)

                components = config['jobs'][job_name]['run'][0].split()
                rel_path = config['jobs'][job_name]['run'][0].split()[-1]
                resolved_path = project_resolver.preview_join_resolved(rel_path)
                components[-1] = resolved_path
            else:
                return

        # run subprocess outside condition to release the lock for other threads
        result = subprocess.run(components, capture_output=True, text=True)
        print(result.stdout)

        with cond:
            if _stop:
                return
            if result.returncode == 0:
                _count += 1
                for dependent in graph_reversed[job_name]:
                    in_degree_reversed[dependent] -= 1
                    if in_degree_reversed[dependent] == 0:
                        queue.append(dependent)
                        cond.notify()
                if _count == len(in_degree_reversed):
                    cond.notify_all()
                    return
            else:
                _stop = True
                cond.notify_all()
                return

threads = [threading.Thread(target=worker) for _ in range(MAX_PARALLEL_JOBS)]
for t in threads: t.start()
for t in threads: t.join()

if _stop:
    print("Workflow Unsuccessful.")
    sys.exit(1)
print("Workflow Successful.")
sys.exit(0)
