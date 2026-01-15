from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Dict, Any, Awaitable
from database import db
from keyboards.keyboards import get_subscription_keyboard

class SubscriptionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        # Check if the event is from a user
        user = data.get("event_from_user")
        if not user:
            return await handler(event, data)

        # Allow /start command to proceed so we can add user to DB
        if isinstance(event, Message) and event.text == "/start":
             return await handler(event, data)
        
        # If it's a callback query for checking subscription, let it pass to the specific handler
        if isinstance(event, CallbackQuery) and event.data == "check_subscription":
            return await handler(event, data)

        channels = await db.get_channels()
        if not channels:
            return await handler(event, data)

        not_subscribed = []
        bot = data['bot']
        
        for channel in channels:
            channel_id = channel[0] # tuple index 0: channel_id
            channel_name = channel[2] # tuple index 2: channel_name
            channel_link = channel[1] # tuple index 1: channel_link
            
            try:
                member = await bot.get_chat_member(chat_id=channel_id, user_id=user.id)
                if member.status not in ["creator", "administrator", "member"]:
                    not_subscribed.append({
                        'channel_name': channel_name,
                        'channel_link': channel_link
                    })
            except Exception as e:
                # If bot cannot check (e.g., kicked from channel), assume not subscribed or log error
                print(f"Error checking channel {channel_id}: {e}")
                not_subscribed.append({
                        'channel_name': channel_name,
                        'channel_link': channel_link
                    })

        if not_subscribed:
            keyboard = get_subscription_keyboard(not_subscribed)
            if isinstance(event, Message):
                await event.answer(
                    "Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling:",
                    reply_markup=keyboard
                )
            elif isinstance(event, CallbackQuery):
                await event.message.answer(
                     "Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling:",
                    reply_markup=keyboard
                )
                await event.answer() # Acknowledge callback
            return # Stop execution if not subscribed

        return await handler(event, data)
