import io

import requests
from PIL import Image
from PIL.Image import Image as PilImage


class LibcomApiTestCase(object):
    def load_image_from_url(self, image_url: str) -> PilImage:
        """Load image from URL.

        Args:
            image_url (str): Image URL.

        Returns:
            PilImage: PIL Image.
        """
        return Image.open(requests.get(image_url, stream=True).raw)

    def get_image_io_from_url(self, image_url: str) -> io.BytesIO:
        """Get image IO from URL.

        Args:
            image_url (str): Image URL.

        Returns:
            io.BytesIO: Image IO.
        """
        image = self.load_image_from_url(image_url)
        return self.get_image_io(image)

    def get_image_io(self, image: PilImage) -> io.BytesIO:
        """Get image IO.

        Args:
            image (PilImage): PIL Image.

        Returns:
            io.BytesIO: Image IO.
        """
        image_io = io.BytesIO()
        image.save(image_io, format="PNG")
        image_io.seek(0)
        return image_io
