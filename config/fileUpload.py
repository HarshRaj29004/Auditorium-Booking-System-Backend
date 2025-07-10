import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from utils.utils import CLOUDINARY_API_KEY,CLOUDINARY_API_SECRET,CLOUD_NAME
from datetime import datetime

# Configuration       
cloudinary.config( 
    cloud_name = CLOUD_NAME, 
    api_key = CLOUDINARY_API_KEY, 
    api_secret = CLOUDINARY_API_SECRET,
    secure=True
)

def CloudinaryFileUpload(file: str):
    try:
        result = cloudinary.uploader.upload(
            file,
            folder="auditorium-pdfs",
            resource_type="auto",
            public_id=f"pdf-{int(datetime.now().timestamp())}",
            format="pdf",
        )

        # print("Upload result:", result)
        return result["secure_url"]

    except Exception as e:
        print("Cloudinary upload error:", e)
        raise e
