import os

# کلیدهای API
BOT_TOKEN = os.getenv("BOT_TOKEN")
ETHERSCAN_API = os.getenv("ETHERSCAN_API")
BSCSCAN_API = os.getenv("BSCSCAN_API")

# نودهای بلاکچین
ETH_NODE = "https://mainnet.infura.io/v3/YOUR_INFURA_KEY"
BSC_NODE = "https://bsc-dataseed.binance.org/"

# لیست آدرس‌های نمونه
WATCH_LIST = [
    "0x8e80c4b533dd977cf716b5c24fd9223129272804",  # آدرس نمونه شما
    "0x00000000219ab540356cbb839cbe05303d7705fa"   # Binance Hot Wallet
]

# متن‌های سیستم
MENU_TEXT = """
🤖 **ربات حرفه‌ای Whale Alert**

▫️ تشخیص معامله‌گران واقعی
▫️ محاسبه خودکار TP/SL
▫️ پشتیبانی از چندین شبکه

انتخاب کنید:
"""