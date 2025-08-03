from http import HTTPStatus
from typing import Annotated

from aioinject import Inject
from aioinject.ext.fastapi import inject
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from result import Err

from app.core.domain.cameras.commands import (
    CameraCreateCommand,
    CameraHttpImageCommand,
    CameraRtpsBase64Command,
    CameraRtpsImageCommand,
)
from app.core.domain.cameras.dto import CameraCreateDTO
from app.core.domain.cameras.errors import CameraAlreadyExistsError
from app.core.domain.cameras.queries import CameraGetQuery
from lib.camera_helper import camera_checker
from lib.image_proccesing.video_capture import VideoStreamCapture

from .schema import (
    CameraCreateSchema,
    CameraSchema,
    CameraUrlSchema,
    RtpsCameraSchema,
    SaveImageSchema,
)

router = APIRouter(
    tags=["cameras"],
    prefix="/cameras",
)


@router.post(
    "",
    responses={
        HTTPStatus.CREATED: {"model": CameraSchema},
    },
    status_code=HTTPStatus.CREATED,
)
@inject
async def cameras_create(
    schema: CameraCreateSchema,
    command: Annotated[CameraCreateCommand, Inject],
) -> CameraSchema:
    camera = await command.execute(
        dto=CameraCreateDTO(
            title=schema.title,
            host=schema.host,
            login=schema.login,
            password=schema.password,
            path=schema.path,
        )
    )
    if isinstance(camera, Err):
        match camera.err_value:
            case CameraAlreadyExistsError():
                raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)

    return CameraSchema.model_validate(camera.ok_value)


@router.get(
    "/{camera_id}",
    responses={
        HTTPStatus.OK: {"model": CameraSchema},
        HTTPStatus.NOT_FOUND: {"description": "Camera not found"},
    },
)
@inject
async def cameras_retrieve(
    camera_id: int,
    camera_query: Annotated[CameraGetQuery, Inject],
) -> CameraSchema:
    camera = await camera_query.execute(camera_id=camera_id)
    if not camera:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return CameraSchema.model_validate(camera)


@router.post(
    "/http-image-capture",
    status_code=HTTPStatus.CREATED,
)
@inject
async def save_image_from_html(
    schema: CameraUrlSchema,
    command: Annotated[CameraHttpImageCommand, Inject],
) -> SaveImageSchema:
    if not schema.url:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Required url"
        )

    image = await command.execute(url=schema.url)
    if isinstance(image, Err):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)

    return SaveImageSchema(name=image.ok_value)


@router.post(
    "/rtps-image-capture",
    status_code=HTTPStatus.CREATED,
)
@inject
async def save_image_from_rtps(
    schema: RtpsCameraSchema,
    command: Annotated[CameraRtpsImageCommand, Inject],
) -> SaveImageSchema:
    if not schema.host or schema.port:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Required host or port"
        )

    available = await camera_checker(host=schema.host, port=schema.port)

    if isinstance(available, Err):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Camera not available"
        )

    image = await command.execute(url=schema.host)
    if isinstance(image, Err):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)

    return SaveImageSchema(name=image.ok_value)


@router.post(
    "/rtps-sent-telegram",
    status_code=HTTPStatus.CREATED,
)
@inject
async def base64_from_rtps(
    schema: CameraUrlSchema,
    command: Annotated[CameraRtpsBase64Command, Inject],
) -> SaveImageSchema:
    # TODO(Srg300): доработать
    await command.execute(url=schema.url)

    return SaveImageSchema(name="Ok")


@router.get(
    "/{camera_id}/stream",
)
@inject
async def video_stream(
    camera_id: int,
    command: Annotated[VideoStreamCapture, Inject],
    camera_query: Annotated[CameraGetQuery, Inject],
) -> StreamingResponse:
    camera = await camera_query.execute(camera_id=camera_id)
    if not camera:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    password = camera.password if camera.password else ""
    url = f"rtsp://{camera.login}:{password}@{camera.host}/cam/realmonitor?channel=1&subtype=0"
    return StreamingResponse(
        command.video_stream_(url=url),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )
