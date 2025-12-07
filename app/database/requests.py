from app.database.models import async_session
from app.database.models import Contact, Admin
from sqlalchemy import select, func

async def set_contact(id, name, email, number):
    async with async_session() as session:
        session.add(Contact(id=id,name=name,email=email,phone_number=number))
        await session.commit()
        
async def is_admin(id):
    async with async_session() as session:
        user = await session.scalar(select(Admin).where(Admin.id == id))
        if not user:
            return False
        else:
            return True

async def count_contacts():
    async with async_session() as session:
        contact_count = await session.execute(select(Contact))
        result = contact_count.scalars().all() 
        return len(result)
    
async def last_five_contacts():
    async with async_session() as session:
        d=[]
        contact_count = await session.execute(select(Contact))
        result = contact_count.scalars().all()
        if len(result)>=5:
            for i in range(len(result)-1,len(result)-6,-1):
                d.append({'id': result[i].id, 'name': result[i].name, 'email': result[i].email, 'phone_number': result[i].phone_number})
        else:
            for i in range(len(result)-1,-1,-1):
                d.append({'id': result[i].id, 'name': result[i].name, 'email': result[i].email, 'phone_number': result[i].phone_number})
        return d
    
async def add_admin(id):
    async with async_session() as session:
        session.add(Admin(id=id))
        await session.commit()
