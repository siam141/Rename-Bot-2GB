import os, sys, time, asyncio, logging, datetime
from config import Config
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
from helper.database import jishubotz

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@Client.on_message(filters.command("status") & filters.user(Config.ADMIN))
async def get_stats(bot, message):
    total_users = await jishubotz.total_users_count()
    uptime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - bot.uptime))
    start_t = time.time()
    st = await message.reply('**Processing The Details.....**')
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await st.edit(text=f"**--Bot Stats--** \n\n**⌚ Bot Uptime:** `{uptime}` \n**🐌 Current Ping:** `{time_taken_s:.3f} ms` \n**👭 Total Users:** `{total_users}`")

@Client.on_message(filters.command("restart") & filters.user(Config.ADMIN))
async def restart_bot(bot, message):
    msg = await bot.send_message(text="🔄 Processes Stopped. Bot Is Restarting...", chat_id=message.chat.id)
    await asyncio.sleep(3)
    await msg.edit("✅️ Bot Is Restarted. Now You Can Use Me")
    os.execl(sys.executable, sys.executable, *sys.argv)

@Client.on_message(filters.private & filters.command("ping"))
async def ping(_, message):
    start_t = time.time()
    rm = await message.reply_text("Pinging....")
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await rm.edit(f"Ping 🔥!\n{time_taken_s:.3f} ms")
    return time_taken_s

@Client.on_message(filters.command("broadcast") & filters.user(Config.ADMIN) & filters.reply)
async def broadcast_handler(bot: Client, m: Message):
    try:
        await bot.send_message(Config.LOG_CHANNEL, f"{m.from_user.mention} or {m.from_user.id} started a broadcast.")
    except Exception as e:
        print("Log channel error:", e)

    all_users = await jishubotz.get_all_users()
    broadcast_msg = m.reply_to_message
    sts_msg = await m.reply_text("Broadcast Started..!")

    done = 0
    failed = 0
    success = 0
    start_time = time.time()
    total_users = await jishubotz.total_users_count()

    async for user in all_users:
        sts = await send_msg(user['_id'], broadcast_msg)
        if sts == 200:
            success += 1
        else:
            failed += 1
        if sts == 400:
            await jishubotz.delete_user(user['_id'])
        done += 1
        if done % 20 == 0:
            try:
                await sts_msg.edit(f"**Broadcast In Progress:** \n\nTotal Users: {total_users} \nCompleted: {done}/{total_users}\nSuccess: {success}\nFailed: {failed}")
            except Exception as e:
                logger.warning(f"Edit failed: {e}")

    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await sts_msg.edit(f"**Broadcast Completed:** \n\nCompleted In `{completed_in}`.\n\nTotal Users: {total_users}\nCompleted: {done}/{total_users}\nSuccess: {success}\nFailed: {failed}")

async def send_msg(user_id, message):
    try:
        await message.copy(chat_id=int(user_id))
        return 200
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await send_msg(user_id, message)
    except InputUserDeactivated:
        logger.info(f"{user_id} : Deactivated")
        return 400
    except UserIsBlocked:
        logger.info(f"{user_id} : Blocked The Bot")
        return 400
    except PeerIdInvalid:
        logger.info(f"{user_id} : User ID Invalid")
        return 400
    except Exception as e:
        logger.error(f"{user_id} : {e}")
        return 500



#gpt



from pyrogram import Client, filters
from pyrogram.types import Message
from helper.database import jishubotz

ADMINS = [7862181538]  # তোমার Telegram ID

@Client.on_message(filters.command("addpremium") & filters.user(ADMINS))
async def cmd_add_premium(_, m: Message):
    if len(m.command) < 2:
        return await m.reply("Usage: /addpremium user_id")
    user_id = int(m.command[1])
    await jishubotz.add_premium(user_id)
    await m.reply(f"✅ User {user_id} added as Premium.")

@Client.on_message(filters.command("delpremium") & filters.user(ADMINS))
async def cmd_del_premium(_, m: Message):
    if len(m.command) < 2:
        return await m.reply("Usage: /delpremium user_id")
    user_id = int(m.command[1])
    await jishubotz.remove_premium(user_id)
    await m.reply(f"❌ User {user_id} removed from Premium.")

@Client.on_message(filters.command("ispremium"))
async def check_premium(_, m: Message):
    is_prem = await jishubotz.is_premium(m.from_user.id)
    if is_prem:
        await m.reply("✅ You are a Premium user.")
    else:
        await m.reply("❌ You are not a Premium user.")





# Ban command remains unchanged
# Unban command remains unchanged
# You can include them again if needed

@Client.on_message(filters.command("premium") & filters.user(Config.ADMIN))
async def premium_menu(bot, message):
    btn = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add Premium", callback_data="add_premium")],
        [InlineKeyboardButton("➖ Remove Premium", callback_data="remove_premium")],
        [InlineKeyboardButton("📋 List Premium", callback_data="list_premium")]
    ])
    await message.reply("**প্রিমিয়াম ইউজার ম্যানেজমেন্ট মেনু**", reply_markup=btn)

@Client.on_callback_query(filters.regex("add_premium") & filters.user(Config.ADMIN))
async def ask_add_premium(bot, query):
    await query.message.edit("প্রিমিয়াম অ্যাড করতে ইউজারের আইডি দিন (উদাঃ `123456789`)")

@Client.on_callback_query(filters.regex("remove_premium") & filters.user(Config.ADMIN))
async def ask_remove_premium(bot, query):
    await query.message.edit("প্রিমিয়াম রিমুভ করতে ইউজারের আইডি দিন (উদাঃ `123456789`)")

@Client.on_callback_query(filters.regex("list_premium") & filters.user(Config.ADMIN))
async def list_premium_users(bot, query):
    users = await jishubotz.get_all_premium()
    if not users:
        await query.message.edit("কোনো প্রিমিয়াম ইউজার নেই।")
    else:
        text = "**প্রিমিয়াম ইউজার লিস্ট:**

" + "
".join([f"`{uid}`" for uid in users])
        await query.message.edit(text)


@Client.on_callback_query(filters.regex("toggle_premium") & filters.user(Config.ADMIN))
async def toggle_premium_status(bot, query):
    current_status = await jishubotz.get_premium_status()
    new_status = not current_status
    await jishubotz.set_premium_status(new_status)
    status_text = "চালু" if new_status else "বন্ধ"
    await query.answer()
    await query.message.edit(f"✅ গ্লোবাল প্রিমিয়াম স্টেটাস এখন **{status_text}** করা হয়েছে।")

@Client.on_message(filters.command("premium") & filters.user(Config.ADMIN))
async def premium_menu(bot, message):
    status = await jishubotz.get_premium_status()
    status_text = "ON ✅" if status else "OFF ❌"
    btn = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"Premium Toggle: {status_text}", callback_data="toggle_premium")],
        [InlineKeyboardButton("➕ Add Premium", callback_data="add_premium")],
        [InlineKeyboardButton("➖ Remove Premium", callback_data="remove_premium")],
        [InlineKeyboardButton("📋 List Premium", callback_data="list_premium")]
    ])
    await message.reply("**প্রিমিয়াম ইউজার ম্যানেজমেন্ট মেনু**", reply_markup=btn)
