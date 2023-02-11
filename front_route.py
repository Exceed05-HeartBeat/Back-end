from fastapi import APIRouter, Body
from database import db, hb_collection
from database import HeartRate
from typing import Optional
from database import HeartRate
# from datetime import datetime, timedelta, date
import datetime

router = APIRouter(prefix="/front")

def get_field_from_hb_collection(k: list):
    ret = {}
    data = hb_collection.find_one({}, {"_id": 0})
    if not data:
        print("Not Ok")
    for r in k:
        ret[r] = data[r]
    return ret


@router.post("/data")
def front_post_data(data: HeartRate):
    hb_collection.update_one({}, {"$set" :{"name":data.name, "birth":data.birth}})
    return {"name":data.name, "birth":data.birth}

def calculate_maxrate():
    hr = hb_collection.find_one({}, {"_id": False})
    birth = hr["birth"]
    # print(birth)
    year = datetime.datetime.strptime(birth, '%Y-%m-%d').year
    current_year = datetime.datetime.now().year
    age = current_year - year
    max_rate = 207 - (age*0.7)
    return max_rate

def get_status():
    d = hb_collection.find_one({}, {"_id": 0})
    m = d["mode"]
    hard_rate = d["current_heartrate"]
    max_rate = calculate_maxrate()
    status = 999
    if m == 0:
        if (hard_rate > 110 or hard_rate < 30): #red
            status = 2
        elif ((hard_rate > 100 and hard_rate < 110) or (hard_rate < 60 and hard_rate > 30)): #yellow
            status = 1
        elif (hard_rate < 100 or hard_rate > 60): #less than 70% green
            status = 0
    elif m == 1:
        if (hard_rate > max_rate*0.8 or hard_rate < 30): #red
            status = 2
        elif ((hard_rate > max_rate*0.7 and hard_rate < max_rate*0.8)  or (hard_rate < 60 and hard_rate > 30)): #yellow
            status = 1
        elif (hard_rate < max_rate*0.7 or hard_rate > 60): #less than 70% green
            status = 0
    return status


@router.get("/get_status")
def front_get_status():
    return {"status": get_status()}

@router.get("/mode")
def front_get_mode():
    md = hb_collection.find_one({}, {"_id": False})
    return {"mode": md["mode"]}

@router.get("/get_heartrate")
def get_heartrate():
    md = hb_collection.find_one({}, {"_id": False})
    return {"current_heartrate": md["current_heartrate"]}

@router.get("/get_excercise_heartrate")
def front_get_excercise():
    md = list(hb_collection.find({}, {"_id": False}))
    return md[0]["excercise_heartrate"]

@router.get("/get_normal_heartrate")
def front_get_normal():
    md = list(hb_collection.find({}, {"_id": False}))
    return md[0]["normal_heartrate"]

@router.get("/get_all_heartrate")
def front_get_all():
    md = list(hb_collection.find({}, {"_id": False}))
    return md[0]["normal_heartrate"] + md[0]["excercise_heartrate"]


# @router.get("/status_excersice_mode")
# def hard_get_status():
#     hard_rate = get_field_from_hb_collection(["current_heartrate"])["current_heartrate"]
#     max_rate = calculate_maxrate()
#     # Mock status
#     if (hard_rate > max_rate*0.8): #red
#         status = 2
#     elif (hard_rate > max_rate*0.7 and hard_rate < max_rate*0.8): #yellow
#         status = 1
#     elif (hard_rate < max_rate*0.7): #less than 70% green
#         status = 0
#     return {"status": status}

# @router.get("/status_normal_mode")
# def hard_get_status():
#     hard_rate = get_field_from_hb_collection(["current_heartrate"])["current_heartrate"]
#     # Mock status
#     if (hard_rate > 110): #red
#         status = 2
#     elif (hard_rate > 100 and hard_rate < 110): #yellow
#         status = 1
#     elif (hard_rate < 100): #less than 70% green
#         status = 0
#     return {"status": status}

# print(front_get_excercise())
# print(type(calculate_maxrate()))





