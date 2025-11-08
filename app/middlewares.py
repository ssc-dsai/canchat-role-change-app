from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.datastructures import URL

class RedirectToAppPrefixMiddleware:
    def __init__(self, app: FastAPI, app_prefix: str):
        self.app = app
        self.app_prefix = app_prefix.strip("/")

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            path = scope["path"]
            
            headers = {k.decode("utf-8"): v.decode("utf-8") for k, v in scope.get("headers", [])}
            host = headers.get("x-forwarded-host", headers.get("host", "localhost"))
            proto = headers.get("x-forwarded-proto", "http")

            # If the path is only the app_prefix without a slash, redirect to include the trailing slash
            if path == f"/{self.app_prefix}" and self.app_prefix != "":
                new_url = URL(f"{proto}://{host}/{self.app_prefix}/")
                response = RedirectResponse(url=str(new_url), status_code=308)
                await response(scope, receive, send)
                return

            if not path.startswith(f"/{self.app_prefix}"):
                new_url = URL(f"{proto}://{host}/{self.app_prefix}/{path.lstrip('/')}")
                response = RedirectResponse(url=str(new_url), status_code=308)
                await response(scope, receive, send)
                return

        await self.app(scope, receive, send)


class RemoveTrailingSlashMiddleware:
    def __init__(self, app: FastAPI, app_prefix: str):
        # Save a reference to the ASGI app
        self.app = app
        self.app_prefix = app_prefix.strip("/")

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            path = scope["path"]

            if path != "/" and path != f"/{self.app_prefix}/"  and path.endswith("/"):
                # Extract headers to get `host` and `proto`
                headers = {k.decode("utf-8"): v.decode("utf-8") for k, v in scope.get("headers", [])}
                
                host = headers.get("x-forwarded-host", headers.get("host", "localhost"))
                proto = headers.get("x-forwarded-proto", "http")
                
                new_url = URL(f"{proto}://{host}{path.rstrip('/')}")
                response = RedirectResponse(url=str(new_url), status_code=308)
                await response(scope, receive, send)
                return

        await self.app(scope, receive, send)