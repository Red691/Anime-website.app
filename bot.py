import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatMemberStatus

API_ID = int(os.getenv("API_ID"20594537"))
API_HASH = os.getenv("API_HASH"c505a4e5bb7d482197875888af544f17")
BOT_TOKEN = os.getenv("BOT_TOKEN"7280187591:AAG-aaAesc20QDzvu1G2SCU_xq5MQHVMB68")

app = Client(
    "inline_replace_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ---------------- START ----------------
@app.on_message(filters.private & filters.command("start"))
async def start(_, message):
    await message.reply_text(
        "✅ **Bot Alive Hai!**\n\n"
        "Use /help to see usage."
    )

# ---------------- HELP ----------------
@app.on_message(filters.private & filters.command("help"))
async def help_cmd(_, message):
    await message.reply_text(
        "**📌 How to Use**\n\n"
        "1️⃣ Bot ko channel me add karo\n"
        "2️⃣ Bot ko admin banao (Edit permission)\n"
        "3️⃣ Inline button wali post pe reply karo:\n\n"
        "`/replace old_link new_link`\n\n"
        "**Commands:**\n"
        "/start – Bot status\n"
        "/help – Usage\n"
        "/about – Credits"
    )

# ---------------- ABOUT ----------------
@app.on_message(filters.private & filters.command("about"))
async def about(_, message):
    await message.reply_text(
        "**🤖 Inline Button Replace Bot**\n\n"
        "Developer: Your Name\n"
        "Powered by Pyrogram 🚀"
    )

# ---------------- REPLACE COMMAND ----------------
@app.on_message(filters.command("replace"))
async def replace_buttons(client, message):
    if not message.reply_to_message:
        return await message.reply_text("❌ Post pe reply karo.")

    chat = message.chat
    user = await client.get_chat_member(chat.id, message.from_user.id)

    if user.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        return await message.reply_text("❌ Sirf admins use kar sakte hain.")

    if len(message.command) != 3:
        return await message.reply_text(
            "❌ Format galat hai!\n\n"
            "`/replace old_link new_link`"
        )

    old_link = message.command[1]
    new_link = message.command[2]

    post = message.reply_to_message

    if not post.reply_markup:
        return await message.reply_text("❌ Inline buttons nahi mile.")

    new_keyboard = []

    for row in post.reply_markup.inline_keyboard:
        new_row = []
        for btn in row:
            if btn.url:
                updated_url = btn.url.replace(old_link, new_link)
                new_row.append(
                    InlineKeyboardButton(text=btn.text, url=updated_url)
                )
            else:
                new_row.append(btn)
        new_keyboard.append(new_row)

    markup = InlineKeyboardMarkup(new_keyboard)

    try:
        await post.edit_reply_markup(reply_markup=markup)
        await message.reply_text("✅ Inline button link replace ho gaya!")
    except Exception as e:
        await message.reply_text(f"❌ Error: `{e}`")

app.run()
