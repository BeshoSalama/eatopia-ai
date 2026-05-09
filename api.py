from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from eatopia_ai_cli import build_diet_plan, scan_food
from pydantic import BaseModel
import shutil
import os
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


class DietRequest(BaseModel):
    age: int
    weight: float
    height: float
    activity: str
    goal: str
    durationDays: int = 7


@app.get("/")
def root():
    return {
        "message": "Eatopia AI API Running",
        "contract": "multipart-scan-v2"
    }


@app.post("/diet-plan")
def diet_plan(data: DietRequest):
    result = build_diet_plan(data.dict())
    return result


@app.post("/scan-food")
async def scan_food_api(image: UploadFile = File(...)):
    try:
        file_extension = image.filename.split(".")[-1]
        unique_name = f"{uuid.uuid4()}.{file_extension}"

        file_path = os.path.join(UPLOAD_FOLDER, unique_name)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        result = scan_food({
            "imagePath": file_path
        })

        return {
            "success": True,
            "result": result,
            "data": result
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }
