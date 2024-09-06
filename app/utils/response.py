from fastapi.responses import JSONResponse


class CustomResponse(JSONResponse):
    def __init__(self, message: str, status=200, success=True, data=None) -> None:

        response = {"success": success, "message": message, "data": data}

        super().__init__(status_code=status, content=response)
