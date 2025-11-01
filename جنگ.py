# -*- coding: utf-8 -*-
import os
import json
import time
import random
from datetime import datetime, timedelta
from rubka import Robot
from rubka.context import Message
from rubka.keypad import ChatKeypadBuilder

TOKEN = "DDJIA0DIMPUMPDWDZGHPEPGXNUAFEMHYGJZAHPHVJUOUPXOUIQAJRPVDKXLVPBNX"
DATA_FILE = "ww_data.json"
ADMIN_PASSWORD = "RTF"

# ایجاد نمونه ربات با مدیریت خطا
try:
    bot = Robot(TOKEN)
    print("✅ ربات با موفقیت ایجاد شد")
except Exception as e:
    print(f"❌ خطا در ایجاد ربات: {e}")
    exit(1)

# دیکشنری پرچم کشورها (تعداد بسیار بیشتر)
COUNTRY_FLAGS = {
    "آمریکا": "🇺🇸", "روسیه": "🇷🇺", "چین": "🇨🇳", "ایران": "🇮🇷", "آلمان": "🇩🇪",
    "فرانسه": "🇫🇷", "انگلیس": "🇬🇧", "ژاپن": "🇯🇵", "هند": "🇮🇳", "ترکیه": "🇹🇷",
    "عربستان": "🇸🇦", "مصر": "🇪🇬", "برزیل": "🇧🇷", "آرژانتین": "🇦🇷", "مکزیک": "🇲🇽",
    "کره جنوبی": "🇰🇷", "استرالیا": "🇦🇺", "کانادا": "🇨🇦", "ایتالیا": "🇮🇹", "اسپانیا": "🇪🇸",
    "پاکستان": "🇵🇰", "افغانستان": "🇦🇫", "عراق": "🇮🇶", "سوریه": "🇸🇾", "امارات": "🇦🇪",
    "قطر": "🇶🇦", "کویت": "🇰🇼", "اندونزی": "🇮🇩", "مالزی": "🇲🇾", "ویتنام": "🇻🇳",
    "تایلند": "🇹🇭", "فیلیپین": "🇵🇭", "سنگاپور": "🇸🇬", "نیوزلند": "🇳🇿", "هلند": "🇳🇱",
    "بلژیک": "🇧🇪", "سوئد": "🇸🇪", "نروژ": "🇳🇴", "فنلاند": "🇫🇮", "دانمارک": "🇩🇰",
    "سوئیس": "🇨🇭", "اتریش": "🇦🇹", "لهستان": "🇵🇱", "اوکراین": "🇺🇦", "رومانی": "🇷🇴",
    "بلغارستان": "🇧🇬", "یونان": "🇬🇷", "پرتغال": "🇵🇹", "مجارستان": "🇭🇺", "چک": "🇨🇿",
    "اسلواکی": "🇸🇰", "کرواسی": "🇭🇷", "صربستان": "🇷🇸", "بوسنی": "🇧🇦", "آلبانی": "🇦🇱",
    "مقدونیه": "🇲🇰", "قزاقستان": "🇰🇿", "ازبکستان": "🇺🇿", "ترکمنستان": "🇹🇲", "قرقیزستان": "🇰🇬",
    "تاجیکستان": "🇹🇯", "ارمنستان": "🇦🇲", "گرجستان": "🇬🇪", "آذربایجان": "🇦🇿", "بلاروس": "🇧🇾",
    "مولداوی": "🇲🇩", "لیتوانی": "🇱🇹", "لتونی": "🇱🇻", "استونی": "🇪🇪", "اسلوونی": "🇸🇮",
    "لوکزامبورگ": "🇱🇺", "موناکو": "🇲🇨", "آندورا": "🇦🇩", "لیختن اشتاین": "🇱🇮", "سان مارینو": "🇸🇲",
    "واتیکان": "🇻🇦", "مالت": "🇲🇹", "قبرس": "🇨🇾", "ایسلند": "🇮🇸", "ایرلند": "🇮🇪",
    "پرتوریکو": "🇵🇷", "کوبا": "🇨🇺", "جمهوری دومینیکن": "🇩🇴", "هائیتی": "🇭🇹", "جامائیکا": "🇯🇲",
    "باهاما": "🇧🇸", "پاناما": "🇵🇦", "کاستاریکا": "🇨🇷", "نیکاراگوئه": "🇳🇮", "هندوراس": "🇭🇳",
    "السالوادور": "🇸🇻", "گواتمالا": "🇬🇹", "بلیز": "🇧🇿", "کلمبیا": "🇨🇴", "ونزوئلا": "🇻🇪",
    "پرو": "🇵🇪", "اکوادور": "🇪🇨", "بولیوی": "🇧🇴", "پاراگوئه": "🇵🇾", "اروگوئه": "🇺🇾",
    "شیلی": "🇨🇱", "گینه": "🇬🇳", "سنگال": "🇸🇳", "غنا": "🇬🇭", "نیجریه": "🇳🇬",
    "کنیا": "🇰🇪", "اتیوپی": "🇪🇹", "تانزانیا": "🇹🇿", "آفریقای جنوبی": "🇿🇦", "مراکش": "🇲🇦",
    "الجزایر": "🇩🇿", "تونس": "🇹🇳", "لیبی": "🇱🇾", "سودان": "🇸🇩", "سومالی": "🇸🇴",
    "اوگاندا": "🇺🇬", "رواندا": "🇷🇼", "بروندی": "🇧🇮", "زامبیا": "🇿🇲", "زیمبابوه": "🇿🇼",
    "موزامبیک": "🇲🇿", "ماداگاسکار": "🇲🇬", "موریتانی": "🇲🇷", "مالی": "🇲🇱", "نیجر": "🇳🇪",
    "چاد": "🇹🇩", "ساحل عاج": "🇨🇮", "بورکینافاسو": "🇧🇫", "بنین": "🇧🇯", "توگو": "🇹🇬",
    "سریلانکا": "🇱🇰", "بنگلادش": "🇧🇩", "نپال": "🇳🇵", "بوتان": "🇧🇹", "مالدیو": "🇲🇻",
    "یمن": "🇾🇪", "عمان": "🇴🇲", "اردن": "🇯🇴", "لبنان": "🇱🇧", "فلسطین": "🇵🇸",
    "کامبوج": "🇰🇭", "لائوس": "🇱🇦", "میانمار": "🇲🇲", "برونئی": "🇧🇳", "تیمور شرقی": "🇹🇱",
    "پاپوا گینه نو": "🇵🇬", "فیجی": "🇫🇯", "ساموآ": "🇼🇸", "تونگا": "🇹🇴", "جزایر سلیمان": "🇸🇧",
    "وانواتو": "🇻🇺", "کیریباتی": "🇰🇮", "نائورو": "🇳🇷", "جزایر مارشال": "🇲🇭", "پالائو": "🇵🇼",
    "ایالات فدرال میکرونزی": "🇫🇲", "جزایر کوک": "🇨🇰", "نیووی": "🇳🇺", "توکلائو": "🇹🇰"
}

COUNTRIES = list(COUNTRY_FLAGS.keys())

# ری‌اکشن‌های مختلف برای پیام‌ها
REACTIONS = {
    "success": ["🎉", "✅", "✨", "🌟", "🔥", "💫", "🎊", "🥳", "👏", "👍"],
    "failure": ["❌", "💔", "😢", "👎", "💥", "⚡", "🌧️", "🌀"],
    "attack": ["⚔️", "🎯", "💣", "🔥", "⚡", "🌪️", "💀", "🛡️"],
    "defense": ["🛡️", "🏰", "🪖", "🚧", "🔒", "🛑", "🚨"],
    "resources": ["💰", "💎", "🍖", "🌲", "📦", "🎁", "💼"],
    "building": ["🏗️", "🏭", "🏠", "🏢", "🏛️", "🗼", "🏟️"],
    "treasure": ["🏴‍☠️", "💎", "📜", "🗺️", "⚱️", "🎯", "🔍"],
    "work": ["👷", "💼", "🛠️", "⚒️", "🔧", "🪛", "📊"],
    "alliance": ["🤝", "👥", "🤜🤛", "🫂", "🏴", "🚩"],
    "shop": ["🛒", "🏪", "💰", "💳", "🛍️", "📦"]
}

# پیام‌های تصادفی برای رویدادهای مختلف
RANDOM_MESSAGES = {
    "welcome": [
        "به امپراتوری خود خوش آمدید! 👑",
        "فرمانده جدید وارد میدان شد! 🎖️",
        "قدرت جدیدی در جهان متولد شد! 🌍",
        "حکمرانی تو آغاز شد! ⚔️",
        "به خانواده جنگ جهانی خوش آمدی! 🎯"
    ],
    "attack_success": [
        "حمله کوبنده! دشمن نابود شد! 💥",
        "پیروزی درخشان! منابع به غنیمت گرفته شد! 🎯",
        "لشکرکشی موفق! دشمن فرار را برقرار کرد! 🏃‍♂️",
        "حمله برق آسا! دشمن غافلگیر شد! ⚡",
        "فتح جدید! قلمرو تو گسترش یافت! 🗺️"
    ],
    "attack_failure": [
        "نیروهای دشمن مقاومت کردند! 💔",
        "حمله عقب نشینی کرد! 🚩",
        "دشمن آماده بود! تاکتیک تغییر کن! 🎯",
        "شکست موقت! اما جنگ ادامه دارد! ⚔️",
        "دفاع دشمن قوی بود! نیروهایت را تقویت کن! 🛡️"
    ],
    "treasure_success": [
        "گنجینه افسانه‌ای کشف شد! 🗝️",
        "ثروت باستانی به دست آمد! 💎",
        "ماجراجویی پرسود! گنج پیدا شد! 🏴‍☠️",
        "نقشه گنج درست بود! ثروت بی‌پایان! 📜",
        "شکارچی گنج تو هستی! جایزه بزرگ! 🎯"
    ],
    "work_success": [
        "کار سخت نتیجه داد! حقوق دریافت شد! 💰",
        "پروژه تکمیل شد! پاداش ارزشمند! 🏆",
        "زحماتت جبران شد! درآمد خوبی داشتی! 💎",
        "کارمند نمونه! پاداش ویژه دریافت کردی! 👑",
        "تلاش تو ثمر داد! منابعت افزایش یافت! 📈"
    ],
    "transfer_success": [
        "کمک بشردوستانه ارسال شد! 🤝",
        "همپیمانی جدید! منابع به متحد فرستاده شد! 🎁",
        "دیپلماسی موفق! رابطه تقویت شد! ✨",
        "کمک مالی به متحد! اتحاد محکم‌تر شد! 💪",
        "هدیه دیپلماتیک! روابط بین‌المللی بهبود یافت! 🌍"
    ]
}

# سوالات و جواب‌های تصادفی
QUESTIONS_ANSWERS = [
    {
        "question": "قوی‌ترین سلاح در جنگ جهانی چیست؟",
        "answers": [
            "💪 قدرت اراده فرمانده!",
            "🚀 موشک‌های پیشرفته!",
            "🛡️ سیستم دفاعی قوی!",
            "🤝 اتحاد با قدرت‌های دیگر!",
            "💰 منابع مالی بی‌پایان!"
        ]
    },
    {
        "question": "چگونه امپراتوری خود را تقویت کنم؟",
        "answers": [
            "🏗️ ساختمان‌ها را ارتقا بده!",
            "🎖️ نیروهای نظامی بیشتری آموزش بده!",
            "💎 با الماس تجهیزات بخر!",
            "🤝 با کشورهای دیگر متحد شو!",
            "🏴‍☠️ به شکار گنج برو!"
        ]
    },
    {
        "question": "بهترین استراتژی دفاعی چیست؟",
        "answers": [
            "🛡️ همیشه سپر داشته باش!",
            "📡 رادارهای نظارتی نصب کن!",
            "🎯 نیروهای دفاعی قدرتمند بساز!",
            "🏰 ساختمان‌ها را تقویت کن!",
            "🤝 از متحدان کمک بگیر!"
        ]
    },
    {
        "question": "چگونه سریع پیشرفت کنم؟",
        "answers": [
            "👷 مرتب کار کن و حقوق بگیر!",
            "⚔️ حمله کن و منابع غارت کن!",
            "🏴‍☠️ گنج‌های ارزشمند پیدا کن!",
            "🏗️ ساختمان‌های تولیدی بساز!",
            "💰 با دیگران تجارت کن!"
        ]
    },
    {
        "question": "اتحادیه چه مزایایی دارد؟",
        "answers": [
            "🤝 حمایت در جنگ‌ها!",
            "🎁 اشتراک منابع!",
            "🛡️ دفاع گروهی!",
            "💪 قدرت چانه‌زنی بیشتر!",
            "🌍 نفوذ بین‌المللی!"
        ]
    }
]

# مطمئن شو داده‌ها درست لود شدن
DATA = {"users": {}, "alliances": {}, "buildings": {}}
user_states = {}
user_questions = {}  # برای ذخیره سوالات فعال کاربران

def save_data():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(DATA, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"خطا در ذخیره داده: {e}")

def load_data():
    global DATA
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                loaded_data = json.load(f)
                DATA = {
                    "users": loaded_data.get("users", {}),
                    "alliances": loaded_data.get("alliances", {}),
                    "buildings": loaded_data.get("buildings", {})
                }
    except Exception as e:
        print(f"خطا در بارگذاری داده: {e}")
        DATA = {"users": {}, "alliances": {}, "buildings": {}}

load_data()

def get_random_reaction(category):
    """دریافت ری‌اکشن تصادفی برای دسته‌بندی مشخص"""
    return random.choice(REACTIONS.get(category, ["✨"]))

def get_random_message(event_type):
    """دریافت پیام تصادفی برای رویداد مشخص"""
    return random.choice(RANDOM_MESSAGES.get(event_type, ["✅ عملیات موفق!"]))

def ask_random_question(uid):
    """پرسش سوال تصادفی از کاربر"""
    if uid not in user_questions:
        user_questions[uid] = {}
    
    question_data = random.choice(QUESTIONS_ANSWERS)
    user_questions[uid] = {
        "question": question_data["question"],
        "answers": question_data["answers"],
        "asked_at": time.time()
    }
    
    return question_data["question"]

def check_answer(uid, user_answer):
    """بررسی پاسخ کاربر به سوال"""
    if uid not in user_questions:
        return None
    
    question_data = user_questions[uid]
    
    # اگر کاربر جواب درست داده (هر پاسخی در این سیستم درست است)
    if user_answer.strip():
        correct_answer = random.choice(question_data["answers"])
        
        # پاک کردن سوال
        del user_questions[uid]
        
        # جایزه کوچک برای پاسخ دادن
        reward = {
            "meat": random.randint(10, 30),
            "wood": random.randint(5, 20),
            "diamonds": random.randint(1, 5)
        }
        
        return {
            "correct": True,
            "reward": reward,
            "message": f"🎯 پاسخ هوشمندانه!\n{correct_answer}\n\n🎁 جایزه: {reward['meat']} گوشت, {reward['wood']} چوب, {reward['diamonds']} الماس"
        }
    
    return None

def init_user_data(uid):
    """مقداردهی اولیه داده‌های کاربر"""
    if uid not in DATA["users"]:
        used_countries = [u.get("country", "") for u in DATA["users"].values()]
        available_countries = [c for c in COUNTRIES if c not in used_countries]
        country = random.choice(available_countries) if available_countries else random.choice(COUNTRIES)
        
        DATA["users"][uid] = {
            "country": country,
            "meat": 200,
            "wood": 150,
            "soldiers": 20,
            "tanks": 0,
            "jets": 0,
            "missiles": 0,
            "radar": 0,
            "diamonds": 100,
            "score": 0,
            "shield": 0,
            "last_attack": 0,
            "last_work": 0,
            "work_started": 0,
            "alliance": None,
            "last_treasure_hunt": 0,
            "last_question": 0,
        }
        save_data()
    
    if uid not in DATA["buildings"]:
        DATA["buildings"][uid] = {
            "farm": {"level": 1, "last_collected": time.time(), "type": "farm", "production": 60},
            "factory": {"level": 1, "last_collected": time.time(), "type": "factory", "production": 40},
            "mine": {"level": 1, "last_collected": time.time(), "type": "mine", "production": 10}
        }
        save_data()

def start_menu():
    kb = ChatKeypadBuilder()
    kb.row(kb.button(id="start", text="شروع بازی"))
    return kb.build()

def main_menu():
    kb = ChatKeypadBuilder()
    kb.row(kb.button(id="inventory", text="موجودی"))
    kb.row(kb.button(id="shop", text="فروشگاه 🛒"))
    kb.row(kb.button(id="attack", text="حمله"))
    kb.row(kb.button(id="defense", text="پدافند 🛡️"))
    kb.row(kb.button(id="buildings", text="ساختمان‌ها 🏗️"))
    kb.row(kb.button(id="work", text="کار 👷"))
    kb.row(kb.button(id="commanders", text="فرماندهان"))
    kb.row(kb.button(id="alliance", text="اتحادیه"))
    kb.row(kb.button(id="transfer", text="انتقال منابع"))
    kb.row(kb.button(id="treasure", text="شکار گنج 🏴‍☠️"))
    kb.row(kb.button(id="quiz", text="سوال روز 🎯"))
    kb.row(kb.button(id="delete", text="حذف فرماندهی"))
    return kb.build()

def shop_menu():
    kb = ChatKeypadBuilder()
    kb.row(kb.button(id="buy_soldier", text="خرید سرباز (10 گوشت)"))
    kb.row(kb.button(id="buy_tank", text="خرید تانک (100 چوب)"))
    kb.row(kb.button(id="buy_jet", text="خرید جنگنده (20 الماس)"))
    kb.row(kb.button(id="convert_meat", text="تبدیل گوشت به چوب"))
    kb.row(kb.button(id="convert_wood", text="تبدیل چوب به الماس"))
    kb.row(kb.button(id="back", text="بازگشت"))
    return kb.build()

def attack_menu():
    kb = ChatKeypadBuilder()
    kb.row(kb.button(id="attack_random", text="حمله شانسی"))
    kb.row(kb.button(id="attack_missile", text="شلیک موشک 🚀"))
    kb.row(kb.button(id="back", text="بازگشت"))
    return kb.build()

def defense_menu():
    kb = ChatKeypadBuilder()
    kb.row(kb.button(id="defense_info", text="اطلاعات پدافند"))
    kb.row(kb.button(id="buy_missile", text="خرید موشک 🚀"))
    kb.row(kb.button(id="buy_shield", text="خرید سپر 🛡️"))
    kb.row(kb.button(id="buy_radar", text="خرید رادار 📡"))
    kb.row(kb.button(id="back", text="بازگشت"))
    return kb.build()

def buildings_menu():
    kb = ChatKeypadBuilder()
    kb.row(kb.button(id="farm", text="مزرعه 🐓"))
    kb.row(kb.button(id="factory", text="کارخانه 🌲"))
    kb.row(kb.button(id="mine", text="معدن 💎"))
    kb.row(kb.button(id="back", text="بازگشت"))
    return kb.build()

def farm_menu():
    kb = ChatKeypadBuilder()
    kb.row(kb.button(id="farm_collect", text="جمع‌آوری محصول"))
    kb.row(kb.button(id="farm_upgrade", text="ارتقا مزرعه"))
    kb.row(kb.button(id="farm_info", text="اطلاعات مزرعه"))
    kb.row(kb.button(id="back", text="بازگشت"))
    return kb.build()

def factory_menu():
    kb = ChatKeypadBuilder()
    kb.row(kb.button(id="factory_collect", text="جمع‌آوری چوب"))
    kb.row(kb.button(id="factory_upgrade", text="ارتقا کارخانه"))
    kb.row(kb.button(id="factory_info", text="اطلاعات کارخانه"))
    kb.row(kb.button(id="back", text="بازگشت"))
    return kb.build()

def mine_menu():
    kb = ChatKeypadBuilder()
    kb.row(kb.button(id="mine_collect", text="جمع‌آوری الماس"))
    kb.row(kb.button(id="mine_upgrade", text="ارتقا معدن"))
    kb.row(kb.button(id="mine_info", text="اطلاعات معدن"))
    kb.row(kb.button(id="back", text="بازگشت"))
    return kb.build()

def work_menu():
    kb = ChatKeypadBuilder()
    kb.row(kb.button(id="work_start", text="شروع کار"))
    kb.row(kb.button(id="work_collect", text="دریافت حقوق"))
    kb.row(kb.button(id="back", text="بازگشت"))
    return kb.build()

def alliance_menu():
    kb = ChatKeypadBuilder()
    kb.row(kb.button(id="alliance_list", text="لیست اتحادیه‌ها"))
    kb.row(kb.button(id="alliance_create", text="ساخت اتحادیه"))
    kb.row(kb.button(id="alliance_join", text="پیوستن به اتحادیه"))
    kb.row(kb.button(id="alliance_leave", text="خروج از اتحادیه"))
    kb.row(kb.button(id="alliance_my", text="اتحادیه من"))
    kb.row(kb.button(id="back", text="بازگشت"))
    return kb.build()

def transfer_menu():
    kb = ChatKeypadBuilder()
    kb.row(kb.button(id="transfer_info", text="اطلاعات انتقال"))
    kb.row(kb.button(id="transfer_send", text="ارسال منابع"))
    kb.row(kb.button(id="back", text="بازگشت"))
    return kb.build()

def treasure_menu():
    kb = ChatKeypadBuilder()
    kb.row(kb.button(id="treasure_hunt", text="شکار گنج"))
    kb.row(kb.button(id="treasure_info", text="اطلاعات گنج‌ها"))
    kb.row(kb.button(id="back", text="بازگشت"))
    return kb.build()

@bot.on_message()
def handler(bot_obj, message: Message):
    try:
        uid = str(message.chat_id)
        text = (message.text or "").strip()
        
        print(f"دریافت پیام از {uid}: {text}")
        
        current_state = user_states.get(uid, "")
        
        # بررسی پاسخ به سوال
        if uid in user_questions and user_questions[uid].get("asked_at", 0) > time.time() - 300:  # 5 دقیقه فرصت پاسخ
            result = check_answer(uid, text)
            if result:
                # اعمال جایزه
                user = DATA["users"][uid]
                user["meat"] += result["reward"]["meat"]
                user["wood"] += result["reward"]["wood"]
                user["diamonds"] += result["reward"]["diamonds"]
                save_data()
                
                message.reply_keypad(result["message"], keypad=main_menu())
                return
            else:
                # اگر پاسخ نامعتبر بود، سوال را حذف کنیم
                del user_questions[uid]
        
        # شروع بازی
        if text == "/start":
            welcome_msg = random.choice(RANDOM_MESSAGES["welcome"])
            message.reply_keypad(f"{welcome_msg}", keypad=start_menu())
            user_states[uid] = ""
            return
        
        if text == "start" or text == "شروع بازی":
            init_user_data(uid)
            user = DATA["users"][uid]
            country_flag = COUNTRY_FLAGS.get(user['country'], "🏴")
            welcome_msg = random.choice(RANDOM_MESSAGES["welcome"])
            reaction = get_random_reaction("success")
            message.reply_keypad(f"{reaction} {welcome_msg}\n\n✅ کشور شما: {country_flag} {user['country']}", keypad=main_menu())
            user_states[uid] = ""
            return
        
        if uid not in DATA["users"]:
            message.reply_keypad("❌ لطفا اول بازی را شروع کنید", keypad=start_menu())
            return
        
        user = DATA["users"][uid]
        
        # سوال روز
        if text == "quiz" or text == "سوال روز 🎯":
            now = time.time()
            if now - user.get("last_question", 0) < 3600:  # 1 ساعت بین سوالات
                remaining = 3600 - (now - user.get("last_question", 0))
                minutes = int(remaining // 60)
                message.reply_keypad(f"⏳ {minutes} دقیقه دیگر می‌توانی سوال بعدی را بپرسی", keypad=main_menu())
                return
            
            question = ask_random_question(uid)
            user["last_question"] = now
            save_data()
            
            kb = ChatKeypadBuilder()
            kb.row(kb.button(id="answer_quiz", text="پاسخ دادن ✍️"))
            kb.row(kb.button(id="back", text="بازگشت"))
            
            message.reply_keypad(f"🎯 سوال روز:\n\n{question}\n\nبرای پاسخ دادن دکمه زیر را بزن:", keypad=kb.build())
            return
        
        elif text == "answer_quiz" or text == "پاسخ دادن ✍️":
            if uid in user_questions:
                message.reply("💭 پاسخ خود را به سوال بالا وارد کنید:")
                user_states[uid] = "answering_quiz"
            else:
                message.reply_keypad("❌ سوال فعالی ندارید", keypad=main_menu())
            return
        
        # منوی اصلی - پردازش کلیک دکمه‌ها
        if text == "inventory" or text == "موجودی":
            country_flag = COUNTRY_FLAGS.get(user.get('country', ''), "🏴")
            shield = "فعال" if user.get("shield", 0) > time.time() else "غیرفعال"
            alliance = user.get("alliance", "ندارد")
            
            # ری‌اکشن تصادفی
            reaction = get_random_reaction("resources")
            
            msg = f"""{reaction} موجودی کشور {country_flag} {user.get('country', 'ناشناس')}:

🏆 امتیاز: {user.get('score', 0)}
🤝 اتحادیه: {alliance}
🛡️ سپر: {shield}

💎 الماس: {user.get('diamonds', 0)}
🍖 گوشت: {user.get('meat', 0)}
🌲 چوب: {user.get('wood', 0)}

🎖️ نیروها:
• سربازان: {user.get('soldiers', 0)}
• تانک: {user.get('tanks', 0)}
• جنگنده: {user.get('jets', 0)}
• موشک: {user.get('missiles', 0)}
• رادار: {user.get('radar', 0)}"""
            
            message.reply_keypad(msg, keypad=main_menu())
            return
        
        elif text == "shop" or text == "فروشگاه 🛒":
            reaction = get_random_reaction("shop")
            message.reply_keypad(f"{reaction} فروشگاه:", keypad=shop_menu())
            return
        
        elif text == "buy_soldier" or text == "خرید سرباز (10 گوشت)":
            if user.get("meat", 0) >= 10:
                user["meat"] -= 10
                user["soldiers"] = user.get("soldiers", 0) + 1
                save_data()
                reaction = get_random_reaction("success")
                message.reply_keypad(f"{reaction} 1 سرباز خریداری شد (10 گوشت کسر شد)", keypad=shop_menu())
            else:
                reaction = get_random_reaction("failure")
                message.reply_keypad(f"{reaction} گوشت کافی نیست", keypad=shop_menu())
            return
        
        elif text == "buy_tank" or text == "خرید تانک (100 چوب)":
            if user.get("wood", 0) >= 100:
                user["wood"] -= 100
                user["tanks"] = user.get("tanks", 0) + 1
                save_data()
                reaction = get_random_reaction("success")
                message.reply_keypad(f"{reaction} 1 تانک خریداری شد (100 چوب کسر شد)", keypad=shop_menu())
            else:
                reaction = get_random_reaction("failure")
                message.reply_keypad(f"{reaction} چوب کافی نیست", keypad=shop_menu())
            return
        
        elif text == "buy_jet" or text == "خرید جنگنده (20 الماس)":
            if user.get("diamonds", 0) >= 20:
                user["diamonds"] -= 20
                user["jets"] = user.get("jets", 0) + 1
                save_data()
                reaction = get_random_reaction("success")
                message.reply_keypad(f"{reaction} 1 جنگنده خریداری شد (20 الماس کسر شد)", keypad=shop_menu())
            else:
                reaction = get_random_reaction("failure")
                message.reply_keypad(f"{reaction} الماس کافی نیست", keypad=shop_menu())
            return
        
        elif text == "attack" or text == "حمله":
            reaction = get_random_reaction("attack")
            message.reply_keypad(f"{reaction} انتخاب نوع حمله:", keypad=attack_menu())
            return
        
        elif text == "attack_random" or text == "حمله شانسی":
            now = time.time()
            if now - user.get("last_attack", 0) < 300:
                remaining = 300 - (now - user.get("last_attack", 0))
                minutes = int(remaining // 60)
                seconds = int(remaining % 60)
                message.reply_keypad(f"⏳ {minutes}دقیقه {seconds}ثانیه صبر کن", keypad=main_menu())
                return
            
            targets = [tid for tid, t in DATA["users"].items() if tid != uid]
            
            if not targets:
                message.reply_keypad("🎯 حریف پیدا نشد", keypad=main_menu())
                return
            
            target_uid = random.choice(targets)
            target = DATA["users"][target_uid]
            
            if random.random() < 0.7:  # 70% شانس موفقیت
                loot_m = min(target.get("meat", 0), random.randint(50, 150))
                loot_w = min(target.get("wood", 0), random.randint(30, 100))
                loot_d = min(target.get("diamonds", 0), random.randint(1, 10))
                
                user["meat"] += loot_m
                user["wood"] += loot_w
                user["diamonds"] += loot_d
                user["last_attack"] = now
                save_data()
                
                attack_msg = get_random_message("attack_success")
                reaction = get_random_reaction("attack")
                message.reply_keypad(f"{reaction} {attack_msg}\n🎯 غارت: {int(loot_m)}گ {int(loot_w)}چ {int(loot_d)}الماس", keypad=main_menu())
            else:
                lost = min(user.get("soldiers", 0), random.randint(5, 15))
                user["soldiers"] -= lost
                user["last_attack"] = now
                save_data()
                
                attack_msg = get_random_message("attack_failure")
                reaction = get_random_reaction("failure")
                message.reply_keypad(f"{reaction} {attack_msg}\n💀 تلفات: {lost} سرباز", keypad=main_menu())
            return
        
        elif text == "attack_missile" or text == "شلیک موشک 🚀":
            if user.get("missiles", 0) <= 0:
                message.reply_keypad("❌ موشک ندارید", keypad=attack_menu())
                return
            
            now = time.time()
            if now - user.get("last_attack", 0) < 180:
                remaining = 180 - (now - user.get("last_attack", 0))
                minutes = int(remaining // 60)
                seconds = int(remaining % 60)
                message.reply_keypad(f"⏳ {minutes}دقیقه {seconds}ثانیه صبر کن", keypad=main_menu())
                return
            
            targets = [tid for tid, t in DATA["users"].items() if tid != uid]
            
            if not targets:
                message.reply_keypad("🎯 حریف پیدا نشد", keypad=attack_menu())
                return
            
            target_uid = random.choice(targets)
            target = DATA["users"][target_uid]
            
            # موشک همیشه موفق است
            user["missiles"] -= 1
            
            # غارت بیشتر با موشک
            loot_m = min(target.get("meat", 0), random.randint(100, 300))
            loot_w = min(target.get("wood", 0), random.randint(80, 200))
            loot_d = min(target.get("diamonds", 0), random.randint(5, 20))
            
            user["meat"] += loot_m
            user["wood"] += loot_w
            user["diamonds"] += loot_d
            target["meat"] = max(0, target.get("meat", 0) - loot_m)
            target["wood"] = max(0, target.get("wood", 0) - loot_w)
            target["diamonds"] = max(0, target.get("diamonds", 0) - loot_d)
            
            user["last_attack"] = now
            save_data()
            
            reaction = get_random_reaction("attack")
            message.reply_keypad(f"{reaction} موشک شلیک شد!\n🎯 غارت: {int(loot_m)}گ {int(loot_w)}چ {int(loot_d)}الماس", keypad=main_menu())
            return
        
        elif text == "defense" or text == "پدافند 🛡️":
            reaction = get_random_reaction("defense")
            message.reply_keypad(f"{reaction} سیستم پدافند:", keypad=defense_menu())
            return
        
        elif text == "buy_missile" or text == "خرید موشک 🚀":
            if user.get("diamonds", 0) >= 30:
                user["diamonds"] -= 30
                user["missiles"] = user.get("missiles", 0) + 1
                save_data()
                reaction = get_random_reaction("success")
                message.reply_keypad(f"{reaction} 1 موشک خریداری شد (30 الماس کسر شد)", keypad=defense_menu())
            else:
                reaction = get_random_reaction("failure")
                message.reply_keypad(f"{reaction} الماس کافی نیست", keypad=defense_menu())
            return
        
        elif text == "buy_shield" or text == "خرید سپر 🛡️":
            if user.get("diamonds", 0) >= 50:
                user["diamonds"] -= 50
                user["shield"] = time.time() + (6 * 3600)  # 6 ساعت
                save_data()
                reaction = get_random_reaction("success")
                message.reply_keypad(f"{reaction} سپر برای 6 ساعت فعال شد (50 الماس کسر شد)", keypad=defense_menu())
            else:
                reaction = get_random_reaction("failure")
                message.reply_keypad(f"{reaction} الماس کافی نیست", keypad=defense_menu())
            return
        
        elif text == "buy_radar" or text == "خرید رادار 📡":
            if user.get("diamonds", 0) >= 50:
                user["diamonds"] -= 50
                user["radar"] = user.get("radar", 0) + 1
                save_data()
                reaction = get_random_reaction("success")
                message.reply_keypad(f"{reaction} 1 رادار خریداری شد (50 الماس کسر شد)", keypad=defense_menu())
            else:
                reaction = get_random_reaction("failure")
                message.reply_keypad(f"{reaction} الماس کافی نیست", keypad=defense_menu())
            return
        
        elif text == "buildings" or text == "ساختمان‌ها 🏗️":
            reaction = get_random_reaction("building")
            message.reply_keypad(f"{reaction} مدیریت ساختمان‌ها:", keypad=buildings_menu())
            return
        
        elif text == "work" or text == "کار 👷":
            reaction = get_random_reaction("work")
            message.reply_keypad(f"{reaction} سیستم کار:", keypad=work_menu())
            return
        
        elif text == "work_start" or text == "شروع کار":
            if user.get("work_started", 0) > time.time() - 3600:
                remaining = 3600 - (time.time() - user.get("work_started", 0))
                minutes = int(remaining // 60)
                message.reply_keypad(f"⏳ {minutes} دقیقه صبر کن", keypad=work_menu())
                return
            
            user["work_started"] = time.time()
            save_data()
            reaction = get_random_reaction("work")
            message.reply_keypad(f"{reaction} کار شروع شد! بعد از 1 ساعت برگرد", keypad=work_menu())
            return
        
        elif text == "work_collect" or text == "دریافت حقوق":
            if not user.get("work_started"):
                message.reply_keypad("❌ اول باید کار شروع کنی", keypad=work_menu())
                return
            
            work_time = time.time() - user.get("work_started", 0)
            if work_time < 3600:
                remaining = 3600 - work_time
                minutes = int(remaining // 60)
                message.reply_keypad(f"⏳ {minutes} دقیقه دیگر آماده است", keypad=work_menu())
                return
            
            salary_meat = random.randint(50, 100)
            salary_wood = random.randint(30, 70)
            salary_diamonds = random.randint(1, 5)
            
            user["meat"] += salary_meat
            user["wood"] += salary_wood
            user["diamonds"] += salary_diamonds
            user["work_started"] = 0
            save_data()
            
            work_msg = get_random_message("work_success")
            reaction = get_random_reaction("success")
            
            message.reply_keypad(f"""{reaction} {work_msg}

🍖 {salary_meat} گوشت
🌲 {salary_wood} چوب
💎 {salary_diamonds} الماس""", keypad=work_menu())
            return
        
        elif text == "commanders" or text == "فرماندهان":
            commanders = list(DATA["users"].values())
            if not commanders:
                message.reply_keypad("❌ هنوز فرماندهی وجود ندارد", keypad=main_menu())
                return
            
            commanders.sort(key=lambda x: x.get("score", 0), reverse=True)
            result = "🏆 5 فرمانده برتر:\n\n"
            for i, cmd in enumerate(commanders[:5], 1):
                country_flag = COUNTRY_FLAGS.get(cmd.get('country', ''), "🏴")
                result += f"{i}. {country_flag} {cmd.get('country', 'ناشناس')}\n   امتیاز: {cmd.get('score', 0)}\n\n"
            message.reply_keypad(result, keypad=main_menu())
            return
        
        elif text == "alliance" or text == "اتحادیه":
            reaction = get_random_reaction("alliance")
            message.reply_keypad(f"{reaction} سیستم اتحادیه:", keypad=alliance_menu())
            return
        
        # سیستم انتقال منابع
        elif text == "transfer" or text == "انتقال منابع":
            reaction = get_random_reaction("resources")
            message.reply_keypad(f"{reaction} سیستم انتقال منابع", keypad=transfer_menu())
            return
        
        elif text == "transfer_info" or text == "اطلاعات انتقال":
            info_msg = """
💰 اطلاعات سیستم انتقال منابع:

📊 محدودیت‌های روزانه:
• هر کاربر می‌تواند به ۱ نفر در روز منابع بدهد
• هر کاربر می‌تواند از ۲ نفر در روز منابع بگیرد

💡 نحوه استفاده:
1. روی 'ارسال منابع' کلیک کنید
2. نام کشور مقصد را وارد کنید
3. نوع و مقدار منبع را انتخاب کنید

⏰ بازنشانی: هر روز صبح
"""
            message.reply_keypad(info_msg, keypad=transfer_menu())
            return
        
        elif text == "transfer_send" or text == "ارسال منابع":
            message.reply("🔍 نام کشور مورد نظر برای ارسال منابع را وارد کنید:")
            user_states[uid] = "transfer_find_user"
            return
        
        # سیستم شکار گنج
        elif text == "treasure" or text == "شکار گنج 🏴‍☠️":
            reaction = get_random_reaction("treasure")
            message.reply_keypad(f"{reaction} سیستم شکار گنج", keypad=treasure_menu())
            return
        
        elif text == "treasure_info" or text == "اطلاعات گنج‌ها":
            info_msg = """
🏴‍☠️ اطلاعات سیستم شکار گنج:

⏰ زمان انتظار: ۶ ساعت بین هر شکار

🎁 انواع گنج:
• معمولی (۶۰٪): منابع پایه
• نادر (۲۵٪): منابع + موشک
• افسانه‌ای (۱۰٪): منابع زیاد + جنگنده
• سلطنتی (۵٪): منابع بسیار زیاد + جوایز ویژه

💎 جوایز ممکن:
🍖 گوشت, 🌲 چوب, 💎 الماس
🎖️ سرباز, 🚀 موشک, ✈️ جنگنده
"""
            message.reply_keypad(info_msg, keypad=treasure_menu())
            return
        
        elif text == "treasure_hunt" or text == "شکار گنج":
            now = time.time()
            if now - user.get("last_treasure_hunt", 0) < 6 * 3600:
                remaining = 6 * 3600 - (now - user.get("last_treasure_hunt", 0))
                hours = int(remaining // 3600)
                minutes = int((remaining % 3600) // 60)
                message.reply_keypad(f"⏳ باید {hours} ساعت و {minutes} دقیقه صبر کنید", keypad=treasure_menu())
                return
            
            # شکار گنج ساده
            rewards = {
                "meat": random.randint(50, 150),
                "wood": random.randint(30, 100),
                "diamonds": random.randint(5, 20)
            }
            
            user["meat"] += rewards["meat"]
            user["wood"] += rewards["wood"]
            user["diamonds"] += rewards["diamonds"]
            user["last_treasure_hunt"] = now
            save_data()
            
            treasure_msg = get_random_message("treasure_success")
            reaction = get_random_reaction("treasure")
            
            message.reply_keypad(f"""{reaction} {treasure_msg}

🎁 جوایز:
🍖 {rewards['meat']} گوشت
🌲 {rewards['wood']} چوب
💎 {rewards['diamonds']} الماس""", keypad=treasure_menu())
            return
        
        # پردازش حالت‌های خاص
        elif current_state == "transfer_find_user":
            target_country = text.strip()
            target_uid = None
            
            for user_id, user_data in DATA["users"].items():
                if user_data.get("country") == target_country and user_id != uid:
                    target_uid = user_id
                    break
            
            if target_uid:
                user_states[uid] = f"transfer_select_{target_uid}"
                target_user = DATA["users"][target_uid]
                target_flag = COUNTRY_FLAGS.get(target_user.get('country', ''), "🏴")
                message.reply(f"✅ کاربر پیدا شد: {target_flag} {target_country}\n\nلطفا مقدار منابع برای ارسال را وارد کنید (مثلاً: 50 گوشت):")
            else:
                message.reply("❌ کاربری با این نام کشور پیدا نشد")
                user_states[uid] = ""
            return
        
        elif current_state.startswith("transfer_select_"):
            target_uid = current_state.split("_")[2]
            
            try:
                # پردازش ورودی کاربر (مثلاً: "50 گوشت")
                parts = text.split()
                if len(parts) >= 2:
                    amount = int(parts[0])
                    resource_type = parts[1]
                    
                    if resource_type in ["گوشت", "چوب", "الماس"]:
                        # تبدیل به انگلیسی برای استفاده در کد
                        resource_map = {"گوشت": "meat", "چوب": "wood", "الماس": "diamonds"}
                        resource_key = resource_map[resource_type]
                        
                        if user.get(resource_key, 0) >= amount:
                            target_user = DATA["users"][target_uid]
                            user[resource_key] -= amount
                            target_user[resource_key] = target_user.get(resource_key, 0) + amount
                            save_data()
                            
                            target_flag = COUNTRY_FLAGS.get(target_user.get('country', ''), "🏴")
                            transfer_msg = get_random_message("transfer_success")
                            reaction = get_random_reaction("success")
                            message.reply_keypad(f"{reaction} {transfer_msg}\n{amount} {resource_type} به {target_flag} {target_user.get('country')} ارسال شد.", keypad=transfer_menu())
                        else:
                            reaction = get_random_reaction("failure")
                            message.reply_keypad(f"{reaction} {resource_type} کافی ندارید", keypad=transfer_menu())
                    else:
                        message.reply("❌ لطفا نوع منبع را صحیح وارد کنید (گوشت، چوب یا الماس)")
                else:
                    message.reply("❌ فرمت صحیح: مقدار و نوع منبع (مثلاً: 50 گوشت)")
                
                user_states[uid] = ""
                
            except ValueError:
                message.reply("❌ لطفا یک عدد معتبر وارد کنید")
            return
        
        # دکمه بازگشت
        elif text == "back" or text == "بازگشت":
            message.reply_keypad("🏠 منوی اصلی", keypad=main_menu())
            user_states[uid] = ""
            return
        
        # اگر هیچکدام از دستورات بالا نبود
        message.reply_keypad("❌ لطفا از دکمه‌های منو استفاده کنید", keypad=main_menu())
        
    except Exception as e:
        print(f"خطا: {e}")
        import traceback
        traceback.print_exc()
        try:
            message.reply("⚠️ خطایی رخ داد، لطفا دوباره تلاش کنید")
        except:
            pass

print("✅ ربات فعال شد")
print(f"🌍 تعداد کشورها: {len(COUNTRIES)} کشور")
print("🎯 ویژگی‌های جدید:")
print("  • ۱۵۰ کشور مختلف با پرچم")
print("  • سیستم سوال و جواب با جایزه")
print("  • ری‌اکشن‌های متنوع برای پیام‌ها")
print("  • پیام‌های تصادفی برای رویدادها")
print("  • تجربه کاربری پویا و جذاب")

# اجرای ربات با مدیریت خطا
try:
    bot.run()
except Exception as e:
    print(f"❌ خطا در اجرای ربات: {e}")