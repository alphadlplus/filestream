# alphadl
import asyncio
import requests
from datetime import datetime, timedelta
from WebStreamer.bot import StreamBot
from WebStreamer.utils.database import Database
from WebStreamer.utils.human_readable import humanbytes, size_gb
from WebStreamer.vars import Var
from pyrogram import filters, Client
from pyrogram.enums import ParseMode
from pyrogram.errors import FloodWait
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
db = Database()


@StreamBot.on_message(filters.private & (filters.document | filters.video | filters.audio), group=4)
async def private_receive_handler(c: Client, m: Message):
    accountType = db.info(m.from_user.id)
    check_status = db.check_status(m.from_user.id)
    if check_status == False:
        await c.send_message(
            chat_id=m.chat.id,
            text='''سلام
شما اشتراک ندارید برای خرید اشتراک به ایدی زیر پیام دهید.
<a href='https://t.me/alphadlsup'> AlphaDL Suport</a>''',
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
    if accountType['accountType'] == "free":
        await c.send_message(
            chat_id=m.chat.id,
            text='''سلام
شما اشتراک ندارید برای خرید اشتراک به ایدی زیر پیام دهید.
<a href='https://t.me/alphadlsup'> AlphaDL Suport</a>''',
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
    if accountType['accountType'] != "free":
        try:
            file_size = None
            size_file = None
            if m.video:
                size_file = m.video.file_size
                file_size = f"{humanbytes(m.video.file_size)}"
            elif m.document:
                size_file = m.document.file_size
                file_size = f"{humanbytes(m.document.file_size)}"
            elif m.audio:
                size_file = m.audio.file_size
                file_size = f"{humanbytes(m.audio.file_size)}"

            file_name = None
            if m.video:
                file_name = f"{m.video.file_name}"
            elif m.document:
                file_name = f"{m.document.file_name}"
            elif m.audio:
                file_name = f"{m.audio.file_name}"

            msg_text = """<b><u> لینک دانلود آمادست</u></b>
📂 نام فایل : {}
📦 اندازه فایل : {}
📥 لینک دانلود : {}
🚸 نکته : لینک پس از 24 ساعت منقضی می شود
🍃 کانال ما : <a href='https://t.me/alphadl'> AlphaDL</a>"""
            if check_status == True:
                if db.check_dailyusage(m.from_user.id, size_gb(size_file)) == True:
                    log_msg = await m.forward(chat_id=Var.BIN_CHANNEL)
                    stream_link = "https://{}/{}/{}".format(Var.FQDN, log_msg.id, file_name) if Var.ON_HEROKU or Var.NO_PORT else \
                        "http://{}/{}/{}".format(Var.FQDN,log_msg.id, file_name)
                    url_encod = requests.utils.quote(
                        stream_link)
                    url_encod = url_encod.replace("%3A", ":", 2)
                    #short_link = db.shourt_link(stream_link)
                    qwe = db.set_data(int(log_msg.id), int(datetime.timestamp(datetime.now() + timedelta(hours=24))))
                    await log_msg.reply_text(text=f"**RᴇQᴜᴇꜱᴛᴇᴅ ʙʏ :** [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n**Uꜱᴇʀ ɪᴅ :** `{m.from_user.id}`\n**Dᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ :** {url_encod}", disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN, quote=True)
                    await m.reply_text(
                        text=msg_text.format(file_name, file_size, url_encod),
                        parse_mode=ParseMode.HTML,
                        disable_web_page_preview=True,
                        # reply_markup=InlineKeyboardMarkup(
                        #     [[InlineKeyboardButton("دانلود 📥", url=url_encod)]]),
                        quote=True
                    )
                else:
                    await m.reply_text(
                        text='''**حجم استفاده روزانه شما کافی نیست**\n
 حجم باقی مانده : {} '''.format(accountType['dailyUsage']+' GB'),
                        parse_mode=ParseMode.MARKDOWN,
                        disable_web_page_preview=True

                    )
            else:
                await m.reply_text(
                    text='''شما اشتراک ندارید برای خرید اشتراک به ایدی زیر پیام دهید.
<a href='https://t.me/alphadlsup'> AlphaDL Suport</a>''',
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True
                )
        except FloodWait as e:
            print(f"Sleeping for {str(e.x)}s")
            await asyncio.sleep(e.x)
            await c.send_message(chat_id=Var.BIN_CHANNEL, text=f"Gᴏᴛ FʟᴏᴏᴅWᴀɪᴛ ᴏғ {str(e.x)}s from [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n\n**𝚄𝚜𝚎𝚛 𝙸𝙳 :** `{str(m.from_user.id)}`", disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)


# @StreamBot.on_message(filters.channel & (filters.document | filters.video) & ~filters.edited, group=-1)
# async def channel_receive_handler(bot, broadcast):
#     if int(broadcast.chat.id) in Var.BANNED_CHANNELS:
#         await bot.leave_chat(broadcast.chat.id)
#         return
#     try:
#         log_msg = await broadcast.forward(chat_id=Var.BIN_CHANNEL)
#         stream_link = "https://{}/{}".format(Var.FQDN, log_msg.message_id) if Var.ON_HEROKU or Var.NO_PORT else \
#             "http://{}:{}/{}".format(Var.FQDN,
#                                     Var.PORT,
#                                     log_msg.message_id)
#         url_encod = requests.utils.quote(stream_link).replace("%3A",":",1)

#         await log_msg.reply_text(
#             text=f"**Cʜᴀɴɴᴇʟ Nᴀᴍᴇ:** `{broadcast.chat.title}`\n**Cʜᴀɴɴᴇʟ ID:** `{broadcast.chat.id}`\n**Rᴇǫᴜᴇsᴛ ᴜʀʟ:** {url_encod}",
#             quote=True,
#             parse_mode="Markdown"
#         )
#         await bot.edit_message_reply_markup(
#             chat_id=broadcast.chat.id,
#             message_id=broadcast.message_id,
#             reply_markup=InlineKeyboardMarkup(
#                 [[InlineKeyboardButton("Dᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ 📥", url=url_encod)]])
#         )
#     except FloodWait as w:
#         print(f"Sleeping for {str(w.x)}s")
#         await asyncio.sleep(w.x)
#         await bot.send_message(chat_id=Var.BIN_CHANNEL,
#                              text=f"Gᴏᴛ FʟᴏᴏᴅWᴀɪᴛ ᴏғ {str(w.x)}s from {broadcast.chat.title}\n\n**Cʜᴀɴɴᴇʟ ID:** `{str(broadcast.chat.id)}`",
#                              disable_web_page_preview=True, parse_mode="Markdown")
#     except Exception as e:
#         await bot.send_message(chat_id=Var.BIN_CHANNEL, text=f"**#ᴇʀʀᴏʀ_ᴛʀᴀᴄᴇʙᴀᴄᴋ:** `{e}`", disable_web_page_preview=True, parse_mode="Markdown")
#         print(f"Cᴀɴ'ᴛ Eᴅɪᴛ Bʀᴏᴀᴅᴄᴀsᴛ Mᴇssᴀɢᴇ!\nEʀʀᴏʀ: {e}")
