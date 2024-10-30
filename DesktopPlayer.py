import subprocess
import os

from config import MAIN_PATH

VENV_PATH = os.path.join(MAIN_PATH, "venv")

cmd_venv = f"{os.path.join(VENV_PATH, "Scripts/activate")}"

cmd_run_server = "uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

cmd_server1 = f"{cmd_venv} & {cmd_run_server}"
cmd_server2 = f"cd desktop-player & npm run dev -- --host"

try:
    server1 = subprocess.Popen(cmd_server1, shell=True)
    server2 = subprocess.Popen(cmd_server2, shell=True)

    server1.wait()
    server2.wait()
except subprocess.CalledProcessError as e:
    print(f"Servidor detenido \n {e}")
except KeyboardInterrupt as e:
    print(f"Servidor detenido \n {e}")