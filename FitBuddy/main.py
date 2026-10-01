from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import ai_service
import database

app = FastAPI(title="FitBuddy AI")
templates = Jinja2Templates(directory="FitBuddy/templates")
database.init_db()

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
def generate(name: str = Form(...), age: int = Form(...), weight: float = Form(...), goal: str = Form(...), intensity: str = Form(...)):
    plan = ai_service.generate_workout_plan(age, weight, goal, intensity)
    tips = ai_service.generate_nutrition_tips(goal)
    database.save_user(name, age, weight, goal, intensity, plan, tips)
    return {"status": "success", "plan": plan, "nutrition": tips}

@app.get("/admin/users")
def all_users():
    return database.get_all_users()
  
