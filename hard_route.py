from fastapi import APIRouter, Body
from database import db, hb_collection
from pydantic import BaseModel
from datetime import datetime, timedelta
import random
router = APIRouter(prefix="/hard")

class Bpm(BaseModel):
    bpm: int

class ChangeMode(BaseModel):
    mode: int

class OnOff(BaseModel):
    is_on: int

hb_history = db["hb_history"]
class HeartbeatHistory(BaseModel):
    time: datetime
    bpm: int
    mode: int
    status: int

# delete records that less than x hrs old
def clear_history(hr: int):
    now = datetime.now()
    now -= timedelta(hours=hr)
    hb_history.delete_many({"time": {"$lt": now}})

def get_field_from_hb_collection(k: list):
    ret = {}
    return ret

@router.get("/debug/mock_hb_history")
def mock_hb_history():
    now = datetime.now()
    now -= timedelta(hours=random.randint(0, 44))
    record = {"time": now,
              "bpm": random.randint(66, 180),
              "mode": 1,
              "status": 1}
    hb_history.insert_one(record)
    return "Ok"

@router.get("/debug/clear_history/{hr}")
def debug_clear(hr: int):
    clear_history(hr)
    return "Ok"

@router.get("/get_status")
def hard_get_status():
    status = get_field_from_hb_collection(["status"])["status"]
    return {"status": status}

@router.get("/get_mode")
def hard_get_mode():
    mode = get_field_from_hb_collection(["mode"])["mode"]
    return {"mode": mode}

# recive bpm from hard
@router.post("/send_bpm")
def hard_send_bpm(bpm: Bpm = Body()): 
    bmp = bpm.bpm
    record = {"time": datetime.now(),
              "bpm": bpm,
              "mode": 1,
              "status": 1}
    hb_history.insert_one(record)

# recieve change mode button
@router.post("/change_mode")
def hard_change_mode(chm: ChangeMode = Body()):
    new_mode = chm.mode

@router.post("/on_off")
def hard_on_off(on_off: OnOff):
    is_on = on_off.is_on
