from fastapi import FastAPI
from pydantic import BaseModel
from eatopia_ai_cli import build_diet_plan, scan_food

app = FastAPI()


class DietRequest(BaseModel):
    age: int
    weight: float
    height: float
    activity: str
    goal: str
    durationDays: int = 7


class ScanRequest(BaseModel):
    imagePath: str


@app.get("/")
def root():
    return {"message": "Eatopia AI API Running"}


@app.post("/diet-plan")
def diet_plan(data: DietRequest):
    result = build_diet_plan(data.dict())
    return result


@app.post("/scan-food")
def scan_food_api(data: ScanRequest):
    result = scan_food(data.dict())
    return result