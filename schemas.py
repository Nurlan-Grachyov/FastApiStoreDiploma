import re

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    username: str = Field(..., max_length=50, description="Напишите свое ФИО")
    email_or_phone: EmailStr | str = Field(
        ...,
        description="Введите email или номер телефона. Телефон должен быть в формате +7XXXXXXXXXX",
    )
    password: str = Field(..., min_length=8)
    password_confirm: str = Field(..., min_length=8)

    @field_validator("email_or_phone")
    def validator_email_or_phone(cls, v):
        if v.isdigit():
            if not re.match(r"^\+7\d{10}$", v):
                raise ValueError("Телефон должен начинаться с +7 и содержать 10 цифр.")
            return v
        else:
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

    @field_validator("password_confirm")
    def passwords_match(cls, v, values):
        if "password" in values and v != values["password"]:
            raise ValueError("Пароли не совпадают")
        return v


class UserRead(BaseModel):
    email_or_phone: EmailStr | str


class Token(BaseModel):
    access_token: str
    token_type: str
