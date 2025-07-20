import os
import telebot
from telebot import types
import requests
from web3 import Web3
from flask import Flask, request
import threading
import time
from config import *

app = Flask(__name__)
bot = telebot.TeleBot(BOT_TOKEN)
w3 = {
    'eth': Web3(Web3.HTTPProvider(ETH_NODE)),
    'bsc': Web3(Web3.HTTPProvider(BSC_NODE))
}

# --- سیستم تشخیص معامله‌گران واقعی ---
def is_real_trader(address, chain='eth'):
    code = w3[chain].eth.get_code(address)
    tx_count = w3[chain].eth.get_transaction_count(address)
    return code == b'' and tx_count < 1000  # فیلتر ربات‌های پرتراکنش

# --- سیستم TP/SL ---
def calculate_risk(tx_value):
    entry = float(tx_value) * 0.98  # نقطه ورود 2% پایین‌تر
    tp = float(tx_value) * 1.05     # حد سود 5%
    sl = float(tx_value) * 0.95     # حد ضرر 5%
    return entry, tp, sl

# --- مانیتورینگ هوشمند ---
def monitor_wallets():
    while True:
        for wallet in WATCH_LIST:
            txs = get_transactions(wallet)
            for tx in txs:
                if is_real_trader(tx['from']):
                    entry, tp, sl = calculate_risk(tx['value'])
                    send_alert(tx, entry, tp, sl)
        time.sleep(60)

# --- رابط کاربری تلگرام ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    buttons = ["📊 مدیریت کیف‌پول‌ها", "⚙️ تنظیمات TP/SL", "🔔 نمونه آدرس"]
    markup.add(*buttons)
    bot.send_message(message.chat.id, MENU_TEXT, reply_markup=markup)

@app.route('/webhook', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return "OK", 200

if __name__ == '__main__':
    threading.Thread(target=monitor_wallets).start()
    app.run(host='0.0.0.0', port=5000)