"""generate a simple b/w qr code image"""

from PIL import Image
import qrcode


def generate_qrcode(content: str) -> Image:  # pyright: ignore
    """
    generates and returns a QR code

    Parameters
    ----------
    content : str
        the content that is available when qr code is scanned

    Returns
    -------
    Image
        generated QR code image
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.ERROR_CORRECT_H,
        box_size=16,
        border=0,
    )
    qr.add_data(content)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white').convert('L')  # pyright: ignore

    offset_min = 8 * 16
    width, height = img.size
    width = (width + 255 + offset_min) // 256 * 256
    height = (height + 255 + offset_min) // 256 * 256
    if width > 1024:
        raise ValueError("Content too large!!!")

    bg = Image.new('L', (width, height), 255)
    coords = (
        (width - img.size[0]) // 2 // 16 * 16,
        (height - img.size[1]) // 2 // 16 * 16
    )
    bg.paste(img, coords)
    return bg  # pyright: ignore
