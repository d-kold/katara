import threading
from pathlib import Path

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter, Request
from fastapi.staticfiles import StaticFiles
from starlette.templating import _TemplateResponse, Jinja2Templates

from api.api_v1.api import api_router
from core.config import settings
from env_config import EnvConfig
from services.mqtt_service import MqttClient
from core import commands
from core.db import init_db

BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "assets"))

root_router = APIRouter()
app = FastAPI(title="Katara API")

app.mount("/assets", StaticFiles(directory=str(BASE_PATH / "assets")), name="assets")

load_dotenv()  # take environment variables from .env


@root_router.get("/", status_code=200)
def root(request: Request) -> _TemplateResponse:
    """
    Root GET
    """
    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request},
    )
    # return TEMPLATES.TemplateResponse("base.html",
    #                                   {
    #                                       "request": request,
    #                                       "include_switch_control": True,
    #                                       "include_current_status": True,
    #                                       "include_status_list": True,
    #                                   })


app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)


def start():
    init_db()

    config = EnvConfig.load(EnvConfig.CONFIG_KEYS)

    mqtt_client = MqttClient(
        host=config['MQTT_HOST'],
        port=config['MQTT_PORT'],
        qos=config['MQTT_QOS'],
        username=config['MQTT_USERNAME'],
        password=config['MQTT_PASSWORD']
    )

    commands.mqtt_client = mqtt_client

    t = threading.Thread(target=mqtt_client.start, name='mqtt client')
    t.daemon = True
    t.start()

    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")


if __name__ == "__main__":
    start()
