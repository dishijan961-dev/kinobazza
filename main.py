import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .api import router
from .bot import bot, dp, setup_bot
from .config import STATIC_DIR, UPLOAD_DIR
from .database import init_db

logging.basicConfig(level=logging.INFO)

NO_CACHE = {"Cache-Control": "no-cache"}


async def polling_forever():
    """Polling rejimi: xato (masalan, tarmoq uzilishi) bo'lsa o'zi qayta urinadi."""
    while True:
        try:
            await dp.start_polling(bot, handle_signals=False)
            return
        except Exception:
            logging.exception("Polling to'xtadi, 10 soniyadan keyin qayta uriniladi")
            await asyncio.sleep(10)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await setup_bot()
    # Bot (polling) va veb-server bir jarayonda, bir vaqtda ishlaydi
    task = asyncio.create_task(polling_forever())
    logging.info("Bot va server ishga tushdi")
    yield
    task.cancel()
    await bot.session.close()


app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None)
app.include_router(router)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")


@app.get("/")
async def index():
    return FileResponse(STATIC_DIR / "index.html", headers=NO_CACHE)


@app.get("/admin")
async def admin_page():
    return FileResponse(STATIC_DIR / "admin.html", headers=NO_CACHE)


@app.api_route("/health", methods=["GET", "HEAD"])
async def health():
    """UptimeRobot shu manzilni ping qiladi."""
    return {"ok": True}
