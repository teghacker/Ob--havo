import asyncio
import logging
from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import callback_query, Message, FSInputFile
from confik import *
from buttons import *
from states import *
import requests
from bs4 import BeautifulSoup 
router = Router()
bot = Bot(token=token)
logging.basicConfig(level=logging.INFO)
dp = Dispatcher()
dp.include_router(router)

@router.message(Command('start'))
async def star(message: Message):
    welcome_message = await message.answer_photo(photo='https://cdn2.iconfinder.com/data/icons/weather-flat-14/64/weather02-512.png', caption=f"""Assalom alaykum {message.from_user.full_name}
🌤 Ob - havo botimizga xush kelibsiz !""")
    await message.delete()
    viloyatlar_message = await message.answer(f"""Qaysi viloyatni Ob - havosi ☀️ kerak?""", reply_markup=Viloyatlar.as_markup())
    await message.delete()
    

@router.callback_query(F.data.in_(d.values()))
async def star(call: callback_query,state:FSMContext):
    # await welcome_message.delete()
    # await viloyatlar_message.delete()
    text = call.data
    await state.update_data({'text':text})
    print(text)
    await call.message.answer(f"""Kunlik ob-havo kerakmi yoki Haftalik""", reply_markup=sahifa)
    await call.message.delete()
    await state.set_state(vil.var)


@router.callback_query(F.data, vil.var)
async def star(call: callback_query,state:FSMContext):
    cnt=1
    data = await state.get_data()
    for i,j in d.items():
        if j == f'{data.get('text')}':
            break
        cnt+=1
    text = call.data
    url = f"https://sinoptik.ua/погода-{dic[f'{cnt}']}"
    response = requests.get(url)
    malumotlar = BeautifulSoup(response.text, 'html.parser')
    c=0
    if text=='Bugungi ob-havo':
        for temp in malumotlar.select("#content"):
            maxx = (temp.select(".temperature .max"))[c].text
            minn = temp.select('.temperature .min')[c].text
            month = temp.select('.month')[c].text
            day = temp.select('.day-link')[c].text
            kun = temp.select('.date')[c].text
        try:await call.message.answer(text=f"📅Sana : {month} - {day} - {kun}\nIqlim : {maxx} -- {minn}", reply_markup=ortga)
        except:
            await call.message.answer(f"Nozozlik bo'ldi, uzur soraymiz keyinroq urinib koring")
            await call.message.answer(f"""Qaysi viloyatni Ob - havosi sizga qizik ?""", reply_markup=Viloyatlar.as_markup())
            await state.clear()
    else: 
        text1=""
        for i in range(7):
            for temp in malumotlar.select("#content"):
                maxx = (temp.select(".temperature .max"))[c].text
                minn = temp.select('.temperature .min')[c].text
                month = temp.select('.month')[c].text
                day = temp.select('.day-link')[c].text
                kun = temp.select('.date')[c].text
            c+=1
            try:
                text1+=f"📅Sana : {month}-{day}-{kun}\nIqlim : {maxx} -- {minn}\n\n"
            except:
                await call.message.answer(f"🪛 Nozozlik bo'ldi, uzur soraymiz keyinroq urinib koring")
                await call.message.answer(f"""Qaysi viloyatni Ob - havosi kerak ?""", reply_markup=Viloyatlar.as_markup())
                await state.clear()
                await call.message.delete()
                break
        await call.message.answer(text1, reply_markup=ortga)
    await call.message.delete()
    await state.set_state(vil.finish)


@router.callback_query(F.data, vil.finish)
async def star(call: callback_query,state:FSMContext):
    text = call.data
    if text=='Ortga':
        await call.message.answer(f"""Siz boyagi tanlagandasiz
Kunlik ob-havo kerakmi yoki Haftalik""", reply_markup=sahifa)
        await state.set_state(vil.var)
        await call.message.delete()
    else:
        await call.message.answer(f"""Qaysi viloyatni Ob - havosi kerak ?""", reply_markup=Viloyatlar.as_markup())
        await call.message.delete()
        await state.clear()


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())