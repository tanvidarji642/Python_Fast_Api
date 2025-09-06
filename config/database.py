
import os
import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient


# Get MongoDB URL from environment variable, ensure correct formatting
MONGO_URL = os.environ.get("MONGODB_URL")
if not MONGO_URL:
    raise ValueError("MONGODB_URL environment variable is not set. Please set it in your Render dashboard as just the connection string, e.g. mongodb+srv://user:pass@host/db?options, with no spaces or variable name.")
if MONGO_URL.strip().startswith("MONGODB_URL"):
    raise ValueError("MONGODB_URL environment variable is incorrectly set. Only use the connection string as the value, not 'MONGODB_URL = ...'.")
DATABASE_NAME = "internship_fast"

client = AsyncIOMotorClient(MONGO_URL)
db = client[DATABASE_NAME]
role_collection = db["roles"]
user_collection = db["users"]
department_collection = db["departments"]
employee_collection = db["employees"]
state_collection = db["states"]
city_collection = db["cities"]
category_collection = db["categories"]
sub_category_collection = db["sub_categories"]
area_collection = db["areas"]
location_collection = db["locations"]
area_collection = db["areas"]
offer_collection = db["offers"]
product_collection = db["products"]
rating_collection = db["ratings"]
restaurant_collection = db["restaurant"]


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render sets the PORT env variable
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
