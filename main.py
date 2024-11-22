from fastapi import FastAPI, Header
import uvicorn
from typing import Annotated

from models import Item
import service
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/item")
def read_item(item: Item, tenant_id: Annotated[str | None, Header(convert_underscores=False)] = None):
    print(f"tenant_id: {tenant_id}")
    service.create_item(item, tenant_id)
    return "OK"


if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True)
