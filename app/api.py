from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
import os

# Ensure the parent directory is in the sys.path so we can import src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.predict import predict_rainfall
from src.risk_classifier import classify_risk, get_recommendations
from src.fetch_bmkg import get_realtime_weather

app = FastAPI(
    title="RainGuard AI API",
    description="Sistem peringatan dini risiko banjir berbasis prediksi curah hujan AI",
    version="1.0.0"
)

class RiskRequest(BaseModel):
    region: str
    days: int = 7

class DailyForecast(BaseModel):
    day: int
    rainfall_mm: float
    risk_level: str

class RiskResponse(BaseModel):
    region: str
    overall_risk_today: str
    recommendations: list[str]
    forecast: list[DailyForecast]
    bmkg_realtime: dict

@app.get("/")
def read_root():
    return {"message": "Selamat datang di RainGuard AI API. Gunakan endpoint /predict untuk melihat perkiraan."}

@app.post("/predict", response_model=RiskResponse)
def predict(request: RiskRequest):
    try:
        # Get rainfall predictions
        predictions = predict_rainfall(request.region, days=request.days)
        
        forecast = []
        for i, rain in enumerate(predictions):
            risk = classify_risk(rain)
            forecast.append(DailyForecast(
                day=i+1,
                rainfall_mm=rain,
                risk_level=risk
            ))
            
        # Today's risk is based on Day 1 prediction
        today_risk = forecast[0].risk_level
        recs = get_recommendations(today_risk)
        
        # Fetch BMKG real-time data
        bmkg_data = get_realtime_weather(request.region)
        
        return RiskResponse(
            region=request.region,
            overall_risk_today=today_risk,
            recommendations=recs,
            forecast=forecast,
            bmkg_realtime=bmkg_data
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
