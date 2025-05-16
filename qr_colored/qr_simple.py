"""Generate a simple black-and-white QR code image"""

from typing import Tuple
from PIL import Image
import qrcode


def generate_qrcode(content: str,
                    version: int = 1,
                    error_correction: int = qrcode.ERROR_CORRECT_H,
                    box_size: int = 16,
                    border: int = 0,
                    padding_multiple: int = 256,
                    max_size: int = 1024,
                    ) -> Image.Image:
    """
    Generates and returns a QR code image with centered padding.

    Parameters
    ----------
    content : str
        The content to encode into the QR code.
    version : int, optional
        Controls the size of the QR Code (1 to 40). Higher numbers = bigger code.
    error_correction : int, optional
        Error correction level: L (7%), M (15%), Q (25%), H (30%).
    box_size : int, optional
        Number of pixels per box/module in the QR code matrix.
    border : int, optional
        Thickness of border (in boxes/modules) around the QR code.
    padding_multiple : int, optional
        Final image dimensions will be rounded up to a multiple of this.
    max_size : int, optional
        Maximum allowable image size (in pixels). If exceeded, raises an error.

    Returns
    -------
    Image.Image
        A grayscale ('L' mode) QR code image centered on a padded white canvas.

    Raises
    ------
    ValueError
        If the padded image exceeds the allowed `max_size`.
    """
    # Initialize a QRCode object with the given configuration
    # for size, error correction, and layout.
    qr = qrcode.QRCode(
        version=version,
        error_correction=error_correction,
        box_size=box_size,
        border=border,
    )

    # Add the provided content to the QR matrix and
    # auto-adjust the structure to fit the data.
    qr.add_data(content)
    qr.make(fit=True)

    # Generate a black-and-white QR code image from the
    # matrix and convert it to grayscale mode ('L').
    qr_image = qr.make_image(fill_color='black', back_color='white')
    qr_image = qr_image.convert('L')  # pyright: ignore

    # Extract the raw size of the QR code image before adding any padding.
    qr_width, qr_height = qr_image.size

    # Calculate the minimum additional space needed to prevent edge clipping.
    min_offset = 8 * box_size

    # Compute the final canvas size by rounding up to the nearest multiple of `padding_multiple`.
    # This ensures consistent alignment in grid-based image layouts or display systems.
    padded_width = (qr_width + 255 + min_offset) // padding_multiple * padding_multiple
    padded_height = (qr_height + 255 + min_offset) // padding_multiple * padding_multiple

    # Guard against generating images that are excessively large.
    if padded_width > max_size:
        raise ValueError("Content too large for the configured maximum image size!")

    # Create a new blank canvas (white background) in grayscale mode with the padded dimensions.
    canvas = Image.new('L', (padded_width, padded_height), 255)

    # Calculate the top-left coordinates where the QR image should be pasted to appear centered.
    # Coordinates are aligned to `box_size` to ensure visual symmetry and alignment.
    top_left: Tuple[int, int] = (
        ((padded_width - qr_width) // 2) // box_size * box_size,
        ((padded_height - qr_height) // 2) // box_size * box_size,
    )

    # Paste the QR code onto the center of the canvas using the calculated position.
    canvas.paste(qr_image, top_left)

    # Return the final padded QR code image ready for saving, displaying, or further processing.
    return canvas
