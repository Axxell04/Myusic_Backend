import qrcode
from config import IP_SERVER

url = f"http://{IP_SERVER}:8000"
qr = qrcode.QRCode()
qr.add_data(url)
qr.make()
qr.print_ascii(invert=True)