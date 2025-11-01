from rubka import Robot
from rubka.context import Message
from deep_translator import GoogleTranslator

bot = Robot(token="ECBHI0MKCODQDQOUNOGDHMWOKAPIQMQSCKVNQGZLKEZPMKAVBEGIZCJVDPLIAEJY")

LANG_CODES = {
    "/en": "en",
    "/fa": "fa",
    "/fr": "fr",
    "/de": "de",
    "/it": "it",
    "/es": "es",
    "/ru": "ru",
    "/ar": "ar",
    "/ja": "ja",
    "/zh": "zh"
}

@bot.on_message()
def translate(bot, message: Message):
    user_input = message.text.strip() if message.text else ""

    for cmd, lang_code in LANG_CODES.items():
        if user_input.startswith(cmd):
            text = user_input[len(cmd):].strip()
            if not text:
                return message.reply("⚠️ لطفاً متنی برای ترجمه وارد کن.")
            try:
                translated = GoogleTranslator(source='auto', target=lang_code).translate(text)
                return message.reply(f"✅ ترجمه به [{lang_code}]:\n{translated}")
            except Exception as e:
                return message.reply("❌ خطایی در ترجمه رخ داد.")

    if user_input.startswith("/start"):
        langs = GoogleTranslator().get_supported_languages(as_dict=True)
        result = "\n".join([
            f"{cmd} ➜ {langs.get(lang_code, lang_code)}"
            for cmd, lang_code in LANG_CODES.items()
        ])
        return message.reply(
            "👋 خوش اومدی!\n"
            "برای ترجمه، یکی از این دستورات رو بفرست:\n\n" + result
        )

    return message.reply("❗ لطفاً یکی از دستورات ترجمه رو وارد کن.")

bot.run()
