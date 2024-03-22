import json
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse

from core import commands
from sqlalchemy.orm import Session

from core.db import get_db, SwitchEvent

router = APIRouter()


@router.get("/status", response_class=HTMLResponse)
async def get_water_solenoid_status(db: Session = Depends(get_db)) -> HTMLResponse:
    latest_event = db.query(SwitchEvent).order_by(SwitchEvent.id.desc()).first()
    if latest_event is None:
        return HTMLResponse(content="<div>No status found.</div>", status_code=200)
    return HTMLResponse(content=f"""
    <div class="bg-white shadow-lg rounded-lg p-5 mb-4">
        <h2 class="font-bold text-xl">Current Status: {latest_event.status.upper()}</h2>
        <p>Last updated at: {latest_event.timestamp}</p>
    </div>
    """, status_code=200)


@router.get("/status/all", response_class=HTMLResponse)
async def get_all_statuses(db: Session = Depends(get_db)) -> HTMLResponse:
    events = db.query(SwitchEvent).order_by(SwitchEvent.id.desc()).all()
    if not events:
        return HTMLResponse(content="<div>No status events found.</div>", status_code=200)
    events_html = "".join([
        f"<div class='bg-white shadow-lg rounded-lg p-5 mb-4'><h2 class='font-bold'>Status: {event.status.upper()}</h2><p>Timestamp: {event.timestamp}</p></div>"
        for event in events
    ])
    return HTMLResponse(content=events_html, status_code=200)


@router.post("/on", status_code=201)
async def turn_on_water_solenoid(db: Session = Depends(get_db)) -> HTMLResponse:
    # data = {"status": "ON", "message": "The solenoid is activated."}
    # json_data_str = json.dumps(data, indent=4)

    # Save the event to the database
    db_event = SwitchEvent(status="on")
    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    # Send a message to the MQTT broker to turn on the water solenoid
    commands.switch(message="on")

    gif_html = '<img src="/assets/on.gif" width="480" height="270" />'

    response_html = f"""
    <div>
        {gif_html}
    </div>
    """

    return HTMLResponse(content=response_html, status_code=201)


@router.post("/off", status_code=201)
async def turn_off_water_solenoid(db: Session = Depends(get_db)) -> HTMLResponse:
    # data = {"status": "ON", "message": "The solenoid is turned off."}
    # json_data_str = json.dumps(data, indent=4)

    # Save the event to the database
    db_event = SwitchEvent(status="off")
    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    # Send a message to the MQTT broker to turn off the water solenoid
    commands.switch(message="off")

    gif_html = '<img src="/assets/off.gif" width="480" height="270" />'

    response_html = f"""
    <div>
        {gif_html}
    </div>
    """

    return HTMLResponse(content=response_html, status_code=201)
