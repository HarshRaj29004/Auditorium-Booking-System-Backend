from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.auth import authRouter
from routes.ticketRouter import ticketRouter
from utils.utils import FRONTEND_URL

app = FastAPI()

origins = [
    "https://auditorium-booking-system-frontend.vercel.app/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       
    allow_credentials=True,
    allow_methods=["*"],            
    allow_headers=["*"],          
)

app.include_router(authRouter, prefix='/auth')
app.include_router(ticketRouter, prefix='/ticket')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
