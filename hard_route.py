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
    data = hb_collection.find_one({}, {"_id": 0});
    if not data:
        print("Not Ok")
    for r in k:
        ret[r] = data[r]
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
    hard_rate = get_field_from_hb_collection(["current_heartrate"])["current_heartrate"]
    # Mock status
    if (hard_rate > 130):
        status = 2
    elif (hard_rate > 120):
        status = 1
    else:
        status = 0
    return {"status": status}

@router.get("/get_mode")
def hard_get_mode():
    mode = get_field_from_hb_collection(["mode"])["mode"]
    return {"mode": mode}

# recive bpm from hard
@router.post("/send_bpm")
def hard_send_bpm(bpm_get: Bpm = Body()): 
    bpm = bpm_get.bpm
    record = {"time": datetime.now(),
              "bpm": bpm,
              "mode": 1,
              "status": 1}
    hb_collection.update_many({}, {"$set": {"current_heartrate": bpm}})
    return "OK"

# recieve change mode button
@router.post("/change_mode")
def hard_change_mode(chm: ChangeMode = Body()):
    new_mode = chm.mode
    hb_collection.update_many({}, {"$set": {"mode": new_mode}})
    return "OK"

@router.post("/on_off")
def hard_on_off(on_off: OnOff):
    is_on = on_off.is_on
    hb_collection.update_many({}, {"$set": {"is_on": is_on}})
    return "OK"
