from typing import get_args

import pytest
import torch
from fastapi.testclient import TestClient

from libcom_api.routers.shadow_generation import ModelType
from libcom_api.testing import LibcomApiTestCase


class TestShadowGeneartion(LibcomApiTestCase):
    @pytest.mark.skipif(
        not torch.cuda.is_available(), reason="No GPUs available for testing"
    )
    @pytest.mark.parametrize(
        argnames="image_url, mask_image_url",
        argvalues=(
            (
                "https://raw.githubusercontent.com/bcmi/libcom/refs/heads/main/tests/shadow_generation/composite/1.png",
                "https://raw.githubusercontent.com/bcmi/libcom/refs/heads/main/tests/shadow_generation/composite_mask/1.png",
            ),
            (
                "https://raw.githubusercontent.com/bcmi/libcom/refs/heads/main/tests/shadow_generation/composite/2.png",
                "https://raw.githubusercontent.com/bcmi/libcom/refs/heads/main/tests/shadow_generation/composite_mask/2.png",
            ),
        ),
    )
    @pytest.mark.parametrize(
        argnames="model_type",
        argvalues=get_args(ModelType),
    )
    def test_endpoint(
        self,
        client: TestClient,
        image_url: str,
        mask_image_url: str,
        model_type: ModelType,
    ):
        img_io = self.get_image_io_from_url(image_url)
        msk_io = self.get_image_io_from_url(mask_image_url)

        response = client.post(
            "/shadow-generation",
            files={
                "image_file": ("image.png", img_io),
                "mask_image_file": ("mask.png", msk_io),
            },
            params={
                "model_type": model_type,
                "num_predictions": 1,
                "seed": 42,
            },
        )
        assert response.status_code == 200

    def test_model_type(self):
        from libcom.shadow_generation.shadow_generation import (
            model_set as expected_model_type,
        )

        accutual_model_type = get_args(ModelType)
        assert (
            accutual_model_type == expected_model_type
        ), f"{accutual_model_type} != {expected_model_type}"
