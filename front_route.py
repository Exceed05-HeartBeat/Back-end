from fastapi import APIRouter, Body
from database import db, hb_collection
from database import HeartRate
# from datetime import datetime, timedelta, date
import datetime

router = APIRouter(prefix="/front")

@router.get("/get_status")
def front_get_status():
    return {"status": 1}

@router.get("/mode")
def front_get_mode():
    md = hb_collection.find_one({}, {"_id": False})
    return {"mode": md["mode"]}

@router.get("/get_heartrate")
def front_get_mode():
    md = hb_collection.find_one({}, {"_id": False})
    return {"current_heartrate": md["current_heartrate"]}

@router.get("/get_normal_heartrate")
def front_get_normal_heartrate():
    hr = hb_collection.find_one({}, {"_id": False})
    return hr["normal_heartrate"]

@router.get("/get_excercise_heartrate")
def front_get_normal_heartrate():
    hr = hb_collection.find_one({}, {"_id": False})
    return hr["excercise_heartrate"]

def calculate_maxrate():
    hr = hb_collection.find_one({}, {"_id": False})
    birth = hr["birth"]
    year = datetime.datetime.strptime(birth, '%Y-%m-%d').year
    current_year = datetime.datetime.now().year
    age = current_year - year
    max_rate = 207 - (age*0.7)
    return max_rate
#need to insert insteed of update
@router.post("/data")
def front_post_data(heartrate: HeartRate = Body()):
    hb_collection.update_one({}, {"$set" :{"name":heartrate.name, "birth":heartrate.birth}})
    # print(datetime.datetime.strptime(heartrate.birth, '%Y-%m-%d').year)
    return {"name":heartrate.name, "birth":heartrate.birth}
    # print(heartrate.name)
    # print(heartrate.birth)

# def calculate_maxrate():
#     hr = hb_collection.find_one({}, {"_id": False})
#     birth = hr["birth"]
#     year = datetime.datetime.strptime(birth, '%Y-%m-%d').year
#     return year
print(calculate_maxrate())





