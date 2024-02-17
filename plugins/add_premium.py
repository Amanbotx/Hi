import pytz
import os
import asyncio
from datetime import time, datetime, timedelta
from info import *
from Script import script
from utils import get_seconds
from database.users_chats_db import db
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong
from pyrogram.errors import FloodWait

@Client.on_message(filters.command("remove_premium") & filters.user(ADMINS))
async def remove_premium(client, message):
    if len(message.command) == 2:
        user_id = int(message.command[1])
        user = await client.get_users(user_id)
        if await db.has_premium_access(user_id):
            await db.remove_premium_access(user_id)
            await message.reply_text(f"<b>Sᴜᴄᴄᴇssꜰᴜʟʟy Rᴇᴍᴏᴠᴇᴅ {user.mention}'s Pʀᴇᴍɪᴜᴍ Sᴜʙꜱᴄʀɪᴘᴛɪᴏɴ ❗</b>")
            try:
                await client.send_message(chat_id=user_id, text=f"<b>आपका प्रीमियम प्लान खतम हो गया है ‼️\n\nअगर आपको वापस प्रीमियम Buy करना है तो \n/premium पर क्लिक करके प्लान वापस Buy कर ले...‼️\n\nTʜᴀɴᴋꜱ Fᴏʀ Uꜱɪɴɢ Oᴜʀ Sᴇʀᴠɪᴄᴇ...❤️</b>")
            except:
                pass
        else:
            await message.reply_text(f"<b>who is this {user.mention} ❓</b>")
    else:
        await message.reply_text("<b>Cᴏᴍᴍᴀɴᴅ Iɴᴄᴏᴍᴘʟᴇᴛᴇ...</b>")

@Client.on_message(filters.private & filters.command("myplan"))
async def myplan(client, message):
    user = message.from_user.mention
    user_id = message.from_user.id
    data = await db.get_user(message.from_user.id)
    if data and data.get("expiry_time"):
        expiry = data.get("expiry_time") 
        expiry_ist = expiry.astimezone(pytz.timezone(TIMEZONE))
        expiry_str_in_ist = expiry.astimezone(pytz.timezone(TIMEZONE)).strftime("%d-%m-%Y %I:%M:%S %p")            

        current_time = datetime.now(pytz.timezone(TIMEZONE))
        time_left = expiry_ist - current_time

        days = time_left.days
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        time_left_str = f"{days} days, {hours} hours, {minutes} minutes"
        await message.reply_text(f"<b>⚡ ᴄᴜʀʀᴇɴᴛ ᴘʟᴀɴ ᴅᴇᴛᴀɪʟꜱ ⚡\n\nᴛɪᴍᴇ ʟᴇꜰᴛ - {time_left_str}\nᴇxᴘɪʀᴇ ᴛɪᴍᴇ - {expiry_str_in_ist}</b>", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Uᴘɢʀᴀᴅᴇ", url="https://t.me/TheHappyHourBot?start=TheHappyHour"), InlineKeyboardButton("Cʟᴏsᴇ ❌", callback_data="close_data")]])) 
    else:
        await message.reply_text(f"<b>आपने कोई प्रीमियम प्लान Buy नई किया...😒\n\nप्रीमियम प्लान Buy करने के \nलिऐ /premium पर क्लिक करें ‼️</b>")

@Client.on_message(filters.command("add_premium") & filters.user(ADMINS))
async def give_premium_cmd_handler(client, message):
    if len(message.command) == 4:
        time_zone = datetime.now(pytz.timezone(TIMEZONE))
        current_time = time_zone.strftime("%d-%m-%Y %I:%M:%S %p") 
        user_id = int(message.command[1])
        user = await client.get_users(user_id)
        time = message.command[2]+" "+message.command[3]
        seconds = await get_seconds(time)
        if seconds > 0:
            expiry_time = datetime.now() + timedelta(seconds=seconds)
            user_data = {"id": user_id, "expiry_time": expiry_time}
            await db.update_user(user_data)
            data = await db.get_user(user_id)
            expiry = data.get("expiry_time")
            expiry_str_in_ist = expiry.astimezone(pytz.timezone(TIMEZONE)).strftime("%d-%m-%Y %I:%M:%S %p")         
            await message.reply_text(f"<b>ᴘʀᴇᴍɪᴜᴍ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴀᴅᴅᴇᴅ ✅\n\nᴜꜱᴇʀ - {user.mention}\nʙᴜʏɪɴɢ ᴛɪᴍᴇ - {current_time}\nᴠᴀʟᴀᴅɪᴛʏ - {time}\nᴇxᴘɪʀᴇ ᴛɪᴍᴇ - {expiry_str_in_ist}\n\nᴘʀᴏᴄᴇꜱꜱɪɴɢ ᴄᴏᴍᴘʟᴇᴛᴇ 🎉</b>", disable_web_page_preview=True)
            try:
                await client.send_message(chat_id=user_id, text=f"<b>🎉 cᴏɴɢʀᴀᴛᴜʟᴀᴛɪᴏɴꜱ 🥳\n\nआपको प्रीमियम लिस्ट में ᴀᴅᴅ किया गया है...✅\nअब आप सभी प्रीमियम फ्यूचर का उपयोग कर सकते है...🎉\n\nʙᴜʏɪɴɢ ᴛɪᴍᴇ - {current_time}\nᴠᴀʟᴀᴅɪᴛʏ - {time}\nᴇxᴘɪʀᴇ ᴛɪᴍᴇ - {expiry_str_in_ist}</b>", disable_web_page_preview=True) 
            except:
                pass
            await client.send_message(PREMIUM_LOGS, text=f"<b>ᴘʀᴇᴍɪᴜᴍ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴀᴅᴅᴇᴅ ✅\n\nᴜꜱᴇʀ - {user.mention}\nʙᴜʏɪɴɢ ᴛɪᴍᴇ - {current_time}\nᴠᴀʟᴀᴅɪᴛʏ - {time}\nᴇxᴘɪʀᴇ ᴛɪᴍᴇ - {expiry_str_in_ist}\n\nᴘʀᴏᴄᴇꜱꜱɪɴɢ ᴄᴏᴍᴘʟᴇᴛᴇ 🎉</b>", disable_web_page_preview=True)                
        else:
            await message.reply_text("<i>Iɴᴠᴀʟɪᴅ Tɪᴍᴇ Fᴏʀᴍᴀᴛ...</i>\n\n1 day\n1 hour\n1 min\n1 month\n1 year")
    else:
        await message.reply_text("<b>Cᴏᴍᴍᴀɴᴅ Iɴᴄᴏᴍᴘʟᴇᴛᴇ...</b>")

@Client.on_message(filters.private & filters.command("futures"))
async def allplans(bot, message):
    btn = [[
            InlineKeyboardButton('🎁 ᴄʜᴇᴄᴋ ᴘʟᴀɴs 🎁', callback_data='check'), 
        ],[
            InlineKeyboardButton('ʜᴏᴡ ɪᴛs ᴡᴏʀᴋ', url="https://graph.org/The-Happy-Hour-12-22-2"),
            InlineKeyboardButton('cʟᴏꜱᴇ', callback_data='close_data')
        ]]
    await message.reply_photo(
        photo="https://graph.org/file/322b2512f1ceaf9094abb.jpg",
        caption="<b>🔥 Pʀᴇᴍɪᴜᴍ Uꜱᴇʀ Fᴜᴛᴜʀᴇ 🔥\n\n☞ आप प्रीमियम user हैं तो आपको वेरीफिकेशन नई करना पड़ेगा ।\n☞ डायरेक्ट मूवी का फाइल ही मिलेगा ।\n☞ आपको फास्ट डाउनलोड लिंक & ऑनलाइन स्ट्रीम कि लिंक भी use सकते हे ।\n☞ बहुत सारे प्लेयर में ओनलाइन मूवी देख सकते है ।\n☞ आप अनलिमिटेड मूवी ले सकतें है।\n☞ कोई प्रकार का AD शो नई होगा।\n☞ एडमिन की तरफ से पूरा सपोर्ट मिलेगा ।\n☞ अगर कोई प्रॉबलम आता है तो ऐडमिन उसे जल्द ही सॉल्व कर देगे ।\n\n🔥 Pʀᴇᴍɪᴜᴍ Uꜱᴇʀ Fᴜᴛᴜʀᴇ 🔥\n\n○ ɴᴏ ɴᴇᴇᴅ ᴛᴏ ᴠᴇʀɪғʏ\n○ ᴅɪʀᴇᴄᴛ ғɪʟᴇs\n○ ᴀᴅ-ғʀᴇᴇ ᴇxᴘᴇʀɪᴇɴᴄᴇ\n○ ʜɪɢʜ-sᴘᴇᴇᴅ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ\n○ ᴍᴜʟᴛɪ-ᴘʟᴀʏᴇʀ sᴛʀᴇᴀᴍɪɴɢ ʟɪɴᴋs\n○ ᴜɴʟɪᴍɪᴛᴇᴅ ᴍᴏᴠɪᴇs & sᴇʀɪᴇs\n○ ꜰᴜʟʟ ᴀᴅᴍɪɴ sᴜᴘᴘᴏʀᴛ\n○ ʀᴇǫᴜᴇsᴛ ᴡɪʟʟ ʙᴇ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ɪɴ 1ʜ ɪꜰ ᴀᴠᴀɪʟᴀʙʟᴇ\n\n--> Cʀᴇᴀᴛᴇᴅ Bʏ Tʜᴇ Hᴀᴘᴘʏ Hᴏᴜʀ</b>",
        reply_markup=InlineKeyboardMarkup(btn)
    )

@Client.on_message(filters.private & filters.command("premium"))
async def allplan(bot, message):
    btn = [[
            InlineKeyboardButton('📸 sᴇɴᴅ sᴄʀᴇᴇɴsʜᴏᴛ 📸', url="https://t.me/Master_Jiraya_Bot")
        ],[
            InlineKeyboardButton('☘️ ꜰᴜᴛᴜʀᴇ ☘️', url="https://graph.org/The-Happy-Hour-12-22-2"),
            InlineKeyboardButton('cʟᴏꜱᴇ', callback_data='close_data')
        ]]
    await message.reply_photo(
        photo="https://graph.org/file/37ffdc19a9c1459b9d6e2.jpg",
        caption="""<b>
        <a href='https://graph.org/The-Happy-Hour-12-22-2'>💥 ᴘʀᴇᴍɪᴜᴍ ᴘʀɪᴄᴇ 💥
        
1 Wᴇᴇᴋ = [50 + 0] Rs
1 Mᴏɴᴛʜ = [50 + 10] Rs
2 Mᴏɴᴛʜ = [50 + 30] Rs
3 Mᴏɴᴛʜ = [50 + 50] Rs
6 Mᴏɴᴛʜ = [50 + 100] Rs
1 Yᴇᴀʀ = [50 + 150] Rs

⚡ᴄʜᴀᴄᴋ ᴘʀᴇᴍɪᴜᴍ ꜰᴜᴛᴜʀᴇꜱ⚡
ㅤㅤㅤㅤㅤ</a></b>""",
        reply_markup=InlineKeyboardMarkup(btn)
    )