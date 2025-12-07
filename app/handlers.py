from aiogram.filters import CommandStart, Command
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
import app.keyboards as kb
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import app.database.requests as rq

router = Router()

class AddAdmin(StatesGroup):
    id = State()

class Reg(StatesGroup):
    name = State()
    email = State()
    number = State()

@router.message(CommandStart())
async def StartingCommand(message: Message):
    await message.answer("Добро пожаловать! Я помогу вам оставить заявку на консультацию.", reply_markup=kb.main)

@router.message(Command('help'))
async def Help(message:Message):
    await message.answer(f"Это бот для создания заявки на консультанцию\nНапишите /start а затем нажминте на кнопку Оставить заявку чтобы оставить заявку на консультацию")

@router.message(F.text == 'Оставить заявку')
async def register_first_step(message: Message, state: FSMContext):
    await state.set_state(Reg.name)
    await message.answer('Введите имя', reply_markup=kb.main2)

@router.message(Reg.name)
async def register_second_step(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Reg.email)
    await message.answer('Введите ваш email', reply_markup=kb.main2)    

@router.message(Reg.email)
async def register_third_step(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await state.set_state(Reg.number)
    await message.answer('Введите номер телефона', reply_markup=kb.main2)

@router.message(Reg.number)
async def registration_fourth_step(message: Message, state: FSMContext):
    await state.update_data(number = message.text)
    data = await state.get_data()
    try:
        await rq.set_contact(message.from_user.id,data['name'],data['email'],data['number'])
        await message.answer(f'Спасибо за регистрацию! Вот ваши данные: \nИмя: {data['name']}\nEmail: {data['email']}\nНомер телефона: {data['number']}')
        await state.clear()
    except:
        await message.answer('Вы уже были зарегестрированы!')
    

@router.callback_query(F.data == 'stop')
async def stop_registration(callback: CallbackQuery, state: FSMContext):
    await callback.answer(text='Вы отменили создание заявки')
    await callback.message.edit_text('Вы отменили создание заявки, чтобы начать заново напишите /start')
    await state.clear()

@router.message(Command('admin'))
async def admin(message:Message):
    if await rq.is_admin(message.from_user.id):
        await message.answer('Админ панель:', reply_markup=kb.admin)

@router.callback_query(F.data == 'last_five_contacts')
async def all_contacts(callback: CallbackQuery):
    lastfivelist = await rq.last_five_contacts()
    await callback.answer(text='Последние 5 заявок')
    if len(lastfivelist)>=5:
        for i in range(len(lastfivelist)-1,len(lastfivelist)-6,-1):
            await callback.message.answer(f"{i+1} заявка: id: {lastfivelist[i]['id']}, Имя: {lastfivelist[i]['name']}, Email: {lastfivelist[i]['email']}, Номер телефона: {lastfivelist[i]['phone_number']} ")
    else:
        for i in range(len(lastfivelist)-1,-1,-1):
            await callback.message.answer(f"{i+1} заявка: id: {lastfivelist[i]['id']}, Имя: {lastfivelist[i]['name']}, Email: {lastfivelist[i]['email']}, Номер телефона: {lastfivelist[i]['phone_number']} ")

@router.callback_query(F.data == 'all_contacts')
async def all_contacts(callback: CallbackQuery):
    number_of_contacts = await rq.count_contacts()
    await callback.answer(text='Количество заявок')
    await callback.message.answer(f'Всего заявок: {number_of_contacts}')

@router.callback_query(F.data=='addadmin')
async def addadmin_first_step(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Добавить администратора')
    await state.set_state(AddAdmin.id)
    await callback.message.answer("Введите Telegram ID пользователя, которого хотите сделать админом")

@router.message(AddAdmin.id)
async def add_admin_second_step(message: Message, state: FSMContext):
    await state.update_data(id = message.text)
    admindata = await state.get_data()
    try:
        await rq.add_admin(admindata['id'])
        await message.answer(f'Вы успешно добавили пользователя с ID: {admindata["id"]} в администраторы')
    except:
        await message.answer('Пользователь с таким ID уже администратор')