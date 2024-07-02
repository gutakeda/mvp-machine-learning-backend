from typing import List
from pydantic import BaseModel, Field, field_validator
from decimal import Decimal
from enum import Enum

class TransactionType(str, Enum):
    WITHDRAW = 'withdraw'
    DEPOSIT = 'deposit'

class TransactionSchema(BaseModel):
    title: str
    type: TransactionType
    amount: Decimal = Field(..., gt=0, decimal_places=2)
    category_id: int

    @field_validator('title')
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Title must not be empty')
        return v

    @field_validator('type')
    def type_must_be_valid(cls, v):
        if v not in TransactionType._value2member_map_:
            raise ValueError('Type must be either "withdraw" or "deposit"')
        return v

class TransactionViewSchema(BaseModel):
    id: int
    title: str
    type: TransactionType
    amount: Decimal
    category_id: int
    created_at: str

class TransactionListResponse(BaseModel):
    transactions: List[TransactionViewSchema]

class TransactionDelSchema(BaseModel):
    transaction_id: int
