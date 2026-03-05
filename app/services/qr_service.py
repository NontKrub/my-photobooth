import qrcode
from config import DOMAIN


def create_qr(file):

    url = f"{DOMAIN}/download/{file.name}"

    img = qrcode.make(url)

    img.save(str(file) + "_qr.png")