from dotenv import load_dotenv
import os
from pymongo import MongoClient
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional
load_dotenv(".env")

USER = os.getenv("username")
PASSWORD = os.getenv("password")
client = MongoClient(f"mongodb://{USER}:{PASSWORD}@mongo.exceed19.online:8443/?authMechanism=DEFAULT")

db = client["exceed05"]
hb_collection = db["heart-beat"]

class HeartRate(BaseModel):
    name: Optional[str]
    birth: Optional[datetime]
    current_heartrate: Optional[int]
    excercise_heartrate: Optional[int]
    normal_heartrate: Optional[int]
    is_on : int

