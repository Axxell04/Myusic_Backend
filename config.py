import os
import socket

MAIN_PATH = os.path.dirname(os.path.abspath(__file__))
MUSIC_PATH = os.path.join(MAIN_PATH, "music")
IP_SERVER = "0.0.0.0"

DATA_BASE = os.path.join(MAIN_PATH, "myusic.db")

if not os.path.exists(MUSIC_PATH):
    os.mkdir(MUSIC_PATH)
    

def get_local_ip():
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    except socket.error as e:
        print(f"Error al obtener la IP local: {e}")
        return "0.0.0.0"



# Obteniendo ip local
IP_SERVER = get_local_ip()
