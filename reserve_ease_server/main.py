from datetime import datetime, timedelta
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

from reserve_ease_server.connect_supabase import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
supabase = connect_supabase()


class UserInfo(BaseModel):
    supabase_id: str
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str


class ReservationData(BaseModel):
    user_id: str
    start_date: datetime
    end_date: datetime
    title: str
    description: Optional[str] = None


@app.get("/")
def read_root():
    three_months_ago = datetime.now() - timedelta(days=90)
    one_year_future = datetime.now() + timedelta(days=365)

    events_response = (
        supabase.table("events")
        .select("id, title, start_date, end_date, description, user_id")
        .gte("start_date", three_months_ago.isoformat())
        .lte("start_date", one_year_future.isoformat())
        .execute()
    )

    if not events_response.data:
        raise HTTPException(status_code=400, detail="データの取得に失敗しました")

    for event in events_response.data:
        user_response = (
            supabase.table("users")
            .select("last_name")
            .eq("supabase_id", event["user_id"])
            .execute()
        )

        if user_response.data:
            event["last_name"] = user_response.data[0]["last_name"]
        else:
            event["last_name"] = "不明"

    return events_response.data


@app.post("/register-user-info")
async def register_user_info(user_info: UserInfo):
    response = (
        supabase.table("users")
        .insert(
            {
                "supabase_id": user_info.supabase_id,
                "first_name": user_info.first_name,
                "last_name": user_info.last_name,
                "email": user_info.email,
                "phone_number": user_info.phone_number,
            }
        )
        .execute()
    )

    return response


@app.post("/add-events")
async def create_event(reservation: ReservationData):
    reservation_data = jsonable_encoder(reservation)
    response = supabase.table("events").insert(reservation_data).execute()

    if not response.data:
        raise HTTPException(status_code=400, detail="データの挿入に失敗しました")

    return {"message": "予約が登録されました"}
