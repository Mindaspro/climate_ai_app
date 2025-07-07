# train_model.py

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
import joblib

# Load your cleaned training data
data = pd.read_csv("data/training_data.csv")  # This should have crop, soil, rainfall, etc.

# Prepare features and target
X = pd.get_dummies(data.drop("yield", axis=1))
y = data["yield"]

# Train the model
model = RandomForestRegressor()
model.fit(X, y)

# Save model and feature names
joblib.dump(model, "models/yield_predictor.pkl")
joblib.dump(list(X.columns), "models/model_columns.pkl")

print("✅ Model trained and saved.")