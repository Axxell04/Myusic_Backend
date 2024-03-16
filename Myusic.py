import subprocess
import os

from config import MAIN_PATH

VENV_PATH = os.path.join(MAIN_PATH, "venv")

cmd_venv = f"{os.path.join(VENV_PATH, "Scripts/activate")}"

# cmd_pip_freeze = "pip freeze"
cmd_run_server = "py main.py"

try:
    subprocess.run(f"{cmd_venv} & {cmd_run_server}",shell=True, check=True)
except subprocess.CalledProcessError as e:
    print(f"Servidor detenido \n {e}")
except KeyboardInterrupt as e:
    print(f"Servidor detenido \n {e}")