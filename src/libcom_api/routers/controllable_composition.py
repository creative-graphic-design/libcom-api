from typing import Literal, Optional

import torch
from fastapi import APIRouter, Response, UploadFile
from libcom import ControlComModel
from loguru import logger

ModelType = Literal["ControlCom", "ControlCom_blend_harm", "ControlCom_view_comp"]

router = APIRouter(tags=["Controllable Composition"])

model: Optional[ControlComModel] = None
device: torch.device = torch.device("cpu" if torch.cuda.is_available() else "cuda")


def load_model(device: torch.device, model_type: ModelType):
    global model

    if model is not None:
        return model

    logger.info(f"Loading model `{model_type}` on device `{device}`")

    return ControlComModel(
        device=device,  # type: ignore
        model_type=model_type,
    )


@router.post("/controllable-composition")
def controllable_composition(image_file: UploadFile):
    raise NotImplementedError
