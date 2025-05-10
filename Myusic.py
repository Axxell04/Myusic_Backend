import subprocess
import os
import qrcode

from config import MAIN_PATH, IP_SERVER

VENV_PATH = os.path.join(MAIN_PATH, "venv")

cmd_venv = f"{os.path.join(VENV_PATH, "Scripts/activate")}"

# cmd_pip_freeze = "pip freeze"
cmd_run_server = "py main.py"

url = f"http://{IP_SERVER}:8000"
qr = qrcode.QRCode()
qr.add_data(url)
qr.make()
qr.print_ascii(invert=True)

try:
    subprocess.run(f"{cmd_venv} & echo IP Server: {IP_SERVER} & {cmd_run_server}",shell=True, check=True)
except subprocess.CalledProcessError as e:
    print(f"Servidor detenido \n {e}")
except KeyboardInterrupt as e:
    print(f"Servidor detenido \n {e}")