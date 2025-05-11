import subprocess
import os

from config import MAIN_PATH, IP_SERVER

VENV_PATH = os.path.join(MAIN_PATH, "venv")

cmd_venv = f"{os.path.join(VENV_PATH, "Scripts", "activate")}"

# cmd_pip_freeze = "pip freeze"
cmd_activate = f'cmd /k "{cmd_venv} & py print_qr.py & echo IP Server: {IP_SERVER} & py main.py"'



try:
    subprocess.run(cmd_activate,shell=True, check=True)
except subprocess.CalledProcessError as e:
    print(f"Servidor detenido \n {e}")
except KeyboardInterrupt as e:
    print(f"Servidor detenido \n {e}")