import pytest
from fastapi.testclient import TestClient

from libcom_api.testing import LibcomApiTestCase


class TestColorTransfer(LibcomApiTestCase):
    @pytest.mark.parametrize(
        argnames="image_url, style_image_url",
        argvalues=(
            (
                "https://raw.githubusercontent.com/bcmi/libcom/refs/heads/main/tests/source/composite/1.jpg",
                "https://raw.githubusercontent.com/bcmi/libcom/refs/heads/main/tests/source/composite_mask/1.png",
            ),
            (
                "https://raw.githubusercontent.com/bcmi/libcom/refs/heads/main/tests/source/composite/8.jpg",
                "https://raw.githubusercontent.com/bcmi/libcom/refs/heads/main/tests/source/composite_mask/8.png",
            ),
        ),
    )
    def test_endpoint(self, client: TestClient, image_url: str, style_image_url: str):
        img_io = self.get_image_io_from_url(image_url)
        sty_io = self.get_image_io_from_url(style_image_url)

        response = client.post(
            "/color-transfer",
            files={
                "image_file": ("image.png", img_io),
                "style_image_file": ("style.png", sty_io),
            },
        )
        assert response.status_code == 200
