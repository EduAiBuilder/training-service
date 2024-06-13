from fastapi import APIRouter

router = APIRouter()

@router.get("/status")
async def read_status():
    return {"status": "App is runing"}
