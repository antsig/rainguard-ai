import torch
import pandas as pd
import numpy as np
from src.preprocess import load_and_preprocess_data
from src.train_model import RainfallLSTM

def predict_rainfall(region: str, days=7):
    """
    Predict rainfall for the next `days` days for a specific region.
    """
    # Load recent data
    df = load_and_preprocess_data()
    region_data = df[df['region'] == region]
    
    if len(region_data) < 30:
        raise ValueError(f"Not enough historical data for {region}")
    
    # Get the last 30 days
    recent_data = region_data.tail(30)
    features = recent_data[['rainfall', 'temperature', 'humidity', 'log_rainfall']].values
    
    # Prepare tensor
    x = torch.tensor(features, dtype=torch.float32).unsqueeze(0) # shape (1, 30, 4)
    
    # Load model
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = RainfallLSTM(input_size=4, hidden_size=64, num_layers=2, output_size=7).to(device)
    
    try:
        model.load_state_dict(torch.load('models/lstm_model.pth', map_location=device))
    except FileNotFoundError:
        print("Model not found. Returning dummy predictions.")
        return [round(np.random.uniform(0, 50), 2) for _ in range( days)]
        
    model.eval()
    with torch.no_grad():
        x = x.to(device)
        output = model(x)
        predictions = output.squeeze(0).cpu().numpy()
        
    # Ensure no negative predictions
    predictions = np.maximum(predictions, 0)
    # Round to 2 decimal places
    predictions = np.round(predictions, 2)
    
    # If the user asks for more than 7 days, we pad or truncate
    if days > 7:
        # Just repeat the last value
        extra = np.full(days - 7, predictions[-1])
        predictions = np.concatenate([predictions, extra])
    return predictions[:days].tolist()

if __name__ == "__main__":
    region = "Jakarta"
    preds = predict_rainfall(region)
    print(f"7-day Rainfall Prediction for {region}: {preds}")
