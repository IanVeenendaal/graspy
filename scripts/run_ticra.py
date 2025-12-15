import os
import shutil
from pathlib import Path


project_dir = Path(
    r"C:\Users\Ian Veenendaal\OneDrive - Cardiff University\Projects\LiteBIRD\models\antenna\graspy_optimized\L1"
)
run_dir = project_dir.parent / "batch" / project_dir.name
run_dir.mkdir(parents=True, exist_ok=True)

# copy working directory files to run directory
working_dir = project_dir / "working"
for file in working_dir.glob("*"):
    shutil.copy(file, run_dir / file.name)

# Set cwd to run_dir
os.chdir(run_dir)
output_file = "results"
log_file = "log"

cmd = f"ticra-tools batch.gxp {output_file}.out {log_file}.log"

# Add ticra_tools.exe to PATH
os.environ["PATH"] += r";C:\Program Files\TICRA\TICRA-Tools-23.0\bin"

print(f"Running command: {cmd}")
os.system(cmd)
