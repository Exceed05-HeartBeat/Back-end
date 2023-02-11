from fastapi import APIRouter, Body
from database import db, hb_collection
from pydantic import BaseModel
from datetime import datetime, timedelta, time
from front_route import calculate_maxrate, get_status
import random
from database import HeartRate
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
    status = get_status()
    return {"status": status}

@router.get("/get_mode")
def hard_get_mode():
    mode = get_field_from_hb_collection(["mode"])["mode"]
    return {"mode": mode}


# recive bpm from hard
@router.post("/send_bpm")
def hard_send_bpm(bpm_get: Bpm = Body()): 
    bpm = bpm_get.bpm
    now = datetime.now()
    record = {"date": str(now.date()),
              "time": str(now.time().strftime("%H:%M:%S")),
              "bpm": bpm}
    hb_collection.update_many({}, {"$set": {"current_heartrate": bpm}}) 
    status = get_status()
    m = get_field_from_hb_collection(["mode"])["mode"]
    print(m)

    # m = 0 => normal
    if m == 0 and (status == 2):
        hb_db = hb_collection.find_one({}, {"_id": False})
        hb_collection.update_one({}, {"$set": {"current_time_warning_normal": str(now.time().strftime("%H:%M:%S"))}})
        time_normal_current = now.time().strftime("%H:%M:%S")
        time_current = datetime.strptime(time_normal_current, "%H:%M:%S")
        last_normal_time_record = datetime.strptime(hb_db["current_time_warning_normal"], "%H:%M:%S")

        print(last_normal_time_record.date())
        if (time_current.minute - last_normal_time_record.minute) > 1:
            hb_collection.update_many({}, {"$push": {"normal_heartrate": record}})
        else:
            return "Cannot record heartrate"

    # m = 0 => excercise
    elif m == 1 and (status == 2):
        hb_db = hb_collection.find_one({}, {"_id": False})
        hb_collection.update_one({}, {"$set": {"current_time_warning_excercise": str(now.time().strftime("%H:%M:%S"))}})
        time_excercise_current = now.time().strftime("%H:%M:%S")
        time_current = datetime.strptime(time_excercise_current, "%H:%M:%S")
        last_excercise_time_record = datetime.strptime(hb_db["current_time_warning_excercise"], "%H:%M:%S")

        print(last_excercise_time_record.day)
        if (time_current.minute - last_excercise_time_record.minute) > 1:
            hb_collection.update_many({}, {"$push": {"exercise_heartrate": record}})
        else:
            return "Cannot record heartrate"

    return "SEND_BPM OK"

# recieve change mode button
@router.post("/change_mode")
def hard_change_mode(chm: ChangeMode = Body()):
    new_mode = chm.mode
    hb_collection.update_many({}, {"$set": {"mode": new_mode}})
    return "CHANGE_MODE OK"

@router.post("/on_off")
def hard_on_off(on_off: OnOff):
    is_on = on_off.is_on
    hb_collection.update_many({}, {"$set": {"is_on": is_on}})
    if is_on == 0:
        hb_collection.update_many({}, {"$set": {"current_heartrate": -1}})
    return "ON/OFF OK"


