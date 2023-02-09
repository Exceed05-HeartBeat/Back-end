from fastapi import APIRouter
from database import db, hb_collection
router = APIRouter(prefix="/hard")

@router.get("/get_status")
def hard_get_status():
    print(db.list_collection_names())
    return {"status": 1}

