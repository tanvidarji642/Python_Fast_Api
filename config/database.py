import os
import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient

#db url
# MONGO_URL = "mongodb+srv://darjitanvi642:IxgKwZrdvmBlXwd9@cluster0.dgsasfo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
MONGO_URL = os.environ.get("MONGODB_URL")
if not MONGO_URL:
    raise ValueError("MONGODB_URL environment variable is not set")
DATABASE_NAME ="internship_fast"

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

# image_collection = db["images"]
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render sets the PORT env variable
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
