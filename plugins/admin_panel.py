from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import ADMIN, CHANNEL, SUPPORT, LOG_CHANNEL
from helper.database import db  # আগের jishubotz এর জায়গায় db
from plugins.start_&_cd import Txt
import asyncio

@Client.on_message(filters.private & filters.user(ADMIN) & filters.command("panel"))
async def admin_panel(client, message: Message):
    total_users = await db.total_users_count()
    text = f"**আডমিন কন্ট্রোল প্যানেল**\n\nমোট ইউজারঃ `{total_users}` জন"
    button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("সকল ইউজার", callback_data="all_users"),
                InlineKeyboardButton("ব্রডকাস্ট", callback_data="broadcast")
            ],
            [
                InlineKeyboardButton("প্রিমিয়াম ➕", callback_data="add_premium"),
                InlineKeyboardButton("প্রিমিয়াম ➖", callback_data="remove_premium")
            ],
            [
                InlineKeyboardButton("স্ট্যাটাস", callback_data="status"),
                InlineKeyboardButton("রিস্টার্ট", callback_data="restart")
            ]
        ]
    )
    await message.reply(text, reply_markup=button)

@Client.on_callback_query(filters.user(ADMIN))
async def admin_callbacks(client, query: CallbackQuery):
    data = query.data

    if data == "all_users":
        users = await db.get_all_users()
        text = "**সকল ইউজার লিস্টঃ**\n\n"
        for user in users:
            text += f"`{user['_id']}` | {'Premium' if user.get('is_premium') else 'Free'}\n"
        await query.message.edit(text=text[:4000])

    elif data == "broadcast":
        await query.message.edit("**যা লিখবি তা এখন পাঠা (Cancel করতে /cancel)**")

        try:
            broadcast_msg = await client.listen(query.from_user.id, timeout=300)
            if broadcast_msg.text and broadcast_msg.text.lower() == "/cancel":
                await query.message.reply("ব্রডকাস্ট বাতিল করা হয়েছে।")
                return
        except asyncio.TimeoutError:
            await query.message.reply("টাইম শেষ। আবার চেষ্টা কর।")
            return

        users = await db.get_all_users()
        success = 0
        failed = 0

        for user in users:
            try:
                await client.send_message(user['_id'], broadcast_msg.text)
                success += 1
                await asyncio.sleep(0.1)
            except:
                failed += 1
                await db.delete_user(user['_id'])

        await query.message.reply(f"✅ পাঠানো হয়েছে: {success}\n❌ ফেল করেছে: {failed}")

    elif data == "add_premium":
        await query.message.edit("প্রিমিয়াম ইউজার আইডি পাঠাও:")
        try:
            msg = await client.listen(query.from_user.id, timeout=60)
            user_id = int(msg.text)
            await db.add_premium(user_id)
            await query.message.reply(f"`{user_id}` এখন প্রিমিয়াম ইউজার।")
        except:
            await query.message.reply("ভুল হয়েছে। আবার চেষ্টা কর।")

    elif data == "remove_premium":
        await query.message.edit("যেই আইডি প্রিমিয়াম থেকে বাদ দিবে পাঠাও:")
        try:
            msg = await client.listen(query.from_user.id, timeout=60)
            user_id = int(msg.text)
            await db.remove_premium(user_id)
            await query.message.reply(f"`{user_id}` এখন আর প্রিমিয়াম না।")
        except:
            await query.message.reply("ভুল হয়েছে। আবার চেষ্টা কর।")

    elif data == "status":
        total = await db.total_users_count()
        premium = await db.premium_users_count()
        await query.message.edit(f"**স্ট্যাটাস**\n\nমোট ইউজার: `{total}`\nপ্রিমিয়াম: `{premium}`")

    elif data == "restart":
        await query.message.edit("♻️ বট রিস্টার্ট হচ্ছে...")
        await asyncio.sleep(2)
        import os, sys
        os.execl(sys.executable, sys.executable, *sys.argv)