import pickle
import os

# Define model paths
MODEL_PATHS = {
    "Chairs": "models/model_pkl/Furniture_Chairs_sarima_model.pkl",
    "Bookcases": "models/model_pkl/Furniture_Bookcases_sarima_model.pkl",
    "Furnishings": "models/model_pkl/Furniture_Furnishings_sarima_model.pkl",
    "Tables": "models/model_pkl/Furniture_Tables_sarima_model.pkl",
    "Appliances": "models/model_pkl/Office Supplies_Appliances_sarima_model.pkl",
}

# Load models
models = {}
for product, path in MODEL_PATHS.items():
    with open(path, "rb") as f:
        models[product] = pickle.load(f)
