from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from database import db
from keyboards.keyboards import get_subscription_keyboard

user_router = Router()

@user_router.message(CommandStart())
async def cmd_start(message: Message):
    await db.add_user(message.from_user.id)
    await message.answer(
        "Assalomu alaykum! Video kodini yuboring."
    )

@user_router.callback_query(F.data == "check_subscription")
async def check_subscription(callback: CallbackQuery, bot):
    user_id = callback.from_user.id
    channels = await db.get_channels()
    
    not_subscribed = []
    
    for channel in channels:
        channel_id = channel[0]
        channel_name = channel[2]
        channel_link = channel[1]
        
        try:
            member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
            if member.status not in ["creator", "administrator", "member"]:
                not_subscribed.append({
                    'channel_name': channel_name,
                    'channel_link': channel_link
                })
        except Exception as e:
            print(f"Error checking channel {channel_id}: {e}")
            not_subscribed.append({
                    'channel_name': channel_name,
                    'channel_link': channel_link
                })
    
    if not_subscribed:
        await callback.answer("Siz hali barcha kanallarga obuna bo'lmadingiz!", show_alert=True)
        # Optional: refresh the keyboard if list changed, but usually not needed here
    else:
        await callback.message.delete()
        await callback.message.answer("Obuna tasdiqlandi! ✅\nVideo kodini yuborishingiz mumkin.")

@user_router.message()
async def get_video_by_code(message: Message):
    code = message.text.strip()
    
    # Check if it is a digit
    # if not code.isdigit():
    #     await message.answer("Iltimos, faqat raqam yoki kod yuboring.")
    #     return
    
    video = await db.get_video(code)
    
    if video:
        file_id = video[0]
        description = video[1]
        
        caption = f"🎬 Darslik videosi\nKod: {code}"
        if description:
            caption += f"\n\n{description}"
            
        await message.answer_video(video=file_id, caption=caption)
    else:
        await message.answer("❌ Bunday kod topilmadi.")
