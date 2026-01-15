from aiogram import Router, F
from aiogram.types import Message, ContentType
from aiogram.filters import Command, BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import config
from database import db
from keyboards.keyboards import get_admin_main_keyboard

admin_router = Router()

# Filter for admin
class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in config.ADMIN_IDS

# Admin States
class AdminStates(StatesGroup):
    waiting_for_video_code = State()
    waiting_for_video_file = State()
    waiting_for_delete_video_code = State()
    
    waiting_for_channel_id = State()
    waiting_for_channel_link = State()
    waiting_for_channel_name = State()
    waiting_for_delete_channel_id = State()

@admin_router.message(Command("admin"), IsAdmin())
async def cmd_admin(message: Message):
    await message.answer("Admin panelga xo'sh kelibsiz!", reply_markup=get_admin_main_keyboard())

# --- Add Video ---
@admin_router.message(F.text == "➕ Video qo‘shish", IsAdmin())
async def start_add_video(message: Message, state: FSMContext):
    await message.answer("Video kodini kiriting:")
    await state.set_state(AdminStates.waiting_for_video_code)

@admin_router.message(AdminStates.waiting_for_video_code, IsAdmin())
async def process_video_code(message: Message, state: FSMContext):
    await state.update_data(code=message.text)
    await message.answer("Endi videoni yuboring:")
    await state.set_state(AdminStates.waiting_for_video_file)

@admin_router.message(AdminStates.waiting_for_video_file, IsAdmin(), F.video)
async def process_video_file(message: Message, state: FSMContext):
    data = await state.get_data()
    code = data['code']
    file_id = message.video.file_id
    description = message.caption  # Can be None
    
    await db.add_video(code, file_id, description)
    await message.answer(f"Video saqlandi! Kod: {code}")
    await state.clear()

# --- Delete Video ---
@admin_router.message(F.text == "🗑 Video o‘chirish", IsAdmin())
async def start_delete_video(message: Message, state: FSMContext):
    await message.answer("O'chiriladigan video kodini kiriting:")
    await state.set_state(AdminStates.waiting_for_delete_video_code)

@admin_router.message(AdminStates.waiting_for_delete_video_code, IsAdmin())
async def process_delete_video(message: Message, state: FSMContext):
    code = message.text
    await db.delete_video(code)
    await message.answer(f"Video o'chirildi (agar mavjud bo'lsa): {code}")
    await state.clear()

# --- Add Channel ---
@admin_router.message(F.text == "📢 Kanal qo‘shish", IsAdmin())
async def start_add_channel(message: Message, state: FSMContext):
    await message.answer("Kanal ID sini kiriting (masalan -100123456789):")
    await state.set_state(AdminStates.waiting_for_channel_id)

@admin_router.message(AdminStates.waiting_for_channel_id, IsAdmin())
async def process_channel_id(message: Message, state: FSMContext):
    await state.update_data(channel_id=message.text)
    await message.answer("Kanal havolasini kiriting (https://t.me/...):")
    await state.set_state(AdminStates.waiting_for_channel_link)

@admin_router.message(AdminStates.waiting_for_channel_link, IsAdmin())
async def process_channel_link(message: Message, state: FSMContext):
    await state.update_data(channel_link=message.text)
    await message.answer("Kanal nomini kiriting:")
    await state.set_state(AdminStates.waiting_for_channel_name)

@admin_router.message(AdminStates.waiting_for_channel_name, IsAdmin())
async def process_channel_name(message: Message, state: FSMContext):
    data = await state.get_data()
    channel_id = data['channel_id']
    channel_link = data['channel_link']
    channel_name = message.text
    
    await db.add_channel(channel_id, channel_link, channel_name)
    await message.answer(f"Kanal qo'shildi: {channel_name}")
    await state.clear()

# --- Delete Channel ---
@admin_router.message(F.text == "❌ Kanal o‘chirish", IsAdmin())
async def start_delete_channel(message: Message, state: FSMContext):
    channels = await db.get_channels()
    text = "Mavjud kanallar:\n"
    for ch in channels:
        text += f"ID: {ch[0]}, Name: {ch[2]}\n"
    await message.answer(text + "\nO'chiriladigan kanal ID sini kiriting:")
    await state.set_state(AdminStates.waiting_for_delete_channel_id)

@admin_router.message(AdminStates.waiting_for_delete_channel_id, IsAdmin())
async def process_delete_channel(message: Message, state: FSMContext):
    channel_id = message.text
    await db.delete_channel(channel_id)
    await message.answer("Kanal o'chirildi.")
    await state.clear()

# --- Stats ---
@admin_router.message(F.text == "📊 Statistika", IsAdmin())
async def get_stats(message: Message):
    count = await db.get_users_count()
    await message.answer(f"Foydalanuvchilar soni: {count}")

# --- List Codes ---
@admin_router.message(F.text == "📋 Kodlar", IsAdmin())
async def get_codes(message: Message):
    videos = await db.get_all_videos()
    if not videos:
        await message.answer("Hozircha videolar yo'q.")
        return
    
    text = "Mavjud kodlar:\n"
    for v in videos:
        text += f"Kod: {v[0]} - {v[1] or 'Izohsiz'}\n"
    
    # Split if too long (simple check)
    if len(text) > 4000:
        await message.answer(text[:4000])
        await message.answer(text[4000:])
    else:
        await message.answer(text)
