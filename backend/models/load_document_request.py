from pydantic import BaseModel

class LoadDocumentRequest(BaseModel):
    url: str
    content: str
    price: str
    title: str
    image_urls: list[str]
