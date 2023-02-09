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
bulb_collecton = db["heart-beat"]


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