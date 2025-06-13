import re
from typing import Optional

from fastapi_users import schemas
from pydantic import (BaseModel, EmailStr, Field, field_validator,
                      model_validator)
from pydantic_core.core_schema import ValidationInfo


class UserCreate(schemas.BaseUserCreate):
    username: str = Field(..., max_length=150, description="Напишите свое ФИО")
    phone: str = Field(..., description="Телефон должен быть в формате +7XXXXXXXXXX")
    email: EmailStr = Field(
        ..., max_length=100, description="Введите email в формате username@example.com"
    )
    password: str = Field(..., min_length=8)
    password_confirm: str = Field(..., min_length=8)

    @field_validator("phone")
    def validator_email_or_phone(cls, v):
        if not re.match(r"^\+7\d{10}$", v):
            raise ValueError("Телефон должен начинаться с +7 и содержать 10 цифр.")
        return v

    @field_validator("password")
    def validator_password(cls, v):
        if not re.search(r"[A-Za-z]", v):
            raise ValueError("Пароль должен содержать хотя бы одну латинскую букву")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Пароль должен содержать хотя бы одну заглавную букву")
        if not re.search(r"[$%&!:]", v):
            raise ValueError(
                "Пароль должен содержать хотя бы один спецсимвол: $, %, &, !, :"
            )
        return v

    @model_validator(mode="after")
    def check_passwords(cls, obj: "UserCreate"):
        if obj.password != obj.password_confirm:
            raise ValueError("Пароли не совпадают")
        delattr(obj, "password_confirm")
        return obj


class UserRead(schemas.BaseUser):
    phone: str
    email: EmailStr


class UserUpdate(schemas.BaseUserUpdate):
    phone: str | None
    email: EmailStr | None
    password: str | None
    username: str | None
    password_confirm: str | None


class Token(BaseModel):
    access_token: str
    token_type: str


class UserLogin(BaseModel):
    phone: Optional[str]
    email: Optional[EmailStr]
    password: str

    @model_validator(mode="after")
    def check_email_or_phone(cls, instance, info: ValidationInfo):
        if not (instance.phone or instance.email):
            raise ValueError(
                "Необходимо заполнить хотя бы один из полей: телефон или e-mail."
            )
        return instance
