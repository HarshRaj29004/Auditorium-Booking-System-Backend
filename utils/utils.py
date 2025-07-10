import os
from dotenv import load_dotenv

load_dotenv()

FRONTEND_URL = os.getenv("FRONTEND_URL")
MONGO_URL = os.getenv("MONGO_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
DB = os.getenv("DB")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")
CLOUD_NAME = os.getenv("CLOUD_NAME")

SUPERADMINS = [
    tuple(admin.strip().split(":"))
    for admin in os.getenv("SUPERADMINS", "").split(",")
    if ":" in admin
]

SUBADMINS = [
    tuple(admin.strip().split(":"))
    for admin in os.getenv("SUBADMINS", "").split(",")
    if ":" in admin
]
