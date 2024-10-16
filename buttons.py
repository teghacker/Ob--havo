from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup , KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bs4 import BeautifulSoup 
import requests
from confik import *
sahifa = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Bugungi ob-havo", callback_data="Bugungi ob-havo"), InlineKeyboardButton(text="Haftalik ob-havo", callback_data="Haftalik ob-havo")],
    ]
)

ortga = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Ortga ◀️", callback_data="Ortga"),InlineKeyboardButton(text="Bosh menyuga qaytish", callback_data="Bosh")],
    ]
)

Viloyatlar=InlineKeyboardBuilder()
for i,j in d.items():
#    print(i,j)
   Viloyatlar.button(text=f"📍 {j}",callback_data=f"{j}")
Viloyatlar.adjust(2)


