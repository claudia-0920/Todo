from fastapi import Request,HTTPException
from fastapi.responses import JSONResponse
from schemas.common import CommonResponse


async def http_exception_handler(request:Request,exc:HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=CommonResponse(
            code=exc.status_code,
            msg=str(exc.detail),
            data=None
        ).model_dump()
    )