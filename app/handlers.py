import os  # Импортируем модуль os для работы с файлами
from aiogram import F, Router, Bot
from aiogram.types import Message, ContentType, InputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from config import TG_TOKEN

from app.generate import ai_generate

router = Router()
bot = Bot(token=TG_TOKEN)

class Gen(StatesGroup):
    wait = State()
   

@router.message(CommandStart())
async def cmd_start(message: Message):    
    await message.answer("Добро пожаловать, напишите ваш запрос.")

@router.message(Gen.wait)
async def stop_flood(message: Message):    
    await message.answer("Подождите, идет генерация...")

async def send_code_file(chat_id: int, code: str):
    # Создаем временный файл
    file_path = "generated_code.txt"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(code)
    
    # Отправляем файл пользователю
    input_file = InputFile(file_path)  # Создаем экземпляр InputFile
    await bot.send_document(chat_id, input_file, caption="Вот ваш код.")
    
    # Удаляем файл после отправки
    os.remove(file_path)

@router.message()
async def genetating_answer(message: Message, state: FSMContext):
    await state.set_state(Gen.wait)
    response = await ai_generate(message.text)
    
    # Если ответ слишком длинный, отправляем его как файл
    if len(response) > 4096:
        await send_code_file(message.chat.id, response)  # Отправляем файл
    else:
        await message.answer(response)  # Отправляем текстовое сообщение
    
    await state.clear()
