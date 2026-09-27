from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from mangum import Mangum

from app.routers.documents import router as documents_router
from app.routers.chat import router as chat_router
from app.routers import proposals


app = FastAPI(
    title="ContextIA API",
    version="1.0.0",
    redirect_slashes=False
)


app.mount(
    "/generated_reports",
    StaticFiles(directory="generated_reports"),
    name="generated_reports"
)


app.include_router(documents_router)

app.include_router(chat_router)

app.include_router(proposals.router)


handler = Mangum(app)