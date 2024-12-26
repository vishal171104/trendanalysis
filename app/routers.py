from fastapi import APIRouter
from pydantic import BaseModel
import pickle
import os
import pandas as pd

router = APIRouter()

# Folder containing all the models (outside the app folder)
model_folder = os.path.join(os.getcwd(), "model_pkl")

# Sample warehouse data (You will replace this with your actual dataset)
warehouse_data = pd.read_csv('datasets/Updated_Orders_with_Unique_Vendors.csv')

class ProductRequest(BaseModel):
    product_name: str

def load_model(product_name: str):
    """
    Loads the model dynamically from the model_pkl directory
    based on the product name.
    """
    model_path = os.path.join(model_folder, f"{product_name}.pkl")
    
    # Check if model exists
    if not os.path.exists(model_path):
        raise ValueError(f"Model for product {product_name} not found.")
    
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    
    return model

@router.get("/trends/{product_name}")
async def get_trend_analysis(product_name: str):
    try:
        # Filter the dataset based on product_name to get trend-related information
        product_data = warehouse_data[warehouse_data["Item Purchased"] == product_name]

        if product_data.empty:
            return {"error": f"Product '{product_name}' not found in the dataset."}

        # Let's assume the 'Frequency of Purchases' column gives us a sense of trend.
        # You might want to further analyze trends over time (e.g., by date if your dataset has that info).

        trend_data = {
            "dates": product_data["Season"].unique().tolist(),  # Replace with actual trend-related data if available
            "values": product_data["Frequency of Purchases"].tolist(),  # You can use other columns as needed
        }
        
        return {"product_name": product_name, "trend": trend_data}

    except ValueError as e:
        return {"error": str(e)}

@router.get("/warehouses")
async def get_warehouses():
    # Return a list of available warehouses from the dataset
    warehouses = warehouse_data["Location"].unique().tolist()  # Assuming warehouse info is in 'Location' column
    return {"warehouses": warehouses}

@router.post("/store_product")
async def store_product(product_name: str, warehouse_name: str, product_size: int):
    try:
        # Fetch the warehouse details
        warehouse = warehouse_data[warehouse_data["Location"] == warehouse_name]

        if warehouse.empty:
            return {"error": "Warehouse not found."}

        # Calculate remaining space using a space optimization model
        model = load_model("space_optimizer")  # Assuming you have a general space optimizer model
        remaining_space = warehouse["Size"].iloc[0] - product_size
        
        # If the model requires more complex calculations, call it here:
        optimized_remaining_space = model.optimize(remaining_space)  # Example, adjust based on your model

        # Update warehouse data with the remaining space (store it back to CSV or DB)
        warehouse_data.loc[warehouse_data["Location"] == warehouse_name, "Size"] = optimized_remaining_space
        
        return {"message": f"Product {product_name} stored in {warehouse_name}.", 
                "remaining_space": optimized_remaining_space}

    except ValueError as e:
        return {"error": str(e)}
