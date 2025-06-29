#ZSA : welcome to my code 

import tkinter as tk
from tkinter import messagebox

import requests
from bs4 import BeautifulSoup


def get_gold_price():
    try:
        url = "https://www.tgju.org"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        elements = soup.find_all("td", class_="nf")
        for element in elements:
            text = element.text.strip().replace(',', '')
            if text.isdigit() and len(text) > 5:
                return f"{int(text):,} ریال"
        return "یافت نشد"
    except:
        return "خطا در دریافت"


def get_crypto_price(symbol):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()

        price = data.get(symbol, {}).get("usd")
        if price:
            return f"{price:,} $"
        else:
            return "یافت نشد"

    except Exception as e:
        return f"خطا در دریافت: {e}"


def get_saffron_price():
    url = "https://maahto.ir/prices-of-saffron-days/"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        section = soup.find("h3", string=lambda t: "زعفران نگین صادراتی" in t)
        if section:
            text = section.get_text()
            price = text.split(":")[-1].strip().split()[0]
            return price + " تومان"
        else:
            return "یافت نشد"

    except Exception as e:
        return f"خطا: {e}"


def update_prices():
    status_label.config(text="در حال بروزرسانی...")
    root.update()

    gold = get_gold_price()
    btc = get_crypto_price("bitcoin")
    sol = get_crypto_price("solana")
    saffron = get_saffron_price()

    gold_label.config(text=f"قیمت سکه: {gold}")
    btc_label.config(text=f"بیت‌کوین: {btc}")
    sol_label.config(text=f"سولانا: {sol}")
    saffron_label.config(text=f"قیمت زعفران: {saffron}")

    status_label.config(text="✅ قیمت‌ها بروزرسانی شدند.")


root = tk.Tk()
root.title(" ZSA_app  ")
root.geometry("450x380")
root.configure(bg="#000000")  # بک گراند مشکی

# ===== لوگو اینجا اضافه کن =====
# لوگو باید PNG شفاف باشه و اندازه مناسب (مثلاً 100x100)
# کافیه فایل لوگو رو کنار همین فایل کد بذاری و نامش رو اینجا بگذاری
try:
    logo_img = tk.PhotoImage(file="logo.png")
    logo_label = tk.Label(root, image=logo_img, bg="#000000")
    logo_label.pack(pady=10)
except Exception:
    # اگر لوگو نیست، فقط متن رو نشون بده
    logo_label = tk.Label(root, text="ZSA Price Tracker", font=("Arial", 24, "bold"), fg="#00FF00", bg="#000000")
    logo_label.pack(pady=20)

# عنوان برنامه
title = tk.Label(root, text="📌 قیمت‌های لحظه‌ای", font=("Arial", 18, "bold"), fg="#00FF00", bg="#000000")
title.pack(pady=5)

# بخش قیمت طلا
gold_label = tk.Label(root, text=" قیمت سکه:  ---", font=("Arial", 14, "bold"), fg="#32CD32", bg="#000000")
gold_label.pack(pady=5)

# بخش قیمت بیت کوین
btc_label = tk.Label(root, text="بیت‌کوین: ---", font=("Arial", 14, "bold"), fg="#32CD32", bg="#000000")
btc_label.pack(pady=5)

# بخش قیمت سولانا
sol_label = tk.Label(root, text="سولانا: ---", font=("Arial", 14, "bold"), fg="#32CD32", bg="#000000")
sol_label.pack(pady=5)

# بخش قیمت زعفران
saffron_label = tk.Label(root, text="قیمت زعفران: ---", font=("Arial", 14, "bold"), fg="#32CD32", bg="#000000")
saffron_label.pack(pady=5)

# دکمه بروزرسانی
update_btn = tk.Button(root, text="🔄 بروزرسانی قیمت‌ها", font=("Arial", 14, "bold"), bg="#004400", fg="#00FF00", activebackground="#008000", activeforeground="#000000", command=update_prices)
update_btn.pack(pady=25)

# نمایش وضعیت بروزرسانی
status_label = tk.Label(root, text="", font=("Arial", 10, "italic"), fg="#00FF00", bg="#000000")
status_label.pack()

root.mainloop()
