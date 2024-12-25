from typing import get_args

from libcom_api.routers.shadow_generation import ModelType
from libcom_api.testing import LibcomApiTestCase


class TestControllableComposition(LibcomApiTestCase):
    def test_model_type(self):
        from libcom.controllable_composition.controllable_composition import (
            model_set as expected_model_type,
        )

        accutual_model_type = get_args(ModelType)
        assert (
            accutual_model_type == expected_model_type
        ), f"{accutual_model_type} != {expected_model_type}"
