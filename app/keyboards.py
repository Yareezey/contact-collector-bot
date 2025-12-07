from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Оставить заявку")]], resize_keyboard=True)

main2 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Остановить создание заявки", callback_data='stop')]])

admin = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Всего заявок", callback_data='all_contacts')]
                                              ,[InlineKeyboardButton(text="Последние 5 заявок", callback_data='last_five_contacts')],
                                              [InlineKeyboardButton(text="Добавить админа", callback_data='addadmin')]])
