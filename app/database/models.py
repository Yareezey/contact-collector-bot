from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy import BigInteger

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class Contact(Base):
    __tablename__ = 'contacts'

    id = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column()
    phone_number: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()

class Admin(Base):
    __tablename__ = 'admins'

    id = mapped_column(BigInteger, primary_key=True)

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

