from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.apache import HtpasswdFile
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_401_UNAUTHORIZED


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, htpasswd_path: str, whitelist: list = None):
        super().__init__(app)
        self.htpasswd = HtpasswdFile(htpasswd_path)
        self.security = HTTPBasic()
        self.whitelist = whitelist if whitelist is not None else []

    async def dispatch(self, request: Request, call_next):
        # Skip authentication for whitelisted paths
        if request.url.path in self.whitelist:
            return await call_next(request)

        # Perform authentication
        try:
            credentials: HTTPBasicCredentials = await self.security(request)
        except HTTPException:
            return JSONResponse(
                status_code=HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid authentication details"},
                headers={"WWW-Authenticate": "Basic"},
            )

        if not self.htpasswd.check_password(credentials.username, credentials.password):
            return JSONResponse(
                status_code=HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid authentication details"},
                headers={"WWW-Authenticate": "Basic"},
            )

        request.state.username = credentials.username
        return await call_next(request)
