#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @AlbertEinsteinTG & NO-ONE-KN0WS-ME & MRRONS

from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import UserNotParticipant
from bot import Translation # pylint: disable=import-error
from bot.database import Database # pylint: disable=import-error

db = Database()

@Client.on_message(filters.command(["start"]) & filters.private, group=1)
async def start(bot, update):
    update_channel = "@agorihome"
    if update_channel:
        try:
            user = await bot.get_chat_member(update_channel, update.chat.id)
            if user.status == "kicked out":
               await update.reply_text("🤭 Sorry Dude, You are B A N N E D 🤣🤣🤣")
               return
        except UserNotParticipant:
            #await update.reply_text(f"Join @{update_channel} To Use Me")
            await update.reply_text(
                text="<b>🤭 𝗝𝗼𝗶𝗻 𝗢𝘂𝗿 𝗠𝗮𝗶𝗻 𝗰𝗵𝗮𝗻𝗻𝗲𝗹 🤭\n\nനിങ്ങൾക് സിനിമകൾ വേണോ? അതിനായി ആദ്യം നിങ്ങൾ ചെയ്യേണ്ടത് ഞങ്ങളുടെ മെയിൻ ചാനലിൽ ജോയിൻ ആവുക എന്നതാണ്🤭... 😁\n\nJoin ചെയതത്തിനു ശേഷം വീണ്ടും ബോട്ട് /start ആക്കൂ AND FEEL THE MAGIC.😁</b>",
                reply_markup=InlineKeyboardMarkup([
                    [ InlineKeyboardButton(text=" 🤭JOIN OUR CHANNEL🤭 ", url=f"https://t.me/agorihome")]
              ])
            )
            return
        except Exception:
            await update.reply_text("Something Wrong. Contact my Support Group")
            return
    
    try:
        file_uid = update.command[1]
    except IndexError:
        file_uid = False
    
    if file_uid:
        file_id, file_name, file_caption, file_type = await db.get_file(file_uid)
        
        if (file_id or file_type) == None:
            return
        
        caption = file_caption if file_caption != ("" or None) else ("<code>" + file_name + "</code>")
        
        if file_type == "document":
        
            await bot.send_document(
                chat_id=update.chat.id,
                document = file_id,
                caption ="❤️ 𝚃𝚑𝚊𝚗𝚔𝚢𝚘𝚞 𝙵𝚘𝚛 𝚄𝚜𝚒𝚗𝚐 𝙾𝚞𝚛 𝚂𝚎𝚛𝚟𝚒𝚌𝚎 𝙿𝚕𝚎𝚊𝚜𝚎 𝚂𝚞𝚙𝚙𝚘𝚛𝚝 𝚄𝚜 𝙱𝚢 𝚂𝚑𝚊𝚛𝚒𝚗𝚐 𝙾𝚞𝚛 𝙲𝚑𝚊𝚗𝚗𝚎𝚕/𝙶𝚛𝚘𝚞𝚙 𝙻𝚒𝚗𝚔 𝚃𝚘 𝚈𝚘𝚞𝚛 𝙵𝚛𝚒𝚎𝚗𝚍𝚜 \n\n❁𝕁𝕠𝕚𝕟 𝕆𝕦𝕣 ℂ𝕙𝕒𝕟𝕟𝕖𝕝𝕤❁  \n\n⟱⟱⟱⟱⟱⟱⟱⟱⟱⟱⟱⟱  \n\n📌𝕮𝖍𝖆𝖓𝖓𝖊𝖑: @agorihome➻ \n📌𝕮𝖍𝖆𝖓𝖓𝖊𝖑 : @agoriseries➻ \n👥𝕲𝖗𝖔𝖚𝖕 : @agorimovies➻ \n👥𝕲𝖗𝖔𝖚𝖕 : @mv_mania",
                parse_mode="html",
                reply_to_message_id=update.message_id,
                reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('𝑺𝑯𝑨𝑹𝑬🌐', url="https://t.me/share/url?url=https%3A//t.me/share/url%3Furl%3Dhttps%253A//t.me/agorimovies")
                ],
                [
                    InlineKeyboardButton('💣𝐌𝐎𝐕𝐈𝐄 𝐑𝐄𝐐💣', url="https://t.me/agorimovies"),
                    InlineKeyboardButton('🔥𝐖𝐄𝐁𝐒𝐄𝐑𝐈𝐄S🔥', url="https://t.me/agoriseries")
                ],
                [
                    InlineKeyboardButton('⚠️𝐆𝐑𝐎𝐔𝐏⚠️', url="https://t.me/Agorimovies"),
                    InlineKeyboardButton('💢𝐀𝐍𝐈𝐌𝐄💢', url="https://t.me/agkidsroom")
                ]
            ]
        )
    )

        elif file_type == "video":
        
            await bot.send_video(
                chat_id=update.chat.id,
                video = file_id,
                caption = caption,
                parse_mode="html",
                reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('𝑺𝑯𝑨𝑹𝑬🌐', url="https://t.me/share/url?url=https%3A//t.me/share/url%3Furl%3Dhttps%253A//t.me/agorimovies")
                ],
                [
                    InlineKeyboardButton('💥𝐌𝐎𝐕𝐈𝐄 𝐑𝐄𝐐💥', url="https://t.me/agorimovies"),
                    InlineKeyboardButton('♻️𝐖𝐄𝐁𝐒𝐄𝐑𝐈𝐄𝐒♻️', url="https://t.me/agoriseries")
                ],
                [
                    InlineKeyboardButton('🔱𝐆𝐑𝐎𝐔𝐏🔱', url="https://t.me/agorimovies"),
                    InlineKeyboardButton('♻️𝐀𝐍𝐈𝐌𝐄♻️', url="https://t.me/agkidsroom")
                ]
            ]
        )
    )
            
        elif file_type == "audio":
        
            await bot.send_audio(
                chat_id=update.chat.id,
                audio = file_id,
                caption = caption,
                parse_mode="html",
                reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('𝑺𝑯𝑨𝑹𝑬 🌐', url="https://t.me/share/url?url=https%3A//t.me/share/url%3Furl%3Dhttps%253A//t.me/agorimovies")
                ],
                [
                    InlineKeyboardButton('💥𝐌𝐎𝐕𝐈𝐄 𝐑𝐄𝐐💥', url="https://t.me/filmcityhd1"),
                    InlineKeyboardButton('♻️𝐖𝐄𝐁𝐒𝐄𝐑𝐈𝐄𝐒♻️', url="https://t.me/fchweb")
                ],
                [
                    InlineKeyboardButton('🔱𝐆𝐑𝐎𝐔𝐏🔱', url="https://t.me/fchchatgroup"),
                    InlineKeyboardButton('♻️𝐀𝐍𝐈𝐌𝐄♻️', url="https://t.me/fchanime")
                ]
            ]
        )
    )

        else:
            print(file_type)
        
        return

    await bot.send_photo(
        chat_id=update.chat.id,
        photo = 'https://telegra.ph/file/dc6db71cfea54e0e0565c.jpg',
        caption=Translation.START_TEXT.format(
                update.from_user.first_name),
        reply_markup=InlineKeyboardMarkup(
            [
                
                [
                    InlineKeyboardButton('💣𝐌𝐎𝐕𝐈𝐄 𝐑𝐄𝐐💣', url='https://t.me/agorimovies'),
                    InlineKeyboardButton('💫𝐖𝐄𝐁𝐒𝐄𝐑𝐈𝐄𝐒💫', url ='https://t.me/agoriseries')
                ],
                [
                    InlineKeyboardButton('🚸𝐀𝐍𝐈𝐌𝐄🚸', url='https://t.me/agkidsroom'),
                    InlineKeyboardButton('♻️𝐆𝐑𝐎𝐔𝐏♻️', url='https://t.me/agorimovies')
                ]
            ]
        ), 
        parse_mode="html", 
        reply_to_message_id=update.message_id
    )


@Mai_bOTs.on_message(filters.command(["help"]) & filters.private, group=1)
async def help(bot, update):
    buttons = [[
        InlineKeyboardButton('Close 🔐', callback_data='close')
    ]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.HELP_TEXT,
        reply_markup=reply_markup,
        parse_mode="html",
        reply_to_message_id=update.message_id
    )


@Mai_bOTs.on_message(filters.command(["about"]) & filters.private, group=1)
async def about(bot, update):
    
    buttons = [[
        InlineKeyboardButton('Close 🔐', callback_data='close')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.ABOUT_TEXT,
        reply_markup=reply_markup,
        disable_web_page_preview=True,
        parse_mode="html",
        reply_to_message_id=update.message_id
    )

@Mai_bOTs.on_message(filters.text & ~ filters.command(["start", "help"]) & filters.private & ~ filters.me)
async def note(bot, update):
    buttons = [[
        InlinekeyboardButton('MOVIE REQUEST 💣', url='https://t.me/agorimovies')
    ],[
        InlineKeyboardButton('🏡 WEBSERIES CHANNEL💢', url='https://t.me/agoriseries'),
        InlineKeyboardButton('📽️ ANIME CHANNEL', url ='https://t.me/agkidsroom')
    ],[
        InlineKeyboardButton('🤔𝙷𝙾𝚆 𝚃𝙾 𝚁𝙴𝚀?', url='https://t.me/c/1387634315/4')
    ],[
        InlineKeyboardButton('𝚂𝙷𝙰𝚁𝙴 𝚃𝙾 𝚈𝙾𝚄𝚁 𝙵𝚁𝙸𝙴𝙽𝙳𝚂😍', url='https://t.me/share/url?url=https%3A//t.me/share/url%3Furl%3Dhttps%253A//t.me/agorimovies')
    ]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await bot.send_message(
        chat_id=update.chat.id,
        text="എന്നെ ഉപയോഗിക്കുന്നതിനു നന്ദി😊.നിങ്ങൾക്ക് വേണ്ട പടങ്ങൾ @agorimovies എന്ന ഗ്രൂപ്പിൽ ചോദിച്ചാൽ മാത്രമേ കിട്ടുകയുള്ളൂ.\nഇവിടെ ചോദിച്ചു സമയം കളയണ്ട!🚶\n\nThank you for using me ❤️\nPlease Don't Req For Movies Here.\nJoin Our @filmcityhd1 Group And Req Your Movies There...🚶 ",
        reply_markup=reply_markup,
        parse_mode="html",
        reply_to_message_id=update.message_id
    )
