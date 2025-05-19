import asyncio

from result import Err, Ok, Result

from lib.errors import CameraNotAvailableError, CameraTimeoutError


async def camera_checker(
    host: str, port: int
) -> Result[None, CameraNotAvailableError | CameraTimeoutError]:
    connect_ = asyncio.open_connection(host=host, port=port)
    try:
        _, writer = await asyncio.wait_for(fut=connect_, timeout=1)
        writer.close()
        return Ok(None)
    except TimeoutError:
        return Err(CameraNotAvailableError())

    except ConnectionRefusedError:
        return Err(CameraTimeoutError())
