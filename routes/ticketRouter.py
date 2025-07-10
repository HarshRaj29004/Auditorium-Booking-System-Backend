from fastapi import APIRouter, Body, Depends, UploadFile, File, Form, Query
from controllers.ticketController import CreateTicket, UpdateFormStatus, FetchTickets, FetchBooked
from enums.requestStatus import ReqStatus
from middleware.jwtVerify import jwt_required
from typing import Optional

ticketRouter = APIRouter()

# ✅ Create Ticket — using multipart/form-data
@ticketRouter.post("/createticket")
async def create_ticket(
    file: UploadFile = File(...),
    name: str = Form(...),
    email: str = Form(...),
    mobileno: str = Form(...),
    eventdescription: str = Form(...),
    date: str = Form(...),
    requestType: str = Form(...),
    clubname: str = Form(None),
    startTime: str = Form(...),
    endTime: str = Form(...),
    user=Depends(jwt_required)
):
    ticket_data = {
        "name": name,
        "email": email,
        "mobileno": mobileno,
        "eventdescription": eventdescription,
        "date": date,
        "requestType": requestType,
        "clubname": clubname,
        "startTime": startTime,
        "endTime": endTime,
    }
    return await CreateTicket(ticket_data, file, user["_id"])


# ✅ Update status of a ticket
@ticketRouter.put("/updateticket/{ticket_id}")
async def update_ticket_status(
    ticket_id: str,
    new_status: ReqStatus,
    user=Depends(jwt_required)
):
    return await UpdateFormStatus(ticket_id, new_status, user)


# ✅ Fetch tickets
@ticketRouter.get("/fetchTicket")
async def fetch_tickets(
    status: Optional[str] = Query(None),
    date: Optional[str] = Query(None),
    user=Depends(jwt_required)
):
    return await FetchTickets(user, date, status)

@ticketRouter.get("/fetchBooked")
async def fetch_booked(
    date: Optional[str] = Query(None)
):
    return await FetchBooked(date)
