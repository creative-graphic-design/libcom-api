from tempfile import NamedTemporaryFile

import cv2
import libcom
import libcom.utils
import libcom.utils.process_image
from fastapi import APIRouter, Response, UploadFile
from PIL import Image

from libcom_api.utils import image_to_bytes

router = APIRouter(tags=["Color Transfer"])


@router.post(
    "/color-transfer",
    responses={200: {"content": {"image/png": {}}}},
    response_class=Response,
)
def color_transfer(image_file: UploadFile, style_image_file: UploadFile) -> Response:
    with NamedTemporaryFile() as image:
        with NamedTemporaryFile() as style_image:
            image.write(image_file.file.read())
            style_image.write(style_image_file.file.read())
            image_path = image.name
            style_image_path = style_image.name

            transfered_image_np = libcom.color_transfer(image_path, style_image_path)

    transfered_image_np = cv2.cvtColor(transfered_image_np, cv2.COLOR_BGR2RGB)
    transfered_image_pl = Image.fromarray(transfered_image_np)
    return Response(content=image_to_bytes(transfered_image_pl), media_type="image/png")
