from pydantic import BaseModel


class CookDownload(BaseModel):
    file: str


class CookStatus(BaseModel):
    ok: bool
    ready: bool | None = None
    download: CookDownload | None = None
