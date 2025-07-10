from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pymongo.errors import PyMongoError
from bson import ObjectId
from db.db import db
from enums.requestStatus import ReqStatus
from config.fileUpload import CloudinaryFileUpload
from tempfile import NamedTemporaryFile
from datetime import datetime, timedelta
from enums.requestType import ReqType
from enums.requestStatus import ReqStatus
from enums.role import role
import shutil
from bson import ObjectId
from bson.errors import InvalidId


async def CreateTicket(body, file,user_id):
    try:
        # Step 1: Save file temporarily
        with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            shutil.copyfileobj(file.file, tmp)
            temp_path = tmp.name
        print(body)
        # Step 2: Upload to Cloudinary
        file_url = CloudinaryFileUpload(temp_path)

        # Step 3: Build the ticket data
        data = {
            "username": body["name"],
            "email": body["email"],
            "mobileno": body["mobileno"],
            "user_id": user_id,
            "eventdescription": body["eventdescription"],
            "date": datetime.utcnow(), 
            "clubname": body["clubname"] if body["requestType"] == ReqType.CLUB.value else ReqType.TEACHER.value,
            "requestType": body["requestType"],
            "status": ReqStatus.PENDING,
            "approvedBy": None,
            "file": file_url,
            "startTime": body["startTime"],
            "endTime": body["endTime"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        # Step 4: Insert into MongoDB
        db["Ticket"].insert_one(data)

        return {"message": "Ticket uploaded successfully!"}
    except Exception as e:
        print("File Upload error:",str(e))
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")



# Update Ticket Status
async def UpdateFormStatus(ticket_id: str, new_status: ReqStatus,user):
    try:
        try:
            object_id = ObjectId(ticket_id)
        except InvalidId:
            raise HTTPException(status_code=400, detail="Invalid ticket ID format")

        ticket = db["Ticket"].find_one({ "_id": object_id })
        if not ticket:
            raise HTTPException(status_code=404, detail="Form (ticket) not found")

        # update logic here
        # print(user)
        db["Ticket"].update_one(
            { "_id": object_id },
            { "$set": {
                "status": new_status,
                "approvedBy": user['email']
            }}
        )

        return { "message": "Status updated successfully" }

    except Exception as e:
        print("UpdateStatus error:", str(e))
        raise HTTPException(status_code=400, detail=str(e))

# Fetch All Tickets
async def FetchTickets(user, selected_date=None, status=None):
    try:
        # print(user)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        query = {}
        
        if (status == ReqStatus.BOOKED.value) or (status == ReqStatus.DECLINED.value):
            query['status'] = status
        else:
            if user["role"] == role.SUBADMIN.value:
                query["requestType"] = str(ReqType.CLUB.value)
            elif user["role"] == role.SUPERADMIN.value:
                query["requestType"] = str(ReqType.TEACHER.value)
            else:
                query["user_id"] = user["_id"]

            # Optional filters
            if status:
                query["status"] = str(status)
            if selected_date:
                query["date"] = str(selected_date)

        tickets = list(db["Ticket"].find(query))
        # print("Tickets:", tickets)

        return jsonable_encoder(
            tickets,
            custom_encoder={ObjectId: str}
        )

    except Exception as e:
        print("Fetch Ticket error:", str(e))
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    

async def FetchBooked(date: str):
    try:
        # Convert string date (e.g., "2025-07-09") to datetime
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format, expected YYYY-MM-DD")

        start = date_obj
        end = date_obj + timedelta(days=1)

        tickets = list(
            db["Ticket"].find({
                "date": { "$gte": start, "$lt": end },
                "status": ReqStatus.BOOKED.value
            })
        )

        # print("Tickets:", tickets)

        return jsonable_encoder(
            tickets,
            custom_encoder={ObjectId: str}
        )
    except Exception as e:
        print("Fetch Booked error:", str(e))
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
