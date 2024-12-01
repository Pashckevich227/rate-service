from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Body, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from schemas import (PriceResponse,
                     PriceResponseNotFount,
                     PriceRequest,
                     RateRequest,
                     ServerError,
                     RateResponse,
                     Rate,
                     RateEditResponse)
from exemples import example_rate
from crud import get_price, create_rate, edit_data, delete_data
from database import get_async_session
import json

app = FastAPI()

responses_error = {500: {"model": ServerError}}


@app.get("/price",
         status_code=status.HTTP_200_OK,
         response_model=PriceResponse,
         responses={404: {"model": PriceResponseNotFount}},
         tags=["rate"],
         summary="Получить информацию о цене тарифа")
async def price_rate(filter: PriceRequest = Depends(),
                     db: AsyncSession = Depends(get_async_session)):
    try:
        data = await get_price(date=filter.date,
                               cargo_type=filter.cargo_type,
                               db=db)
        return {"rate_info": data}
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rate not found")


@app.post("/rate",
          status_code=status.HTTP_201_CREATED,
          response_model=RateResponse,
          responses=responses_error,
          tags=["rate"],
          summary="Добавить данные о товаре и страховке из body")
async def rate(info: Annotated[RateRequest, Body(openapi_examples=example_rate)],
               db: AsyncSession = Depends(get_async_session)):
    """
        <b>Присутствует проверка на уникальность данных</b>

        Если date и cargo_type уже есть в базе, то такие данные не добавятся
    """
    try:
        data = await create_rate(info=info, db=db)
        return {"massage": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/rate/file",
          status_code=status.HTTP_201_CREATED,
          response_model=RateResponse,
          responses=responses_error,
          tags=["rate"],
          summary="Добавить данные о товаре и страховке из файла")
async def rate_file(upload_file: UploadFile = File(..., description="Файл с данными о страховке"),
                    db: AsyncSession = Depends(get_async_session)):
    try:
        data_file = json.load(upload_file.file)
        data_serialize = RateRequest(data_file)
        is_created = await create_rate(info=data_serialize, db=db)
        return {"massage": is_created}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.patch('/rate',
           status_code=status.HTTP_200_OK,
           response_model=RateEditResponse,
           responses=responses_error,
           tags=["rate"],
           summary="Изменить данные о товаре и страховке")
async def edit_rate(id: int = Query(..., example=22),
                    edit_info: Rate = Body(),
                    db: AsyncSession = Depends(get_async_session)):
    """
        Здесь можно задать стоимость страховки <b>price_id</b>:
        - **1**: Glass - 100
        - **2**: Other - 50
        - **3**: Car - 200
    """
    data = await edit_data(id=id, edit_info=edit_info, db=db)
    if data:
        return {"message": "Rate edited successfully"}
    else:
        return {"message": "Rate not found"}


@app.delete("/rate",
            status_code=status.HTTP_200_OK,
            responses=responses_error,
            tags=["rate"],
            summary="Удалить данные о товаре и страховке")
async def delete_rate(id: int,
                      db: AsyncSession = Depends(get_async_session)):
    if await delete_data(id=id, db=db):
        return {"message": "Rate deleted successfully"}
    else:
        return {"message": "Rate not found"}
