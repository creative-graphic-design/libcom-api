import random
from tempfile import NamedTemporaryFile
from typing import Literal, Optional

import cv2
import torch
from fastapi import APIRouter, Response, UploadFile
from libcom import ShadowGenerationModel
from loguru import logger
from PIL import Image

from libcom_api.utils import image_to_bytes

ModelType = Literal["ShadowGeneration"]

router = APIRouter(tags=["Shadow Generation"])

model: Optional[ShadowGenerationModel] = None


def load_model(
    model_type: ModelType, device: Optional[torch.device] = None
) -> ShadowGenerationModel:
    """Load `ShadowGenerationModel` model.

    Args:
        model_type (ModelType): Model type to load.
        device (Optional[torch.device], optional): Device to load the model on. Defaults to None.

    Returns:
        ShadowGenerationModel: Loaded model.
    """
    global model

    if model is not None:
        return model

    device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logger.info(f"Loading model `{model_type}` on device `{device}`")

    return ShadowGenerationModel(
        device=device,  # type: ignore
        model_type=model_type,
    )


@router.post(
    "/shadow-generation",
    responses={200: {"content": {"image/png": {}}}},
    response_class=Response,
)
def shadow_generation(
    image_file: UploadFile,
    mask_image_file: UploadFile,
    model_type: ModelType,
    seed: Optional[int] = None,
) -> Response:
    seed = seed or random.randint(0, 2**32)
    model = load_model(model_type=model_type)

    # The model can return multiple generated results, but here we hardcode to return only one
    # TODO: Consider how to return the results when multiple generations are performed
    num_predictions = 1

    with NamedTemporaryFile() as image:
        with NamedTemporaryFile() as mask_image:
            image.write(image_file.file.read())
            mask_image.write(mask_image_file.file.read())
            image_path = image.name
            mask_image_path = mask_image.name

            predictions = model(
                composite_image=image_path,
                composite_mask=mask_image_path,
                number=num_predictions,
                seed=seed,
            )
    assert len(predictions) == num_predictions == 1

    (pred_np,) = predictions
    pred_np = cv2.cvtColor(pred_np, cv2.COLOR_BGR2RGB)
    pred_pl = Image.fromarray(pred_np)

    return Response(content=image_to_bytes(pred_pl), media_type="image/png")
