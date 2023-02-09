from fastapi import APIRouter, Body
from database import db, hb_collection
from pydantic import BaseModel
router = APIRouter(prefix="/hard")

class Bpm(BaseModel):
    bpm: int

class ChangeMode(BaseModel):
    mode: int

class OnOff(BaseModel):
    is_on: int

@router.get("/get_status")
def hard_get_status():
    print(db.list_collection_names())
    return {"status": 1}

# recive bpm from hard
@router.post("/send_bpm")
def hard_send_bpm(bpm: Bpm = Body()): 
    bmp = bpm.bpm

# recieve change mode button
@router.post("/change_mode")
def hard_change_mode(chm: ChangeMode = Body()):
    new_mode = chm.mode

@router.post("/on_off")
def hard_on_off(on_off: OnOff):
    is_on = on_off.is_on
