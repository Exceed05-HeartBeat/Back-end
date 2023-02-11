from dotenv import load_dotenv
import os
from pymongo import MongoClient
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional, List
load_dotenv(".env")

USER = os.getenv("username")
PASSWORD = os.getenv("password")
client = MongoClient(f"mongodb://{USER}:{PASSWORD}@mongo.exceed19.online:8443/?authMechanism=DEFAULT")

db = client["exceed05"]
hb_collection = db["heart-beat"]

class Normal_heartrate(BaseModel):
    date: str
    time: str
    bmp: int

class Excercise_heartrate(BaseModel):
    date: str
    time: str
    bmp: int


class HeartRate(BaseModel):
    name: Optional[str]
    birth: Optional[str]
    current_heartrate: Optional[int]
    excercise_heartrate: Optional[List[Excercise_heartrate]]
    normal_heartrate: Optional[List[Normal_heartrate]]
    is_on : Optional[int]
    mode: Optional[int]
    current_time_warning_normal: Optional[str]
    current_time_warning_excercise: Optional[str]

# class BirthName(BaseModel):
#     name: str
#     birth: str

if __name__ == "__main__":
    import random
    import time
    now = datetime.now()
    data = {"date": str(now.date()),
            "time": str(now.time().strftime("%H:%M:%S")),
            "bpm": 44}
    hb_collection.update_many({}, {"$set": {"excercise_heartrate": [data]}})
    hb_collection.update_many({}, {"$set": {"normal_heartrate": [data]}})
