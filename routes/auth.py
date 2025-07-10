from fastapi import APIRouter, Request
from controllers.auth import login, register,adminRegister
from models.user import User

authRouter = APIRouter()

@authRouter.post('/login')
async def login_route(req: Request):
    body = await req.json()
    convertedReq = User(**body)
    return await login(convertedReq)

@authRouter.post('/register')
async def register_route(req: Request):
    body = await req.json() 
    convertedReq = User(**body)  
    return await register(convertedReq)

@authRouter.put('/adminRegister')
async def adminRegister_route():
    await adminRegister()
    return {"message": "Admins registered successfully"}