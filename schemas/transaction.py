from typing import List
from pydantic import BaseModel
from decimal import Decimal
from enum import Enum

class TransactionType(str, Enum):
    WITHDRAW = 'withdraw'
    DEPOSIT = 'deposit'

class TransactionSchema(BaseModel):
    age: int
    sex: int
    chest_pain_type : int
    resting_bp : int
    cholesterol : int
    fasting_bs : int
    resting_ecg : int
    max_hr : int
    exercise_angina : int
    oldpeak : int
    st_slope: int

class TransactionViewSchema(BaseModel):
    id: int
    age: int
    sex: int
    chest_pain_type : int
    resting_bp : int
    cholesterol : int
    fasting_bs : int
    resting_ecg : int
    max_hr : int
    exercise_angina : int
    oldpeak : int
    st_slope: int
    heart_disease: int
    created_at: str

class TransactionListResponse(BaseModel):
    transactions: List[TransactionViewSchema]

class TransactionDelSchema(BaseModel):
    transaction_id: int
