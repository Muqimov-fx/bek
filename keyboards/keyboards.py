from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

def get_subscription_keyboard(channels: list):
    builder = InlineKeyboardBuilder()
    for channel in channels:
        builder.row(InlineKeyboardButton(text=channel['channel_name'], url=channel['channel_link']))
    
    # Add "Check Subscription" button
    builder.row(InlineKeyboardButton(text="Obuna bo‘ldim ✅", callback_data="check_subscription"))
    return builder.as_markup()

def get_admin_main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="➕ Video qo‘shish"),
        KeyboardButton(text="🗑 Video o‘chirish")
    )
    builder.row(
        KeyboardButton(text="📢 Kanal qo‘shish"),
        KeyboardButton(text="❌ Kanal o‘chirish")
    )
    builder.row(
        KeyboardButton(text="📊 Statistika"),
        KeyboardButton(text="📋 Kodlar")
    )
    return builder.as_markup(resize_keyboard=True)

def get_cancel_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Bekor qilish")
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
