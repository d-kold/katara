import json

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/status")
async def get_water_solenoid_status() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/on")
async def turn_on_water_solenoid() -> HTMLResponse:
    data = {"status": "ON", "message": "The solenoid is activated."}
    json_data_str = json.dumps(data, indent=4)

    gif_html = '<img src="/assets/on.gif" width="480" height="270" />'

    response_html = f"""
    <div>
        {gif_html}
    </div>
    """

    return HTMLResponse(content=response_html, status_code=200)


@router.post("/off")
async def turn_off_water_solenoid() -> HTMLResponse:
    data = {"status": "ON", "message": "The solenoid is turned off."}
    json_data_str = json.dumps(data, indent=4)

    gif_html = '<img src="/assets/off.gif" width="480" height="270" />'

    response_html = f"""
    <div>
        {gif_html}
    </div>
    """

    return HTMLResponse(content=response_html, status_code=200)
