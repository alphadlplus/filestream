from datetime import datetime
from WebStreamer.bot import StreamBot
from WebStreamer.vars import Var
from WebStreamer.utils.database import Database
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
db = Database()

START_TEXT = """👋 سلام به ربات تبدیل فایل به لینک مستقیم ربات آلفا دی ال خوش اومدی.

🔸 با عضویت در ربات اصلیمون ( <a href='https://t.me/alphadlbot'> AlphaDLBot</a> ) پلن رایگان دریافت می کنی که می تونی تا سقف 2 گیگابایت در روز فایل تبدیل کنی.

🔹 برای دریافت حجم بیشتر می تونی تو ربات اصلیمون از بخش پلن، پلن مورد نظرتو خریداری کنی.

🔸 تبدیل فایل به لینک مستقیم پرسرعت، فوری و آنی انجام میشه.

🔹 لینک های تبدیل شده قابلیت پخش آنلاین رو دارن. 
"""

HELP_TEXT = """
<i>🗂 برای دریافت لینک مستقیم فایل ها کافیه بفرستیشون اینجا</i>
<i>🔞 فایل یا ویدیو غیر اخلاقی نفرست (ما  همه چیزو می بینیم 😉) </i>
<i>☎️ اگه به مشکل خوردی یا خواستی با ما در ارتباط باشی</i> :
<a href='https://t.me/alphadlsup'>[ اینجا کلیک کن ]</a>"""

ABOUT_TEXT = """
🔸 کانال ما : <a href='https://telegram.me/alphadl'>AlphaDL</a>\n
🔹ربات دانلود فیلم و سریال : <a href='https://telegram.me/alphadlbot'>AlphaDLBot</a>\n
🔸گروه ما : <a href='https://telegram.me/alphadlgp'>AlphaDL Group</a>\n"""

START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Help', callback_data='help'),
        InlineKeyboardButton('About', callback_data='about'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Home', callback_data='home'),
        InlineKeyboardButton('About', callback_data='about'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Home', callback_data='home'),
        InlineKeyboardButton('Help', callback_data='help'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )

@StreamBot.on_callback_query()
async def cb_data(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=START_BUTTONS
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            disable_web_page_preview=True,
            reply_markup=HELP_BUTTONS
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT,
            disable_web_page_preview=True,
            reply_markup=ABOUT_BUTTONS
        )
    else:
        await update.message.delete()


@StreamBot.on_message(filters.command('start') & filters.private)
async def start(b, m):
    if db.check_user(m.from_user.id) == False :
        await b.send_message(
            Var.BIN_CHANNEL,
            f"**Nᴇᴡ Usᴇʀ Jᴏɪɴᴇᴅ:** \n\n__Mʏ Nᴇᴡ Fʀɪᴇɴᴅ__ [{m.from_user.first_name}](tg://user?id={m.from_user.id}) __Sᴛᴀʀᴛᴇᴅ Yᴏᴜʀ Bᴏᴛ !!__"
        )
        await b.send_message(
                        chat_id=m.chat.id,
                        text='''👋 سلام به ربات تبدیل فایل به لینک مستقیم ربات آلفا دی ال خوش اومدی.

🔸 با عضویت در ربات اصلیمون ( <a href='https://t.me/alphadlbot'> AlphaDLBot</a> ) پلن رایگان دریافت می کنی که می تونی تا سقف 2 گیگابایت در روز فایل تبدیل کنی.

🔹 برای دریافت حجم بیشتر می تونی تو ربات اصلیمون از بخش پلن، پلن مورد نظرتو خریداری کنی.

🔸 تبدیل فایل به لینک مستقیم پرسرعت، فوری و آنی انجام میشه.

🔹 لینک های تبدیل شده قابلیت پخش آنلاین رو دارن.''',
                        parse_mode=ParseMode.HTML,
                        disable_web_page_preview=True
        )
    if db.check_user(m.from_user.id) == True:
        usr_cmd = m.text.split("_")[-1]
        if usr_cmd == "/start":
            await m.reply_text(
                text=START_TEXT.format(m.from_user.mention),
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
                reply_markup=START_BUTTONS
                )                                                                         
@StreamBot.on_message(filters.private & filters.command('about'))
async def about_handler(bot, update):
    await update.reply_text(
        text=ABOUT_TEXT.format(update.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=ABOUT_BUTTONS
    )

@StreamBot.on_message(filters.command('info') & filters.private)
async def info_handler(bot, message):
    if db.check_user(message.from_user.id) == False :
        await bot.send_message(
                        chat_id=message.chat.id,
                        text='''
شما اشتراک ندارید برای خرید اشتراک به ایدی زیر پیام دهید.
<a href='https://t.me/alphadlsup'> AlphaDL Suport</a>''',
                        parse_mode=ParseMode.HTML,
                        disable_web_page_preview=True
        )
    if db.check_user(message.from_user.id) == True:
        info_data = db.info(message.from_user.id)
        try:
            await bot.send_message(
                            chat_id=message.chat.id,
                            text = '''یوزر ایدی : {}
پلن کاربری : {}
حجم روزانه : GB {}
روز های باقی مانده از اشتراک شما : {}
<a href='https://t.me/alphadl'> AlphaDL</a>'''.format(info_data['from_id'], info_data['accountType'], info_data['dailyUsage'], str(datetime.fromtimestamp(int(info_data['expireStamp'])) - datetime.now()).split(" day")[0] if len(str(datetime.fromtimestamp(int(info_data['expireStamp'])) - datetime.now()).split(" day")) == 2 else '0'),
                            parse_mode = ParseMode.HTML,
                            disable_web_page_preview=True
            )
        except ValueError:
            await bot.send_message(
                            chat_id=message.chat.id,
                            text = '''یوزر ایدی : {}
پلن کاربری : {}
حجم روزانه : GB {}
روز های باقی مانده از اشتراک شما : {}
<a href='https://t.me/alphadl'> AlphaDL</a>'''.format(info_data['from_id'], "Free", info_data['dailyUsage'], 'Unlimited'),
                            parse_mode = ParseMode.HTML,
                            disable_web_page_preview=True
            )

@StreamBot.on_message(filters.command('help') & filters.private)
async def help_handler(bot, message):
    if db.check_user(message.from_user.id) == False :
        await bot.send_message(
                        chat_id=m.chat.id,
                        text='''شما اشتراک ندارید برای خرید اشتراک به ایدی زیر پیام دهید.
<a href='https://t.me/alphadlsup'> AlphaDL Suport</a>''',
                        parse_mode=ParseMode.HTML,
                        disable_web_page_preview=True
        )
    if db.check_user(message.from_user.id) == True:
        await message.reply_text(
            text=HELP_TEXT,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
            reply_markup=HELP_BUTTONS
            )
