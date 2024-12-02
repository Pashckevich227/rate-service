from sqlalchemy import select
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models import Rate, Price


async def get_price(date: str,
                    cargo_type: str,
                    db: AsyncSession):
    """Получение стоимости страхования по date и cargo_type"""
    try:
        data = await db.execute(
            select(Rate.rate, Rate.price_id, Price.price).join(Price, Rate.price_id == Price.id)
            .where(Rate.date == date)
            .where(Rate.cargo_type == cargo_type)
        )
        result = data.first()
        rate, price_id, price = result
        return str(price * float(rate))

    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))
    finally:
        await db.close()


async def create_rate(info,
                      db: AsyncSession):
    """Добавление информации о тарифе"""
    try:
        for date, categories in info.root.items():
            for category in categories:

                cargo_type = category.cargo_type
                rate = category.rate

                existing_rate = await db.execute(
                    select(Rate).where(Rate.date == date, Rate.cargo_type == cargo_type)
                )
                if existing_rate.scalars().first():
                    raise HTTPException(
                        status_code=400,
                        detail=f"Duplicate: A rate for date '{date}' and cargo type '{cargo_type}' already exists."
                    )
                else:
                    new_rate = Rate(date=date, cargo_type=cargo_type, rate=rate)

                if new_rate:
                    db.add(new_rate)
                    await db.commit()
                    await db.refresh(new_rate)
                    await db.close()
        return info.dict()

    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))
    finally:
        await db.close()


async def get_rate(id: int, db: AsyncSession):
    """Получение страховки по id"""
    try:
        data = await db.execute(select(Rate).where(Rate.id == id))
        result = data.scalars().first()
        if result:
            return result
    except Exception:
        raise HTTPException(status_code=404, detail="Rate not found")


async def edit_data(id: int,
                    edit_info,
                    db: AsyncSession):
    """Изменение информации о тарифе"""
    try:
        data = await get_rate(id=id, db=db)
        if data:
            edit_info_dict = edit_info.dict(exclude_unset=True)
            for field, value in edit_info_dict.items():
                if hasattr(data, field):
                    setattr(data, field, value)

            await db.commit()
            return edit_info_dict

    except Exception as error:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(error))
    finally:
        await db.close()


async def delete_data(id: int, db: AsyncSession):
    """Удаление информации о тарифе"""
    try:
        data = await db.execute(select(Rate).where(Rate.id == id))
        result = data.scalars().first()
        if result:
            await db.delete(result)
            await db.commit()
            return True

    except Exception as error:
        await db.rollback()
        raise HTTPException(status_code=404, detail=str(error))
    finally:
        await db.close()
