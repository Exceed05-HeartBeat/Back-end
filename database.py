from dotenv import load_dotenv
import os
from pymongo import MongoClient
from pydantic import BaseModel
from datetime import datetime, timedelta, date
from typing import Optional
load_dotenv(".env")

USER = os.getenv("username")
PASSWORD = os.getenv("password")
client = MongoClient(f"mongodb://{USER}:{PASSWORD}@mongo.exceed19.online:8443/?authMechanism=DEFAULT")

db = client["exceed05"]
hb_collection = db["heart-beat"]

class Normal_heartrate(BaseModel):
    timestamp: int
    bmp: int

class Excercise_heartrate(BaseModel):
    timestamp: int
    bmp: int


class HeartRate(BaseModel):
    name: Optional[str]
    birth: Optional[str]
    current_heartrate: Optional[int]
    excercise_heartrate: list[Excercise_heartrate]
    normal_heartrate: list[Normal_heartrate]
    is_on : Optional[int]
    mode: Optional[int]
