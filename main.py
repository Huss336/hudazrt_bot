import requests
import time
import logging
from bs4 import BeautifulSoup
from telegram import Bot

# إعدادات البوت
TOKEN = "YOUR_BOT_TOKEN"  # استبدلها بتوكن البوت الخاص بك
CHAT_ID = "YOUR_CHAT_ID"  # استبدلها بمعرف تيليجرام الخاص بك

# رابط صفحة المنتجات
URL = "https://www.dzrt.com/ar-sa/products"

# تهيئة البوت
bot = Bot(token=TOKEN)

# تخزين المنتجات التي تم العثور عليها سابقًا
known_products = set()

def get_new_products():
    """جلب المنتجات الجديدة من موقع dzrt.com"""
    try:
        response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # استخراج قائمة المنتجات (قد تحتاج لتعديل هذا بناءً على هيكل الموقع)
        products = soup.find_all("div", class_="product-item")  # تأكد من الكلاس الصحيح

        new_products = []
        for product in products:
            title = product.find("h2").text.strip()
            link = product.find("a")["href"]
            full_link = f"https://www.dzrt.com{link}" if not link.startswith("http") else link

            if title not in known_products:
                known_products.add(title)
                new_products.append((title, full_link))

        return new_products

    except requests.RequestException as e:
        logging.error(f"حدث خطأ أثناء محاولة الوصول إلى الموقع: {e}")
        return []

def send_telegram_message(message):
    """إرسال إشعار إلى تيليجرام"""
    try:
        bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        logging.error(f"حدث خطأ أثناء إرسال الرسالة: {e}")

def main():
    """تشغيل الفحص كل دقيقة"""
    while True:
        new_products = get_new_products()
        if new_products:
            for title, link in new_products:
                send_telegram_message(f"🔔 منتج جديد متوفر: {title}\n🔗 الرابط: {link}")
        time.sleep(60)  # الفحص كل دقيقة

if _name_ == "_main_":
    main()
