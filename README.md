# Telegram Video Bot

Bu Telegram bot foydalanuvchilarga kod orqali videolarni yuboradi va majburiy kanalga obuna bo'lishni talab qiladi.

## O'rnatish

1.  **Talablar**:
    *   Python 3.10+
    *   `pip` paket menejeri

2.  **Kutubxonalarni o'rnatish**:
    Terminalda quyidagi buyruqni bering:
    ```bash
    pip install aiogram aiosqlite python-dotenv
    ```

3.  **Sozlash**:
    *   `.env` faylini oching.
    *   `BOT_TOKEN` ga @BotFather dan olingan tokenni yozing.
    *   `ADMIN_ID` ga o'z Telegram ID raqamingizni yozing (buni @userinfobot orqali olishingiz mumkin).

    Misol `.env` fayli:
    ```
    BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
    ADMIN_ID=123456789
    ```

## Ishga tushirish

Botni ishga tushirish uchun quyidagi buyruqni bering:
```bash
python main.py
```

## Admin Panel

Admin panelga kirish uchun `/admin` buyrug'ini yuboring yoki oddiygina `/start` bosing (agar ID to'g'ri sozlangan bo'lsa, admin menyusi ochilmasligi mumkin, lekin `/admin` ishlashi kerak).

**Imkoniyatlar:**
*   **Video qo'shish**: "➕ Video qo‘shish" tugmasini bosing, kodni kiriting va videoni yuboring.
*   **Video o'chirish**: Kod orqali videoni o'chirish.
*   **Kanal qo'shish**: Kanal ID (-100 bilan boshlanadi) va havolasini kiritish. Bot bu kanalga admin bo'lishi kerak!
*   **Statistika**: Foydalanuvchilar soni.

## Eslatma

Majburiy obuna ishlashi uchun bot, majburiy qilib belgilangan kanalda **Admin** bo'lishi va foydalanuvchilarni tekshirish huquqiga ega bo'lishi kerak.
