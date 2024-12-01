from sqlalchemy import MetaData, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship

metadata = MetaData()

Base = declarative_base(metadata=metadata)


class Rate(Base):
    __tablename__ = "rate"
    __target_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date: Mapped[str] = mapped_column(String(10), nullable=False)
    cargo_type: Mapped[str] = mapped_column(String, nullable=False)
    rate: Mapped[str] = mapped_column(String, nullable=False)
    price_id: Mapped[int] = mapped_column(Integer, ForeignKey("price.id"), nullable=True)
    price = relationship('Price')


class Price(Base):
    __tablename__ = "price"
    __target_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    price: Mapped[int] = mapped_column(Float, nullable=False)
