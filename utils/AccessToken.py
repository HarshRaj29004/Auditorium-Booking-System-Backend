from utils.utils import SECRET_KEY
import jwt
import datetime
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
from bson.objectid import ObjectId
from db.db import db

async def generate_access_token(user_id: str, role: str, email: str):
    try:
        # Generate JWT token
        payload = {
            "_id": str(user_id),
            "role": role,
            "email": email,
            "exp": datetime.utcnow() + timedelta(days=7)
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        # Fetch the user from DB
        user = db["User"].find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Trim tokens list to max 5
        tokens = user.get("tokens", [])
        if len(tokens) >= 5:
            tokens = tokens[1:] 

        tokens.append({
            "token": token,
            "createdAt": datetime.utcnow()
        })

        # Update user record
        db["User"].update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {"tokens": tokens, "lastLogin": datetime.utcnow()}
            }
        )

        return token

    except Exception as e:
        print("Token generation error:", str(e))
        raise HTTPException(status_code=500, detail="Unable to generate authentication token")
