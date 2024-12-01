from pydantic import BaseModel, Field, RootModel
from fastapi import Query
from typing import Dict


class PriceRequest(BaseModel):
    """Поля фильтрации страховки"""
    date: str = Field(Query(..., example="2020-06-03", description="Фильтрация по дате, формат 'YYYY-MM-DD'"))
    cargo_type: str = Field(Query(..., example="Glass", description="Фильтрация по страховке"))


class PriceResponse(BaseModel):
    """Получение стоимости страхования"""
    rate_info: str = Field(examples=["41.5"])


class PriceResponseNotFount(BaseModel):
    """Формат ошибки при отсутствии данных"""
    massage: str = Field(examples=["Rate not found"])


class ServerError(BaseModel):
    """Формат ошибки сервера"""
    massage: str = Field(examples=["INTERNAL_SERVER_ERROR"])


class Category(BaseModel):
    """Описание типа страховке и тарифа"""
    cargo_type: str
    rate: str


class RateRequest(RootModel):
    """Формат типа страховки по дате в формате YYYY-MM-DD"""
    root: Dict[str, list[Category]]


class RateResponse(BaseModel):
    """Формат ответа при успешном добавлении информации о страховке"""
    message: str = "The data has been successfully added to the database"


class RateEditResponse(BaseModel):
    """Формат ответа при успешном изменении информации о страховке."""
    message: str = "Rate edited successfully"


class Rate(BaseModel):
    """Поля страховки"""
    date: str
    cargo_type: str
    rate: str
    price_id: int
