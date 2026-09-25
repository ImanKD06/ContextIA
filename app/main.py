from fastapi import FastAPI
from mangum import Mangum

from app.routers.documents import router as documents_router
from app.routers.chat import router as chat_router

app = FastAPI(
    title="ContextIA API",
    version="1.0.0",
    redirect_slashes=False
)

app.include_router(documents_router)
app.include_router(chat_router)

handler = Mangum(app)