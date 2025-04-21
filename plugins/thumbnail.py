from pyrogram import Client, filters
from pyrogram.types import Message
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
from helper.database import (
    jishubotz, set_watermark, get_watermark, del_watermark,
    set_watermark_size, get_watermark_size
)
import os
import subprocess


@Client.on_message(filters.private & (filters.photo | filters.video))
async def add_thumbnail(client, message):
    processing_msg = await message.reply_text("⏳ Processing your thumbnail...")

    file_path, thumb_path, final_path = None, None, None
    user_id = message.from_user.id

    try:
        file_path = await message.download(file_name=f"{user_id}_temp")

        if message.video:
            thumb_path = f"{file_path}_thumb.jpg"
            subprocess.run([
                "ffmpeg", "-ss", "00:00:01.000", "-i", file_path,
                "-vframes", "1", "-q:v", "2", "-vf", "scale=-1:720",
                thumb_path
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            thumb_path = file_path

        # ওপেন থাম্বনেইল আর লোগো
        main_image = Image.open(thumb_path).convert("RGBA")
        logo = Image.open("logo.png").convert("RGBA")

        w, h = main_image.size
        logo_size = int(w * 0.1)
        logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

        # লোগো ট্রান্সপারেন্ট করা
        logo_alpha = logo.split()[3]
        logo_alpha = ImageEnhance.Brightness(logo_alpha).enhance(0.6)
        logo.putalpha(logo_alpha)

        # প্রিমিয়াম চেক
        premium_enabled = await jishubotz.get_premium_status()
        is_premium = await jishubotz.is_premium(user_id)

        if not premium_enabled or not is_premium:
            main_image.paste(logo, (w - logo_size - 15, 15), logo)

            # ওয়াটারমার্ক
            watermark_text = await get_watermark(user_id)
            if watermark_text:
                draw = ImageDraw.Draw(main_image)
                font_size = await get_watermark_size(user_id)
                font_size = int(font_size) if font_size else 36
                try:
                    font = ImageFont.truetype("arial.ttf", size=font_size)
                except:
                    font = ImageFont.load_default()

                bbox = draw.textbbox((0, 0), watermark_text, font=font)
                text_w = bbox[2] - bbox[0]
                text_h = bbox[3] - bbox[1]
                draw.text((15, h - text_h - 15), watermark_text, font=font, fill=(255, 255, 255, 180))

        # ফাইনাল সেভ
        final_path = f"thumb_{user_id}.jpg"
        main_image.convert("RGB").save(final_path, "JPEG", quality=95)

        # সেন্ড এবং সেভ
        sent = await client.send_photo(
            chat_id=message.chat.id,
            photo=final_path,
            caption="✅ **Thumbnail with logo added!**\n\nNow send your video to apply it!"
        )

        await jishubotz.set_thumbnail(user_id, file_id=sent.photo.file_id)
        await processing_msg.edit("✅ **Thumbnail saved successfully!**")

    except Exception as e:
        await processing_msg.edit(f"❌ Failed to process thumbnail.\n\n**Error:** `{e}`")

    finally:
        for path in [file_path, thumb_path, final_path]:
            if path and os.path.exists(path):
                os.remove(path)