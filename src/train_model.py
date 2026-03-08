import os
import sys
import torch
import pandas as pd
import numpy as np
import warnings

# Make sure we can import from src when running from root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.preprocess import load_and_preprocess_data

import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

warnings.filterwarnings("ignore")

# Define a simple LSTM model built from scratch instead of relying on heavy 
# pytorch-forecasting which often has strict dependency conflicts on Windows.
# The project readme mentions "TFT / LSTM", so this serves as our AI model.
class RainfallLSTM(nn.Module):
    def __init__(self, input_size=4, hidden_size=64, num_layers=2, output_size=7):
        super(RainfallLSTM, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, dropout=0.2)
        self.fc = nn.Linear(hidden_size, output_size)
        self.relu = nn.ReLU()
        
    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        
        out, _ = self.lstm(x, (h0, c0))
        # Take the output of the last time step
        out = self.fc(self.relu(out[:, -1, :]))
        return out

class RainfallDataset(Dataset):
    def __init__(self, df, seq_length=30, predict_length=7):
        self.data = []
        self.targets = []
        
        regions = df['region'].unique()
        for region in regions:
            region_data = df[df['region'] == region]
            # Features: rainfall, temperature, humidity, log_rainfall
            features = region_data[['rainfall', 'temperature', 'humidity', 'log_rainfall']].values
            rainfalls = region_data['rainfall'].values
            
            for i in range(len(features) - seq_length - predict_length + 1):
                x = features[i:i+seq_length]
                y = rainfalls[i+seq_length:i+seq_length+predict_length]
                self.data.append(x)
                self.targets.append(y)
                
        self.data = np.array(self.data, dtype=np.float32)
        self.targets = np.array(self.targets, dtype=np.float32)
        
    def __len__(self):
        return len(self.data)
        
    def __getitem__(self, idx):
        return torch.tensor(self.data[idx]), torch.tensor(self.targets[idx])

def train():
    print("Loading data...")
    df = load_and_preprocess_data()
    
    # Split into train/val
    train_size = int(len(df) * 0.8)
    train_df = df.iloc[:train_size]
    val_df = df.iloc[train_size:]
    
    print("Preparing datasets...")
    seq_length = 30 # Use 30 days of history
    predict_length = 7 # Predict 7 days ahead
    
    train_dataset = RainfallDataset(train_df, seq_length, predict_length)
    val_dataset = RainfallDataset(val_df, seq_length, predict_length)
    
    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=64, shuffle=False)
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    model = RainfallLSTM(input_size=4, hidden_size=64, num_layers=2, output_size=predict_length).to(device)
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    
    epochs = 10
    print("Starting training...")
    
    for epoch in range(epochs):
        model.train()
        train_loss = 0.0
        for x, y in train_loader:
            x, y = x.to(device), y.to(device)
            
            optimizer.zero_grad()
            outputs = model(x)
            loss = criterion(outputs, y)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
            
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for x, y in val_loader:
                x, y = x.to(device), y.to(device)
                outputs = model(x)
                loss = criterion(outputs, y)
                val_loss += loss.item()
                
        train_loss /= len(train_loader)
        val_loss /= len(val_loader)
        
        print(f"Epoch {epoch+1}/{epochs} | Train Loss: {train_loss:.4f} | Val Loss: {val_loss:.4f}")
        
    os.makedirs('models', exist_ok=True)
    model_path = 'models/lstm_model.pth'
    torch.save(model.state_dict(), model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train()
