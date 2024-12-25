import io

from PIL.Image import Image as PilImage


def image_to_bytes(image: PilImage) -> bytes:
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    return buf.getvalue()
