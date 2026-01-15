import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import config
from database import db
from handlers.user import user_router
from handlers.admin import admin_router
from middlewares.subscription import SubscriptionMiddleware

async def main():
    # Logging configuration
    logging.basicConfig(level=logging.INFO)

    # Initialize Bot and Dispatcher
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Initialize Database
    await db.create_tables()

    # Register Middlewares
    # Subscription middleware should be applied to user router or globally but carefully
    # Applying it to user router is safer to avoid blocking admin or start commands if handled inside
    user_router.message.middleware(SubscriptionMiddleware())
    user_router.callback_query.middleware(SubscriptionMiddleware())

    # Register Routers
    dp.include_router(admin_router) # Admin router first to catch admin commands
    dp.include_router(user_router)

    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot to'xtatildi.")
