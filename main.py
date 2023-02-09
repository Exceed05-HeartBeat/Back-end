from fastapi import FastAPI, Body, HTTPException
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from typing import Optional
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
load_dotenv(".env")

USER = os.getenv("username")
PASSWORD = os.getenv("password")
client = MongoClient(f"mongodb://{USER}:{PASSWORD}@mongo.exceed19.online:8443/?authMechanism=DEFAULT")

db = client["exceed05"]
hb_collection = db["heart-beat"]


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"Hi": "world"}

# Global Variables
# 0 -> normal 1 -> warn 2 -> danger
STATUS: int = 0

# Hard
@app.get("/hard/get_status")
def hard_get_status():
    return {"status": STATUS}





















# Front
