from fastapi import FastAPI
from routes.RoleRoutes import router as role_router
from routes.UserRoutes import router as user_router
from routes.DepartmentRoutes import router as department_router
from routes.EmployeeRoutes import router as employee_router
from routes.StateRoutes import router as state_router
from routes.CityRoutes import router as city_router
from routes.CategoryRoutes import router as category_router
from routes.SubCategoryRoutes import router as sub_category_router
from routes.AreaRoutes import router as area_router
from routes.LocationRoute import router as location_router
from routes.OfferRoute import router as offer_router
from routes.ProductRoutes import router as product_router
from routes.RatingRoutes import router as rating_router


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(role_router, tags=["Role"])
app.include_router(user_router, tags=["User"])
app.include_router(department_router, tags=["Department"])
app.include_router(employee_router, tags=["Employee"])
app.include_router(state_router, tags=["Satate"])
app.include_router(city_router, tags=["city"])
app.include_router(category_router, tags=["Category"])
app.include_router(sub_category_router)
app.include_router(area_router, tags=["Area"])
app.include_router(location_router, tags=["Location"])
app.include_router(offer_router, tags=["Offer"])
app.include_router(product_router, tags=["Product"])
app.include_router(rating_router, tags=["Rating"])