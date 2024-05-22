from WebStreamer.utils.database import Database
from WebStreamer.bot import StreamBot
from WebStreamer.vars import Var
from datetime import datetime
from pyrogram import filters, Client
from pyrogram.enums import ParseMode
from pyrogram.types import Message
db = Database()


@StreamBot.on_message(filters.command("userinfo") & filters.private & filters.user(Var.OWNER_ID))
async def sts(c: Client, m: Message):
    user_info = db.info(m.text.split(" ")[1])
    try:
        await m.reply_text(text="**user info :**\nuser id : {}\nstatus : {}\nexpire stamp : {}\ndaily usage : {}".format(user_info['from_id'], user_info['accountType'], str(datetime.fromtimestamp(int(user_info['expireStamp'])) - datetime.now()).split(" day")[0] if len(str(datetime.fromtimestamp(int(user_info['expireStamp'])) - datetime.now()).split(" day")) == 2 else '0', user_info['dailyUsage']+' GB'), parse_mode=ParseMode.MARKDOWN, quote=True)

    except ValueError:
        await m.reply_text(text="**user info :**\nuser id : {}\nstatus : {}\nexpire stamp : {}\ndaily usage : {}".format(user_info['from_id'], 'Free', 'Unlimited', user_info['dailyUsage']+' GB'), parse_mode=ParseMode.MARKDOWN, quote=True)
