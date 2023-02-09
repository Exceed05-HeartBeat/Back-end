from fastapi import APIRouter
from database import db, hb_collection

router = APIRouter(prefix="/front")

@router.get("/get_status")
def front_get_status():
    return {"status": 1}
