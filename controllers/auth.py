from models.user import User
from utils.AccessToken import generate_access_token
import bcrypt
from db.db import db
from enums.requestStatus import ReqStatus
from datetime import datetime
from fastapi import HTTPException
from pymongo.errors import PyMongoError
import traceback
from fastapi import status
from enums.role import role
from utils.utils import SUBADMINS,SUPERADMINS


async def login(req: User):
    try:
        email, password = req.email.lower(), req.password
        if not email or not password:
            raise HTTPException(status_code=400, detail="Email and password are required")

        user = db["User"].find_one({"email": email})
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        is_password_correct = bcrypt.checkpw(password.encode(), user["password"].encode())
        if not is_password_correct:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        # Generate JWT token
        token = await generate_access_token(user['_id'],user['role'],user['email'])

        # Save token + update last login
        db["User"].update_one(
            {"email": email},
            {
                "$set": {
                    "lastLogin": datetime.utcnow()
                },
                "$push": {
                    "tokens": {
                        "token": token,
                        "createdAt": datetime.utcnow()
                    }
                }
            }
        )

        # Prepare response (avoid sending hashed password)
        response_user = {
            "id": str(user["_id"]),
            "name": user["username"],
            "email": user["email"],
            "role": user["role"],
            "accessToken": token
        }

        return {"message": "Login successful!", "user": response_user}

    except Exception as e:
        print("Login Error:", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")



async def register(user: User):
    try:
        existing_user = db["User"].find_one({"email": user.email.lower()})
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        if user.role != role.USER:
            return {"message": "Ask Dean's office for registration. Only normal users can self-register."}

        hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()

        user_dict = user.dict()
        user_dict["username"] = user.username
        user_dict["password"] = hashed_password
        user_dict["created_at"] = datetime.utcnow()
        user_dict["updated_at"] = datetime.utcnow()

        db["User"].insert_one(user_dict)
        return {"message": "User registered successfully! Please wait for approval."}

    except Exception as e:
        print("Register Error:", str(e))  
        traceback.print_exc()            
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    
async def adminRegister():
    try:
        for email, password in SUPERADMINS:
            existing = db["User"].find_one({"email": email})
            if not existing:
                hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                dict_data = {
                    "email": email,
                    "username": "Admin",
                    "password": hashed_password,
                    "role": role.SUPERADMIN,
                    "token": [],
                    "lastLogin": None,
                    "isActive": False,
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
                db["User"].insert_one(dict_data)

        for email, password in SUBADMINS:
            existing = db["User"].find_one({"email": email})
            if not existing:
                hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

                db["User"].insert_one({
                    "email": email,
                    "username": "Admin",
                    "password": hashed_password,
                    "role": role.SUBADMIN,
                    "token": [],
                    "lastLogin": None,
                    "isActive": False,
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                })

    except Exception as e:
        print("Admin Register Error:", str(e)) 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to register super-admins: {str(e)}"
        )

