from fastapi import FastAPI, Body, HTTPException
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from typing import Optional
from pymongo import MongoClient
from fastapi.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
import front_route
import hard_route
from database import db, hb_collection

origins = ["*"]
middleware = [
    Middleware(CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])
]

app = FastAPI(middleware=middleware)
app.include_router(front_route.router)
app.include_router(hard_route.router)



@app.get("/")
def root():
    return {"Hi": "world"}

@app.get("/get_status")
def hard_get_status():
    status = hard_route.get_status()
    return {"status": status}
