from motor.motor_asyncio import AsyncIOMotorClient

#db url
MONGO_URL = "mongodb://localhost:27017"
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
