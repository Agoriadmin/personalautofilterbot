import re
import logging
import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import ButtonDataInvalid, FloodWait

from bot.database import Database # pylint: disable=import-error
from bot.bot import Bot # pylint: disable=import-error
from bot import ADMINS

FIND = {}
INVITE_LINK = {}
ACTIVE_CHATS = {}
db = Database()

@Bot.on_message(filters.text & filters.group & ~filters.bot, group=0)
async def auto_filter(bot, update):
    """
    A Funtion To Handle Incoming Text And Reply With Appropriate Results
    """
    KEY_WORD = update.text
    G_SEARCH = re.sub(r' ', '+', f'{KEY_WORD}')
    group_id = update.chat.id

    query = update.text

    if re.findall(r"((^\/|^,|^\.|^[\U0001F600-\U000E007F]).*)", update.text):
        return
    
    if ("https://" or "http://") in update.text:
        return
    

    if len(query) < 2:
        return
    
    results = []
    
    global ACTIVE_CHATS
    global FIND
    
    configs = await db.find_chat(group_id)
    achats = ACTIVE_CHATS[str(group_id)] if ACTIVE_CHATS.get(str(group_id)) else await db.find_active(group_id)
    ACTIVE_CHATS[str(group_id)] = achats
    
    if not configs:
        return
    
    allow_video = configs["types"]["video"]
    allow_audio = configs["types"]["audio"] 
    allow_document = configs["types"]["document"]
    
    max_pages = configs["configs"]["max_pages"] # maximum page result of a query
    pm_file_chat = configs["configs"]["pm_fchat"] # should file to be send from bot pm to user
    max_results = configs["configs"]["max_results"] # maximum total result of a query
    max_per_page = configs["configs"]["max_per_page"] # maximum buttom per page 
    show_invite = configs["configs"]["show_invite_link"] # should or not show active chat invite link
    
    show_invite = (False if pm_file_chat == True else show_invite) # turn show_invite to False if pm_file_chat is True
    
    filters = await db.get_filters(group_id, query)
    
    if filters:
        results.append(
                [
                    InlineKeyboardButton(" ▶️Join Our Channel📽️", url="https://t.me/Agorimovies")
                ]
            )
        for filter in filters: # iterating through each files
            file_name = filter.get("file_name")
            file_type = filter.get("file_type")
            file_link = filter.get("file_link")
            file_size = int(filter.get("file_size", ""))
            file_size = round((file_size/1024),2) # from B to KB
            size = ""
            file_KB = ""
            file_MB = ""
            file_GB = ""
            
            if file_size < 1024:
                file_KB = f"𝚂𝚞𝚋𝚝𝚒𝚝𝚕𝚎"
                size = file_KB
            elif file_size < (1024*1024):
                file_MB = f"📂 {str(round((file_size/1024),2))} 𝙼ʙ"
                size = file_MB
            else:
                file_GB = f"📂 {str(round((file_size/(1024*1024)),2))} 𝙶ʙ"
                size = file_GB
                
            file_names = file_name
            file_size = size
            print(file_name)

            
            if file_type == "video":
                if allow_video: 
                    pass
                else:
                    continue
                
            elif file_type == "audio":
                if allow_audio:
                    pass
                else:
                    continue
                
            elif file_type == "document":
                if allow_document:
                    pass
                else:
                    continue
            
            if len(results) >= max_results:
                break
            
            if pm_file_chat: 
                unique_id = filter.get("unique_id")
                if not FIND.get("bot_details"):
                    try:
                        bot_= await bot.get_me()
                        FIND["bot_details"] = bot_
                    except FloodWait as e:
                        asyncio.sleep(e.x)
                        bot_= await bot.get_me()
                        FIND["bot_details"] = bot_
                
                bot_ = FIND.get("bot_details")
                file_link = f"https://t.me/{bot_.username}?start={unique_id}"
    
            results.append([
            InlineKeyboardButton(file_names, url=file_link),
            InlineKeyboardButton(file_size, url=file_link)
        ])
        
    else:
        if update.from_user.id not in ADMINS:
            send_msg = await bot.send_message(
            chat_id = update.chat.id,
            text=f"𝙋𝙡𝙚𝙖𝙨𝙚 𝘾𝙝𝙚𝙘𝙠 𝘼𝙣𝙙 𝙘𝙤𝙥𝙮 𝙤𝙣𝙡𝙮 𝙢𝙤𝙫𝙞𝙚 𝙣𝙖𝙢𝙚 𝙛𝙧𝙤𝙢 𝙙𝙤𝙬𝙣 𝙗𝙪𝙩𝙩𝙤𝙣𝙨 𝙖𝙣𝙙 𝙨𝙚𝙣𝙙 𝙙𝙞𝙧𝙚𝙘𝙩𝙡𝙮 𝙝𝙚𝙧𝙚",
            reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🔍ᴄʜᴇᴄᴋ sᴘᴇʟʟɪɴɢ ʜᴇʀᴇ", url=f'http://google.com/search?q={G_SEARCH}')
                ]
            ]
         ),
            parse_mode="html",
            reply_to_message_id=update.message_id
         ) 
            await asyncio.sleep(20)
            await send_msg.delete()
            
    if len(results) == 0: # double check
        return
    
    else:
    
        result = []
        # seperating total files into chunks to make as seperate pages
        result += [results[i * max_per_page :(i + 1) * max_per_page ] for i in range((len(results) + max_per_page - 1) // max_per_page )]
        len_result = len(result)
        len_results = len(results)
        results = None # Free Up Memory
        
        FIND[query] = {"results": result, "total_len": len_results, "max_pages": max_pages} # TrojanzHex's Idea Of Dicts😅

        # Add next buttin if page count is not equal to 1
        if len_result != 1:
            result[0].append(
                [
                    InlineKeyboardButton("𝐍𝐞𝐱𝐭 ▶️", callback_data=f"navigate(0|next|{query})")
                ]
            )
        # Just A Decaration
        result[0].append([
            InlineKeyboardButton(f"🎥𝐏𝐚𝐠𝐞 1/{len_result if len_result < max_pages else max_pages} 🔰", callback_data="ignore")
        ])
        
        
        # if show_invite is True Append invite link buttons
        if show_invite:
            
            ibuttons = []
            achatId = []
            await gen_invite_links(configs, group_id, bot, update)
            
            for x in achats["chats"] if isinstance(achats, dict) else achats:
                achatId.append(int(x["chat_id"])) if isinstance(x, dict) else achatId.append(x)

            ACTIVE_CHATS[str(group_id)] = achatId
            
            for y in INVITE_LINK.get(str(group_id)):
                
                chat_id = int(y["chat_id"])
                
                if chat_id not in achatId:
                    continue
                
                chat_name = y["chat_name"]
                invite_link = y["invite_link"]
                
                if ((len(ibuttons)%2) == 0):
                    ibuttons.append(
                        [
                            InlineKeyboardButton(f"⚜ {chat_name} ⚜", url=invite_link)
                        ]
                    )

                else:
                    ibuttons[-1].append(
                        InlineKeyboardButton(f"⚜ {chat_name} ⚜", url=invite_link)
                    )
                
            for x in ibuttons:
                result[0].insert(0, x) #Insert invite link buttons at first of page
                
            ibuttons = None # Free Up Memory...
            achatId = None
            
            
        reply_markup = InlineKeyboardMarkup(result[0])

        try:
            await bot.send_message(
                chat_id = update.chat.id,
                text=f"𝐆𝐫𝐨𝐮𝐩:- <b>@agorihome</b> \n𝐑𝐞𝐪𝐮𝐞𝐬𝐭𝐞𝐝 𝐌𝐨𝐯𝐢𝐞:- <code>{query}</code> \n𝐑𝐞𝐬𝐮𝐥𝐭𝐬 𝐅𝐨𝐮𝐧𝐝:- {(len_results)} \n𝐑𝐞𝐪𝐮𝐞𝐬𝐭𝐞𝐝 𝐁𝐲:- <b>{update.from_user.first_name}</b> \n \n <b><a href='https://t.me/joinchat/SsHwKcAPDY8xOTRl'>𝙅𝙤𝙞𝙣 𝙏𝙝𝙞𝙨 𝘾𝙝𝙖𝙣𝙣𝙚𝙡 𝘼𝙣𝙙 𝗣𝗿𝗲𝘀𝘀 𝗧𝗵𝗲 𝗗𝗼𝘄𝗻 𝗕𝘂𝘁𝘁𝗼𝗻𝘀 𝗧𝗼 𝗔𝗰𝗰𝗲𝘀𝘀 𝗧𝗵𝗲 𝗙𝗶𝗹𝗲</a> \n \n<b><a href='https://t.me/joinchat/SsHwKcAPDY8xOTRl'>പടം ലഭിക്കുന്നതിനായി ഇവിടെ ക്ലിക്ക് ചെയ്താൽ കിട്ടുന്ന ചാനലിൽ ജോയിൻ ആയ ശേഷം താഴെ കാണുന്ന ബട്ടണുകളിൽ ക്ലിക്ക് ചെയ്യുക👇</a></b>",
                reply_markup=reply_markup,
                parse_mode="html",
                reply_to_message_id= (update.message_id) if (update.reply_to_message == None) else (update.reply_to_message.message_id)
            )

        except ButtonDataInvalid:
            print(result[0])
        
        except Exception as e:
            print(e)


async def gen_invite_links(db, group_id, bot, update):
    """
    A Funtion To Generate Invite Links For All Active 
    Connected Chats In A Group
    """
    chats = db.get("chat_ids")
    global INVITE_LINK
    
    if INVITE_LINK.get(str(group_id)):
        return
    
    Links = []
    if chats:
        for x in chats:
            Name = x["chat_name"]
            
            if Name == None:
                continue
            
            chatId=int(x["chat_id"])
            
            Link = await bot.export_chat_invite_link(chatId)
            Links.append({"chat_id": chatId, "chat_name": Name, "invite_link": Link})

        INVITE_LINK[str(group_id)] = Links
    return 


async def recacher(group_id, ReCacheInvite=True, ReCacheActive=False, bot=Bot, update=Message):
    """
    A Funtion To rechase invite links and active chats of a specific chat
    """
    global INVITE_LINK, ACTIVE_CHATS

    if ReCacheInvite:
        if INVITE_LINK.get(str(group_id)):
            INVITE_LINK.pop(str(group_id))
        
        Links = []
        chats = await db.find_chat(group_id)
        chats = chats["chat_ids"]
        
        if chats:
            for x in chats:
                Name = x["chat_name"]
                chat_id = x["chat_id"]
                if (Name == None or chat_id == None):
                    continue
                
                chat_id = int(chat_id)
                
                Link = await bot.export_chat_invite_link(chat_id)
                Links.append({"chat_id": chat_id, "chat_name": Name, "invite_link": Link})

            INVITE_LINK[str(group_id)] = Links
    
    if ReCacheActive:
        
        if ACTIVE_CHATS.get(str(group_id)):
            ACTIVE_CHATS.pop(str(group_id))
        
        achats = await db.find_active(group_id)
        achatId = []
        if achats:
            for x in achats["chats"]:
                achatId.append(int(x["chat_id"]))
            
            ACTIVE_CHATS[str(group_id)] = achatId
    return 

