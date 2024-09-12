import asyncio
import os
import random
import sys
import time
import string
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot
from config import ADMINS, CHANNEL_ID, FORCE_MSG, FORCE_SUB_CHANNEL, FORCE_SUB_CHANNEL2, OWNER_TAG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT, OWNER_ID, SHORTLINK_URL, SHORTLINK_API, USE_PAYMENT, USE_SHORTLINK, VERIFY_EXPIRE, TIME, TUT_VID, U_S_E_P, REQUEST1, REQUEST2, PHOTO_URL, LOG_CHANNEL
from helper_func import encode, get_readable_time, increasepremtime, subscribed, subscribed2, decode, get_messages, get_shortlink, get_verify_status, update_verify_status, get_exp_time
from database.database import add_admin, add_user, del_admin, del_user, full_adminbase, full_userbase, gen_new_count, get_clicks, inc_count, new_link, present_admin, present_hash, present_user

WAIT_MSG = """"<b>Processing ...</b>"""
REPLY_ERROR = """<blockquote><b>Use this command as a reply to any telegram message without any spaces.</b></blockquote>"""
SECONDS = TIME 
TUT_VID = f"{TUT_VID}"


@Bot.on_message(filters.command('start') & filters.private & subscribed & subscribed2)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    if not await present_user(id):
        try:
            await add_user(id)
        except:
            pass
    verify_status = await get_verify_status(id)
    if USE_SHORTLINK and (not U_S_E_P):
        for i in range(1):
            if id in ADMINS:
                continue
            if verify_status['is_verified'] and VERIFY_EXPIRE < (time.time() - verify_status['verified_time']):
                await update_verify_status(id, is_verified=False)
            if "verify_" in message.text:
                _, token = message.text.split("_", 1)
                if verify_status['verify_token'] != token:
                    return await message.reply("<blockquote><b>🔴 Your token verification is invalid or Expired, Hit /start command and try again.<b></blockquote>")
                await update_verify_status(id, is_verified=True, verified_time=time.time())
                if verify_status["link"] == "":
                    reply_markup = None
                await message.reply(f"<blockquote><b>Your token verification was successful\n\nNow you can access all files for 24-hrs...</b></blockquote>", reply_markup=reply_markup, protect_content=False, quote=True)
    if len(message.text) > 7:
        for i in range(1):
            if USE_SHORTLINK and (not U_S_E_P):
                if USE_SHORTLINK: 
                    if id not in ADMINS:
                        try:
                            if not verify_status['is_verified']:
                                continue
                        except:
                            continue
            try:
                base64_string = message.text.split(" ", 1)[1]
            except:
                return
            _string = await decode(base64_string)
            argument = _string.split("-")
            if (len(argument) == 5 )or (len(argument) == 4):
                if not await present_hash(base64_string):
                    try:
                        await gen_new_count(base64_string)
                    except:
                        pass
                await inc_count(base64_string)
                if len(argument) == 5:
                    try:
                        start = int(int(argument[3]) / abs(client.db_channel.id))
                        end = int(int(argument[4]) / abs(client.db_channel.id))
                    except:
                        return
                    if start <= end:
                        ids = range(start, end+1)
                    else:
                        ids = []
                        i = start
                        while True:
                            ids.append(i)
                            i -= 1
                            if i < end:
                                break
                elif len(argument) == 4:
                    try:
                        ids = [int(int(argument[3]) / abs(client.db_channel.id))]
                    except:
                        return
                temp_msg = await message.reply("Please wait... 🫷")
                try:
                    messages = await get_messages(client, ids)
                except:
                    await message.reply_text("Something went wrong..! 🥲")
                    return
                await temp_msg.delete()
                snt_msgs = []
                for msg in messages:
                    if bool(CUSTOM_CAPTION) & bool(msg.document):
                        caption = CUSTOM_CAPTION.format(previouscaption="" if not msg.caption else msg.caption.html,    filename=msg.document.file_name)
                    else:   
                        caption = "" if not msg.caption else msg.caption.html   
                    reply_markup = None 
                    try:    
                        snt_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML,  reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                        await asyncio.sleep(0.5)    
                        snt_msgs.append(snt_msg)    
                    except FloodWait as e:  
                        await asyncio.sleep(e.x)    
                        snt_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode= ParseMode.HTML,  reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                        snt_msgs.append(snt_msg)    
                    except: 
                        pass
                if (SECONDS == 0):
                    return
                notification_msg = await message.reply(f"<blockquote><b><blockquote><b>🔴 This file will be  deleted in {get_exp_time(SECONDS)}. Please save or forward it to your saved messages before it gets deleted.</b></blockquote>.")
                await asyncio.sleep(SECONDS)    
                for snt_msg in snt_msgs:    
                    try:    
                        await snt_msg.delete()  
                    except: 
                        pass    
                await notification_msg.edit(f"<blockquote><b>Your file has been successfully deleted! 😼</b></blockquote>")  
                return
            if (U_S_E_P):
                if verify_status['is_verified'] and VERIFY_EXPIRE < (time.time() - verify_status['verified_time']):
                    await update_verify_status(id, is_verified=False)

            if (not U_S_E_P) or (id in ADMINS) or (verify_status['is_verified']):
                if len(argument) == 3:
                    try:
                        start = int(int(argument[1]) / abs(client.db_channel.id))
                        end = int(int(argument[2]) / abs(client.db_channel.id))
                    except:
                        return
                    if start <= end:
                        ids = range(start, end+1)
                    else:
                        ids = []
                        i = start
                        while True:
                            ids.append(i)
                            i -= 1
                            if i < end:
                                break
                elif len(argument) == 2:
                    try:
                        ids = [int(int(argument[1]) / abs(client.db_channel.id))]
                    except:
                        return
                temp_msg = await message.reply("Please wait... 🫷")
                try:
                    messages = await get_messages(client, ids)
                except:
                    await message.reply_text("Something went wrong..! 🥲")
                    return
                await temp_msg.delete()
                snt_msgs = []
                for msg in messages:
                    if bool(CUSTOM_CAPTION) & bool(msg.document):
                        caption = CUSTOM_CAPTION.format(previouscaption="" if not msg.caption else msg.caption.html, filename=msg.document.file_name)
                    else:   
                        caption = "" if not msg.caption else msg.caption.html   
                    reply_markup = None 
                    try:    
                        snt_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML,  reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                        await asyncio.sleep(0.5)    
                        snt_msgs.append(snt_msg)    
                    except FloodWait as e:  
                        await asyncio.sleep(e.x)    
                        snt_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode= ParseMode.HTML,  reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                        snt_msgs.append(snt_msg)    
                    except: 
                        pass    
            try:
                if snt_msgs:
                    if (SECONDS == 0):
                        return
                    notification_msg = await message.reply(f"<blockquote><b>🔴 This file will be  deleted in  {get_exp_time(SECONDS)}. Please save or forward it to your saved messages before it gets deleted.</b></blockquote>")
                    await asyncio.sleep(SECONDS)    
                    for snt_msg in snt_msgs:    
                        try:    
                            await snt_msg.delete()  
                        except: 
                            pass    
                    await notification_msg.edit("<blockquote><b>Your file has been successfully deleted! 😼</b></blockquote>")  
                    return
            except:
                    newbase64_string = await encode(f"sav-ory-{_string}")
                    if not await present_hash(newbase64_string):
                        try:
                            await gen_new_count(newbase64_string)
                        except:
                            pass
                    clicks = await get_clicks(newbase64_string)
                    newLink = f"https://t.me/{client.username}?start={newbase64_string}"
                    link = await get_shortlink(SHORTLINK_URL, SHORTLINK_API,f'{newLink}')            
                    
                    await client.send_message(chat_id=LOG_CHANNEL, text=f"""<b>#NEW_LINK: [{message.from_user.first_name}](tg://user?id={message.from_user.id})
User: @{message.from_user.username} • {message.from_user.id}

New Link: {newLink}</b>""")
                
                    if USE_PAYMENT:
                        btn = [
                        [InlineKeyboardButton("↪️ Get free access for 24-hrs ↩️", url=link)],
                        [InlineKeyboardButton('🦋 Tutorial', url=TUT_VID)],
                        [InlineKeyboardButton("Buy Premium plan", callback_data="buy_prem")]
                        ]
                    else:
                        btn = [
                        [InlineKeyboardButton("↪️ Get free access for 24-hrs ↩️", url=link)],
                        [InlineKeyboardButton('🦋 Tutorial', url=TUT_VID)]
                        ]
                    await message.reply_photo(photo=PHOTO_URL, caption=f"<blockquote><b>Total clicks: {clicks}. Here is your link </b></blockquote>.", reply_markup=InlineKeyboardMarkup(btn), protect_content=False, quote=True)
                    return

    for i in range(1):
        if USE_SHORTLINK and (not U_S_E_P):
            if USE_SHORTLINK : 
                if id not in ADMINS:
                    try:
                        if not verify_status['is_verified']:
                            continue
                    except:
                        continue
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("☎️ Contact Developer", callback_data="about"),
                    InlineKeyboardButton("📴 Close", callback_data="close")
                ]
            ]
        )
        await message.reply_text(
            text=START_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            quote=True
        )
        return
import *        
    if USE_SHORTLINK and (not U_S_E_P): 
        if id in ADMINS:
            return
        verify_status = await get_verify_status(id)
        if not verify_status['is_verified']:
            token = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            await update_verify_status(id, verify_token=token, link="")
            link = await get_shortlink(SHORTLINK_URL, SHORTLINK_API,f'https://t.me/{client.username}?start=verify_{token}')
            
            await client.send_message(chat_id=LOG_CHANNEL, text=f"""<b>#VERIFICATION_LINK: [{message.from_user.first_name}](tg://user?id={message.from_user.id})
User: @{message.from_user.username} • {message.from_user.id}
Verification Link: {token}
Shorten Link: {link}</b>""")
                    
            if USE_PAYMENT:
                btn = [
                [InlineKeyboardButton("↪️ Get free access for 24-hrs ↩️", url=link)],
                [InlineKeyboardButton('🦋 Tutorial', url=TUT_VID)],
                [InlineKeyboardButton("Premium Membership", callback_data="buy_prem")]
                ]
            else:
                btn = [
                [InlineKeyboardButton("↪️ Get free access for 24-hrs ↩️", url=link)],
                [InlineKeyboardButton('🦋 Tutorial', url=TUT_VID)]
                ]
            await message.reply_photo(photo=PHOTO_URL, caption=f"<blockquote><b>ℹ️ Hi @{message.from_user.username}\nYour verification is expired, click on below button and complete the verification to\n <u>Get free access for 24-hrs</u></b></blockquote>", reply_markup=InlineKeyboardMarkup(btn), protect_content=False, quote=True)
            return
    return



@app.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message):
    try:
        # Initialize buttons list
        buttons = []

        # Add buttons based on configuration
        if FORCE_SUB_CHANNEL > 0:
            if hasattr(client, 'invitelink') and client.invitelink:
                buttons.append([InlineKeyboardButton("Join", url=client.invitelink)])
        if FORCE_SUB_CHANNEL2 > 0:
            if hasattr(client, 'invitelink2') and client.invitelink2:
                buttons.append([InlineKeyboardButton("Join", url=client.invitelink2)])
        if REQUEST1 and REQUEST1 != "0":  # Check if REQUEST1 is valid
            buttons.append([InlineKeyboardButton("Join", url=REQUEST1)])
        if REQUEST2 and REQUEST2 != "0":  # Check if REQUEST2 is valid
            buttons.append([InlineKeyboardButton("Join", url=REQUEST2)])

        # Add "Try Again" button with error handling for missing command arguments
        start_param = message.command[1] if len(message.command) > 1 else ''
        buttons.append([
            InlineKeyboardButton(
                text='Try Again',
                url=f"https://t.me/{client.username}?start={start_param}"
            )
        ])

        # Send the message with inline keyboard
#        await message.reply_text(
#            text="Please join the channels below:",
#            reply_markup=InlineKeyboardMarkup(buttons)
#        )
        
        await message.reply(
            text=FORCE_MSG.format(
            first=message.from_user.first_name,
            last=message.from_user.last_name,
            username=None if not message.from_user.username else '@' + message.from_user.username,
            mention=message.from_user.mention,
            id=message.from_user.id
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True,
        disable_web_page_preview=True
    )

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        if LOG_CHANNEL:
            try:
                # Send error message to the log channel
                await client.send_message(LOG_CHANNEL, error_message)
            except Exception as log_error:
                # If sending to the log channel fails, print the error
                print(f"Failed to send error message to log channel: {str(log_error)}")
        # Optionally, print the error to console
        print(error_message)


'''
@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    if FORCE_SUB_CHANNEL & FORCE_SUB_CHANNEL2:
        buttons = [
        [
            InlineKeyboardButton("Join", url=client.invitelink),
            InlineKeyboardButton("Join", url=REQUEST1),
            InlineKeyboardButton("Join", url=client.invitelink2),
            InlineKeyboardButton("Join", url=REQUEST2),
            
        ]
    ]
    elif FORCE_SUB_CHANNEL:
        buttons = [
            [
                InlineKeyboardButton("Join", url=REQUEST1),
                InlineKeyboardButton("Join", url=client.invitelink1),
                InlineKeyboardButton("Join", url=REQUEST2),
            ]
        ]    
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text='Try Again',
                    url=f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ]
        )
    except IndexError:
        pass

    await message.reply(
        text=FORCE_MSG.format(
            first=message.from_user.first_name,
            last=message.from_user.last_name,
            username=None if not message.from_user.username else '@' + message.from_user.username,
            mention=message.from_user.mention,
            id=message.from_user.id
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True,
        disable_web_page_preview=True
    )
'''

@Bot.on_message(filters.command('ch2l') & filters.private)
async def gen_link_encoded(client: Bot, message: Message):
    try:
        hash = await client.ask(text="<blockquote><b>Enter the code here...\nHit /cancel to cancel the operation</b></blockquote>",chat_id = message.from_user.id, quote=True, timeout=60)
    except Exception as e:
        print(e)
        await hash.reply(f"😔 some error occurred {e}")
        return
    if hash.text == "/cancel":
        await hash.reply("Cancelled 😉!")
        return
    link = f"https://t.me/{client.username}?start={hash.text}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Hash Link", url=link)]])
    await hash.reply_text(f"<b>Here is your generated link\n\n{link}</b>", quote=True, reply_markup=reply_markup)
    return
        

@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot 👥")
    return

@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0

        pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time ⌚</i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1

        status = f"""<b><u>Broadcast Completed 🟢</u>
                
                Total Users: <code>{total}</code>
                Successful: <code>{successful}</code>
                Blocked Users: <code>{blocked}</code>
                Deleted Accounts: <code>{deleted}</code>
                Unsuccessful: <code>{unsuccessful}</code></b>"""

        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()
    return


@Bot.on_message(filters.command('add_admin') & filters.private & filters.user(OWNER_ID))
async def command_add_admin(client: Bot, message: Message):
    while True:
        try:
            admin_id = await client.ask(text="Enter admin id 🔢\n /cancel to cancel : ",chat_id = message.from_user.id, timeout=60)
        except Exception as e:
            print(e)
            return
        if admin_id.text == "/cancel":
            await admin_id.reply("Cancelled 😉!")
            return
        try:
            await Bot.get_users(user_ids=admin_id.text, self=client)
            break
        except:
            await admin_id.reply("❌ Error 😖\n\nThe admin id is incorrect.", quote = True)
            continue
    if not await present_admin(admin_id.text):
        try:
            await add_admin(admin_id.text)
            await message.reply(f"Added admin <code>{admin_id.text}</code> 😼")
            try:
                await client.send_message(
                    chat_id=admin_id.text,
                    text=f"You are verified, ask the owner to add them to db channels. 😁"
                )
            except:
                await message.reply("Failed to send invite. Please ensure that they have started the bot. 🥲")
        except:
            await message.reply("Failed to add admin. 😔\nSome error occurred.")
    else:
        await message.reply("admin already exist. 💀")
    return


@Bot.on_message(filters.command('del_admin') & filters.private  & filters.user(OWNER_ID))
async def delete_admin_command(client: Bot, message: Message):
    while True:
        try:
            admin_id = await client.ask(text="Enter admin id 🔢\n /cancel to cancel : ",chat_id = message.from_user.id, timeout=60)
        except:
            return
        if admin_id.text == "/cancel":
            await admin_id.reply("Cancelled 😉!")
            return
        try:
            await Bot.get_users(user_ids=admin_id.text, self=client)
            break
        except:
            await admin_id.reply("❌ Error\n\nThe admin id is incorrect.", quote = True)
            continue
    if await present_admin(admin_id.text):
        try:
            await del_admin(admin_id.text)
            await message.reply(f"Admin <code>{admin_id.text}</code> removed successfully 😀")
        except Exception as e:
            print(e)
            await message.reply("Failed to remove admin. 😔\nSome error occurred.")
    else:
        await message.reply("admin doesn't exist. 💀")
    return

@Bot.on_message(filters.command('admins')  & filters.private & filters.private)
async def admin_list_command(client: Bot, message: Message):
    admin_list = await full_adminbase()
    await message.reply(f"Full admin list 📃\n<code>{admin_list}</code>")
    return

@Bot.on_message(filters.command('ping')  & filters.private)
async def check_ping_command(client: Bot, message: Message):
    start_t = time.time()
    rm = await message.reply_text("Pinging....", quote=True)
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await rm.edit(f"Ping 🔥!\n{time_taken_s:.3f} ms")
    return


@Client.on_message(filters.private & filters.command('restart') & filters.user(ADMINS))
async def restart(client, message):
    msg = await message.reply_text(
        text="<i>Trying To Restarting.....</i>",
        quote=True
    )
    await asyncio.sleep(5)
    await msg.edit("<i>Server Restarted Successfully ✅</i>")
    try:
        os.execl(sys.executable, sys.executable, *sys.argv)
    except Exception as e:
        print(e)


if USE_PAYMENT:
    @Bot.on_message(filters.command('add_prem') & filters.private & filters.user(ADMINS))
    async def add_user_premium_command(client: Bot, message: Message):
        while True:
            try:
                user_id = await client.ask(text="Enter id of user 🔢\n /cancel to cancel : ",chat_id = message.from_user.id, timeout=60)
            except Exception as e:
                print(e)
                return  
            if user_id.text == "/cancel":
                await user_id.edit("Cancelled 😉!")
                return
            try:
                await Bot.get_users(user_ids=user_id.text, self=client)
                break
            except:
                await user_id.edit("❌ Error 😖\n\nThe admin id is incorrect.", quote = True)
                continue
        user_id = int(user_id.text)
        while True:
            try:
                timeforprem = await client.ask(text="Enter the amount of time you want to provide the premium \nChoose correctly. Its not reversible.\n\n⁕ <code>1</code> for 7 days.\n⁕ <code>2</code> for 1 Month\n⁕ <code>3</code> for 3 Month\n⁕ <code>4</code> for 6 Month\n⁕ <code>5</code> for 1 year.🤑", chat_id=message.from_user.id, timeout=60)
            except Exception as e:
                print(e)
                return
            if not int(timeforprem.text) in [1, 2, 3, 4, 5]:
                await message.reply("You have given wrong input. 😖")
                continue
            else:
                break
        timeforprem = int(timeforprem.text)
        if timeforprem==1:
            timestring = "7 days"
        elif timeforprem==2:
            timestring = "1 month"
        elif timeforprem==3:
            timestring = "3 month"
        elif timeforprem==4:
            timestring = "6 month"
        elif timeforprem==5:
            timestring = "1 year"
        try:
            await increasepremtime(user_id, timeforprem)
            await message.reply("Premium added! 🤫")
            await client.send_message(
            chat_id=user_id,
            text=f"Update for you\n\nPremium plan of {timestring} added to your account. 🤫",
        )
        except Exception as e:
            print(e)
            await message.reply("Some error occurred.\nCheck logs.. 😖\nIf you got premium added message then its ok.")
        return

        
