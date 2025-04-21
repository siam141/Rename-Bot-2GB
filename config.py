# config.py

import os

class Config:
    API_ID = int(os.environ.get("API_ID", 12345))
    API_HASH = os.environ.get("API_HASH", "your_api_hash")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token")
    
    DB_URL = os.environ.get("DB_URL", "mongodb+srv://...")
    DB_NAME = os.environ.get("DB_NAME", "pyrogram_bot")

    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1001234567890"))
    ADMIN = [int(i) for i in os.environ.get("ADMIN", "").split()]
    
    START_PIC = os.environ.get("START_PIC", "https://telegra.ph/file/f6a314da6c047b2a0074f.jpg")
    DONATE_LINK = os.environ.get("DONATE_LINK", "https://t.me/yourchannel")

    BROADCAST_AS_COPY = bool(os.environ.get("BROADCAST_AS_COPY", True))
    FORCE_SUB = os.environ.get("FORCE_SUB", None)

    WATERMARK_FONT = os.environ.get("WATERMARK_FONT", "Arial-Bold.ttf")  # Keep this font file in bot folder or adjust path


class Txt:
    START_TXT = """**স্বাগতম {user_mention}!
    
আমি একটি শক্তিশালী থাম্বনেইল কাস্টমাইজেশন বট।**
        
**প্রিমিয়াম ইউজাররা জলছাপ টেক্সট, সাইজ ও লোগো সেট করতে পারবেন।**

আমার সাহায্যে আপনি:
— কাস্টম থাম্বনেইল যোগ করতে পারবেন  
— জলছাপ টেক্সট ও লোগো যুক্ত করতে পারবেন  
— ক্যাপশন, প্রিফিক্স, সাফিক্স কাস্টমাইজ করতে পারবেন  
— ভিডিওর মেটাডেটা সেট করতে পারবেন

নীচের বোতামগুলো ব্যবহার করে শুরু করুন।
"""

    HELP_TXT = """**সহায়তা বিভাগ**

— /set_watermark → জলছাপ টেক্সট সেট করুন  
— /del_watermark → জলছাপ টেক্সট সরান  
— /set_size → জলছাপ টেক্সটের সাইজ সেট করুন  
— /set_logo → লোগো সেট করুন  
— /del_logo → লোগো সরান  
— /set_caption → কাস্টম ক্যাপশন সেট করুন  
— /set_prefix → নামের আগে টেক্সট  
— /set_suffix → নামের পরে টেক্সট  
— /set_thumbnail → থাম্বনেইল আপলোড করুন  
— /del_thumbnail → থাম্বনেইল মুছুন  
— /settitle → ভিডিওর শিরোনাম সেট করুন  
— /metadata → মেটাডেটা UI পান

**নোট:** জলছাপ, লোগো, মেটাডেটা শুধুমাত্র প্রিমিয়াম ইউজারদের জন্য।  
প্রিমিয়াম নিতে অ্যাডমিনের সাথে যোগাযোগ করুন।
"""

    ABOUT_TXT = """**Bot Details:**

- **Bot Name:** Custom Thumbnail Bot  
- **Language:** Python3  
- **Framework:** Pyrogram  
- **Database:** MongoDB  
- **Developer:** @yourusername  
- **Channel:** [আপনার চ্যানেল]  
- **Source:** [GitHub লিংক দিন]

__Made with love for Bengali users.__
"""

    DONATE_TXT = """**আমাদের সাপোর্ট করুন!**

আপনি চাইলে আমাদের সাপোর্ট করতে পারেন।  
এতে আমরা সার্ভার খরচ চালাতে পারি এবং আরও ফিচার আনতে পারি।

**ডোনেট লিংক:** {donate_link}

ধন্যবাদ আপনাকে!
"""

    PREMIUM_TXT = """**প্রিমিয়াম ফিচারস:**

— জলছাপ টেক্সট ও সাইজ  
— কাস্টম লোগো  
— ভিডিও মেটাডেটা সেট  
— ফাস্টার প্রসেসিং

**মূল্য:**
— ১ মাস: ₹৫০  
— ৩ মাস: ₹১২৫  
— আজীবন: ₹৩৫০

যোগাযোগ করুন: @yourusername
"""