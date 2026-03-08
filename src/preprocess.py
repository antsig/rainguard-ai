import pandas as pd
import numpy as np

def load_and_preprocess_data(csv_path="data/rainfall_dataset.csv"):
    """
    Load data from CSV and add necessary time features for TimeSeriesDataSet.
    """
    df = pd.read_csv(csv_path)
    
    # Ensure date is datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Add time index (required by PyTorch Forecasting)
    # We group by region and create a sequence of integer timesteps
    df = df.sort_values(by=['region', 'date'])
    df['time_idx'] = df.groupby('region').cumcount()
    
    # Add calendar features
    df['month'] = df['date'].dt.month.astype(str).astype('category')
    df['day_of_week'] = df['date'].dt.dayofweek.astype(str).astype('category')
    df['day_of_year'] = df['date'].dt.dayofyear
    
    # Region as category
    df['region'] = df['region'].astype('category')
    
    # Handle any missing values just in case
    df = df.fillna(method='ffill')
    
    # Add log of rainfall to reduce extreme variance impact
    df['log_rainfall'] = np.log1p(df['rainfall'])
    
    return df

if __name__ == "__main__":
    df = load_and_preprocess_data()
    print("Preprocessed data shape:", df.shape)
    print("Columns:", df.columns.tolist())
    print("Sample:\n", df.head())
