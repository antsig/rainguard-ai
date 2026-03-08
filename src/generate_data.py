import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_synthetic_rainfall(output_path="data/rainfall_dataset.csv"):
    np.random.seed(42)
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2025, 12, 31)
    
    date_range = pd.date_range(start=start_date, end=end_date)
    from src.fetch_bmkg import BMKG_URLS
    regions = list(BMKG_URLS.keys())
    
    records = []
    
    for region in regions:
        for date in date_range:
            # Simulate seasonality: wet season (Nov-April), dry season (May-Oct)
            month = date.month
            
            if region == "Bandung":
                base_prob = 0.4
                base_amount = 10
            elif region == "Surabaya":
                base_prob = 0.2
                base_amount = 8
            else:
                base_prob = 0.3
                base_amount = 12
            
            if month in [11, 12, 1, 2, 3, 4]:
                # Wet season
                prob_rain = base_prob * 1.5
                avg_rain = base_amount * 2.0
            else:
                # Dry season
                prob_rain = base_prob * 0.5
                avg_rain = base_amount * 0.5
                
            is_raining = np.random.rand() < prob_rain
            if is_raining:
                # Gamma distribution for rainfall amount
                rainfall = np.random.gamma(shape=2.0, scale=avg_rain/2.0)
                
                # Introduce occasional extreme events (outliers) during wet season
                if month in [12, 1, 2] and np.random.rand() < 0.05:
                    rainfall += np.random.uniform(50, 100)
            else:
                rainfall = 0.0
                
            # Simulate some basic weather indicators (temperature, humidity)
            temp = np.random.normal(28, 2) if is_raining else np.random.normal(32, 2)
            if region == "Bandung":
                temp -= 5
                
            humidity = np.random.normal(85, 5) if is_raining else np.random.normal(65, 10)
            humidity = min(100, max(0, humidity))
            
            records.append({
                "date": date,
                "region": region,
                "rainfall": round(rainfall, 2),
                "temperature": round(temp, 1),
                "humidity": round(humidity, 1)
            })
            
    df = pd.DataFrame(records)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} records for {len(regions)} regions at {output_path}")

if __name__ == "__main__":
    generate_synthetic_rainfall()
