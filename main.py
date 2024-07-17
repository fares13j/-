import requests, telebot, time, threading, random
from telebot import types
from chk import *

admin_id = "6896987155"
token = "7086228704:AAGmEUAmc7gWCU1JcmIF62TlFCE-i6xRfRk"
bot = telebot.TeleBot(token, parse_mode="HTML")

stop_processes = {}
video_urls = [f"https://t.me/O_An6/{i}" for i in [106, 110, 111, 112, 113, 114, 118, 119, 120, 121, 123, 124, 126, 129, 131, 132, 133, 136, 137, 208, 717, 722]]

blacklisted_bins = ['410039', '515462', '415464', '408264', '546775', '415464', '557692', '522274']
riskbins = []

process_running = False

def process(message):
    global process_running
    process_running = True
    video_url = random.choice(video_urls)
    process_id = hash(message)
    stop_processes[process_id] = False
    dd = live = risko = 0
    send = bot.send_video(message.chat.id, video_url, caption="𝐂𝐡𝐞𝐜𝐤𝐢𝐧𝐠 𝐘𝐨𝐮𝐫 𝐂𝐚𝐫𝐝𝐬...", parse_mode='Markdown', reply_to_message_id=message.message_id)
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_name = f"combo_{message.chat.id}.txt"
    
    try:
        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_file)
    except Exception as o:
        bot.send_message(admin_id, f"An error occurred: {o}")
        process_running = False
        return

    with open(file_name, 'r') as file:
        lino = file.readlines()
        total = len(lino)

        for card in lino:
            if card[:6] in riskbins or card[:6] in blacklisted_bins:
                continue
            
            start_time = time.time()
            
            try:
                result = chk(card)
            except Exception as e:
                bot.send_message(admin_id, f"An error occurred: {e}")
                result = "ERROR"
            
            time_taken = round(time.time() - start_time, 2)
            print(result)
            card = card.strip()

            if any(keyword in result for keyword in ['funds', 'OTP', 'Charged', 'Funds', 'avs', 'postal', 'approved', 'Nice!', 'Approved', 'cvv: Gateway Rejected: cvv', 'does not support this type of purchase.', 'Duplicate', 'Successful', 'Authentication Required', 'successful', 'Thank you', 'confirmed', 'successfully']):
                brand, type, level, bank, country_name, country_flag = info(card)
                live += 1
                bot.reply_to(message, f'𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅\n\n𝐂𝐚𝐫𝐝: <code>{card}</code>\n𝐆𝐚𝐭𝐞𝐰𝐚𝐲: Braintree Auth 🔥\n𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: {result}\n\n𝗜𝗻𝗳𝗼: {brand} - {type} - {level}\n𝐈𝐬𝐬𝐮𝐞𝐫: {bank}\n𝐂𝐨𝐮𝐧𝐭𝐫𝐲: {country_name} {country_flag}\n\n𝐓𝐢𝐦𝐞: {time_taken} 𝐬𝐞𝐜𝐨𝐧𝐝𝐬\n𝐁𝐲: <a href="tg://openmessage?user_id=1092890698">yaнya 🇯🇴</a>', parse_mode='HTML')
            elif 'RISK' in result:
                risko += 1
                riskbins.append(card[:6])
            else:
                dd += 1

            buttons = types.InlineKeyboardMarkup(row_width=1)
            buttons.add(
                types.InlineKeyboardButton(f"{card}", callback_data='1'),
                types.InlineKeyboardButton(f"{result}", callback_data='2'),
                types.InlineKeyboardButton(f"𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅ : {live}", callback_data='3'),
                types.InlineKeyboardButton(f"𝐑𝐢𝐬𝐤 ❌️ : {risko}", callback_data='4'),
                types.InlineKeyboardButton(f"𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌ : {dd}", callback_data='5'),
                types.InlineKeyboardButton(f"𝐓𝐨𝐭𝐚𝐥 🍬 : {total}", callback_data='6'),
                types.InlineKeyboardButton("𝐒𝐭𝐨𝐩", callback_data=f'stop_process_{process_id}')
            )
            
            bot.edit_message_caption(chat_id=message.chat.id, message_id=send.message_id, caption='', reply_markup=buttons)

            for _ in range(25):
                if stop_processes.get(process_id):
                    bot.edit_message_caption(chat_id=message.chat.id, message_id=send.message_id, caption="𝐒𝐭𝐨𝐩𝐩𝐞𝐝 𝐬𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲")
                    riskbins.clear()
                    process_running = False
                    return
                time.sleep(1)

    bot.edit_message_caption(chat_id=message.chat.id, message_id=send.message_id, caption="𝐂𝐨𝐦𝐩𝐥𝐞𝐭𝐞𝐝 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲")
    riskbins.clear()
    process_running = False


def info(card):
    url = f'https://bins.antipublic.cc/bins/{card[:6]}'
    response = requests.get(url)

    if any(substring in response.text for substring in ['Cloudflare', 'not found']) or response.status_code != 200:
        return tuple("------" for _ in range(6))
    
    fields = ['brand', 'type', 'level', 'bank', 'country_name', 'country_flag']
    result = [response.json().get(field, "------") for field in fields]
    
    return tuple(result)

@bot.callback_query_handler(func=lambda call: call.data.startswith('stop_process'))
def stop_process_callback(call):
    process_id = int(call.data.split('_')[-1])
    stop_processes[process_id] = True
    
@bot.message_handler(content_types=["document"])
def main(message):
    global process_running
    video_url = random.choice(video_urls)
    if str(message.chat.id) != admin_id:
        return
    if process_running:
        bot.send_video(message.chat.id, video_url, caption="𝐀 𝐩𝐫𝐨𝐜𝐞𝐬𝐬 𝐢𝐬 𝐚𝐥𝐫𝐞𝐚𝐝𝐲 𝐫𝐮𝐧𝐧𝐢𝐧𝐠. 𝐏𝐥𝐞𝐚𝐬𝐞 𝐰𝐚𝐢𝐭 𝐟𝐨𝐫 𝐢𝐭 𝐭𝐨 𝐜𝐨𝐦𝐩𝐥𝐞𝐭𝐞.", parse_mode='Markdown', reply_to_message_id=message.message_id)
    else:
        threading.Thread(target=process, args=[message]).start()

@bot.message_handler(commands=['start'])
def start_command(message):
    if str(message.chat.id) != admin_id:
        return   
    video_url = random.choice(video_urls)
    bot.send_video(message.chat.id, video_url, caption="𝐉𝐮𝐬𝐭 𝐬𝐞𝐧𝐝 𝐲𝐨𝐮𝐫 𝐜𝐨𝐦𝐛𝐨", parse_mode='Markdown', reply_to_message_id=message.message_id)

bot.infinity_polling()
