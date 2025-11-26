from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import Base, engine
from routers import router_slug


@asynccontextmanager
async def lifespan(app: FastAPI):
    """ """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(title="URL Shortener", lifespan=lifespan, root_path="/api")


@app.get("/health")
async def health_check() -> dict[str, str]:
    """ """
    return {"status": "ok"}


app.include_router(router=router_slug)


# app.mount(
#     "/static",
#     StaticFiles(directory=Path(__file__).resolve().parent / "static"),
#     name="static",
# )


# @app.get("/")
# async def index():
#     """ """
#     return RedirectResponse(url="/static/index.html")
