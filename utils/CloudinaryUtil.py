import cloudinary
from cloudinary.uploader import upload

#cloundinary configuration
cloudinary.config(
    cloud_name = "dzxy8gdi2",
    api_key="999815515312319",
    api_secret="cPnawrWAXH_JObfZUeCv05g0n_w"
)

#util functionn...

# async def upload_image(image):
#     result = upload(image)
#     print("cloundianry response,",result)
#     return result["secure_url"] #string

    
async def upload_image(file_path):
    """Upload an image to Cloudinary and return the URL."""
    try:
        # Upload the file to Cloudinary
        result = cloudinary.uploader.upload(file_path)
        # Return the secure URL
        return result["secure_url"]
    except Exception as e:
        print(f"Cloudinary upload error: {str(e)}")
        raise Exception(f"Failed to upload image: {str(e)}")