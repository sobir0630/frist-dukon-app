import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog, ttk, filedialog
import os
import cv2
from PIL import Image, ImageTk
import json
import time
from datetime import datetime
import threading
import random
import re
import sys
from tkinter import font
import customtkinter as ctk
import win32print
import win32ui
import subprocess
import os
import sys
import subprocess
from tkinter import messagebox
import hashlib
import ichki_codes
import notebook
import print2
import sotish_file
import SEARCH



# Global ma'lumotlar
global deleted_phones
deleted_phones = []
phones = []  # Har bir telefon: {"nomi": ..., "modeli": ..., "sana": ..., "narx": ...}
language = "uz"  # Dastur standarti – o'zbek tili
dark_mode = True
data_file = "telefon_data.json"  # Ma'lumotlarni saqlash uchun fayl

# Tarjimalar (O'zbek va Rus)
translations = {
    "uz": {
        "reset": "Dasturni butunlay tozalash",
        "title": "IDEAL MOBILE",
        "phone_menu": "Tovar",
        "add_phone": "📱 Telefon qo‘shish",
        "delete_phone": "❌ Telefonni o‘chirish",
        "view_phones": "📋 Telefonlar ro‘yxati",
        "info_menu": "Malumotlar",
        "settings": "Sozlamalar",
        "success": "Muvaffaqiyatli",
        "error": "Xatolik",
        "added": "qo'shildi!",
        "deleted": "o'chirildi!",
        "no_phones": "Telefonlar mavjud emas!",
        "enter_name": "Telefon nomini kiriting:",
        "enter_model": "Telefon IMEI kiriting:",
        "enter_date": "Qo'shilgan sanani kiriting:",
        "enter_price": "Telefon narxini kiriting:",
        "enter_delete": "O'chirish uchun telefon nomini kiriting:",
        "phone_name_label": "Telefon Nomi",
        "model_label": "IMEI",
        "price_label": "Narxi",
        "date_label": "Sanasi",
        "change_language": "Tilni almashtirish",
        "dark_mode": "Tungi rejim",
        "login_title": "Kirish oynasi",
        "username": "Ism:",
        "password": "Parol:",
        "login": "Chiqish",
        "welcome": "Xush kelibsiz, hurmatli",
        "not_found": "topilmadi!",
        "logout": "Chiqish",
        "search": "Qidirish",
        "search_placeholder": "Telefon nomini yozing...",
        "save_data": "Ma'lumotlarni saqlash",
        "data_saved": "Ma'lumotlar saqlandi!",
        "load_data": "Ma'lumotlarni yuklash",
        "data_loaded": "Ma'lumotlar yuklandi!",
        "export_excel": "Excel formatiga eksport",
        "export_success": "Ma'lumotlar eksport qilindi!",
        "phone_stats": "📊 Statistika",
        "total_phones": "Jami telefonlar:",
        "avg_price": "O'rtacha narx:",
        "highest_price": "Eng qimmat:",
        "lowest_price": "Eng arzon:",
        "edit_phone": "Telefonni tahrirlash",
        "update": "Yangilash",
        "sort_by": "Saralash:",
        "sort_name": "Nomi bo'yicha",
        "sort_price_asc": "Narxi (o'sish)",
        "sort_price_desc": "Narxi (kamayish)",
        "sort_date": "Sana bo'yicha",
        "close": "Yopish",
        "confirm_delete": "Rostdan ham o'chirishni xohlaysizmi?",
        "yes": "Ha",
        "no": "Yo'q",
        "edit": "Tahrirlash",
        "today": "Bugun",
        "fill_all": "Barcha maydonlarni to'ldiring!",
        "report": "Hisobot",
        "generate_report": "Hisobot yaratish",
        "theme": "Mavzu",
        "classic": "Klassik",
        "blue": "Ko'k mavzu",
        "green": "Yashil mavzu",
        "white": "kunduzgi mavzu",
        "black": "kechki mavzu",
        "phone_image": "Telefon rasmi",
        "about": "Dastur haqida",
        "total_price": "Jami narx:",
        "about_text": "Telefon Do'koni Dasturi\nVersiya 2.0\n\nDastur telefon do'konidagi tovarlarni boshqarish uchun yaratilgan.\n\n©2025 Barcha huquqlar himoyalangan.",
        "tur": "turi",
        "index": "indexi",
        "holat": "holati",
        "qushilgan": "qushilgan sana",
        "kunduzgi_theme": "kunduzgi mavzu",
        "kechgi_theme": "kechgi mavzu",
        "muviqli": "Muvoffaqiyatli",
        "tel_index": "telefon indexi",
        "asosiy": "📋 Asosiy Ma'lumotlar",
        "nomi": "📱 Telefon Nomi:",
        "turi": "🏷️ Telefon Turi:",
        "Moliyaviy": "💰 Moliyaviy Ma'lumotlar",
        "sell_narx": "💰 Sotib Olingan Narx ($):",
        "sell_sana": "📅 Sotib Olingan Sana:",
        "bug": "📅 Bugun",
        "qush_mal": "📝 Qo'shimcha Ma'lumotlar",
        "tel_hol": "⚡ Telefon Holati:",
        "malumot": ["Yangi", "Juda Yaxshi", "Yaxshi", "O'rtacha", "Tuzatishga Muhtoj"],
        "tasdiq": "✅ Tasdiqlash",
        "tel_qush": "📱 Telefon Qo'shilmoqda...",
        "qush": "qo'shilmoqda...",
        "saqla": "✅ Saqlash",
        "bekor_q": "❌ Bekor qilish",
        "yangilash": "yangilash",
        "tur": "Turi",
        "san": "Sana",
        "hol": "Holati",
        "qushil": "Qushilgan sana",
        "xato": "❌ Xatolik",
        "tel_tanla": "Iltimos, telefon tanlang!",
        "about": "Telefon haqida",
        "sot": "✅ Sotish",
        "chop_et": "🖨️ Chop etish",
        "yop": "Yopish",
        "sotuvga_ut": "Sotuvga utish",
        "savdo_st": "📊 Savdo statistikasi",
        "sotilgan_san": "Sotilgan sana",
        "davr": "Davrni tanlang",
        "tel_jad": "Telefonlar jadvali topilmadi!",
        "tel_jad_yuq": "Tanlangan telefon mavjud emas.",
        "sell_tel": "📱 Telefon Sotish",
        "tel_info": "📋 Telefon Ma'lumotlari",
        "narx_info": "💰 Narx Ma'lumotlari",
        "sell_info": "Sotish Narxi ($):",
        "sel_entry": "Sotish narxini kiriting",
        "foyda/zarar": "💹 Foyda/Zarar: $0.00",
        "noturi": "❌ Noto'g'ri narx",
        "mijoz": "👤 Mijoz Ma'lumotlari",
        "mj": "👤 Mijoz Ismi:",
        "mj_name": "Mijoz ismini kiriting",
        "mj_tel": "📞 Telefon Raqami:",
        "sel_narx": "Sotish narxini kiriting!",
        "sel_0": "Sotish narxi 0 dan katta bo'lishi kerak!",
        "ero": "Mijoz telefon raqamini kiriting!",
        "neto": "Noto'g'ri narx formati!\nFaqat raqam kiriting.",
        "mavj":"Sotilgan yoki o'chirilgan telefonlar mavjud emas!",
        "tel_istory": "📱 Telefon tarixi",
        "qdr": "Qidirish:",
        "qdr_matn": "Qidirish uchun matn kiriting...",
        "total": "Jami",
        "sel": "Sotilgan",
        "uchrl": "O'chirilgan",
        "umumiy": "Umumiy",
        "tel_serch": "Telefon qidirish",
        "tel_qdr_imai": "🔍 IMEI orqali telefon qidirish",
        "4_imai": "IMEI oxirgi 4 raqam:",
        "4_imai_qdr": "IMEI raqamning oxirgi 4 ta raqamini kiriting",
        "seel_phon": "📱 Sotilgan telefonlar",
        "phone_istory": "📊 Telefon tarixi",
        "print": "🖨️ SHTRIX KOD",
        "title": "Telefon do'kon dasturi",
        "phone_menu": "Telefonlar",
        "settings_menu": "Sozlamalar",
        "yangilar": "yangilar",
        "note": "Eslatmalar",
        "sell_0": "Sotish narxi 0 dan katta bo'lishi kerak!"

    },
    "ru": {
        "reset": "Полная очистка программы",
        "note": "Примечания",
        "yangilar": "Новички",
        "settings_menu": "Настройки",
        "title": "Магазин телефонов",
        "phone_menu": "Телефоны",
        "print": "🖨️ БАР КОД",
        "phone_istory": "📊 История телефона",
        "seel_phon": "📱 Проданные телефоны",
        "4_imai_qdr": "Введите последние 4 цифры номера IMEI",
        "4_imai": "Последние 4 цифры IMEI:",
        "tel_qdr_imai": "🔍 Поиск телефона по IMEI",
        "tel_serch": "Поиск телефона",
        "umumiy": "Общий",
        "sel": "Продал",
        "uchrl": "Выключенный",
        "total": "Общий",
        "qdr_matn": "Введите текст для поиска...",
        "qdr": "Поиск:",
        "tel_istory": "📱 История телефона",
        "mavj":"Проданных или деактивированных телефонов нет!",
        "neto": "Неверный формат цены!\nВведите только число.",
        "ero": "Введите номер телефона клиента!",
        "sel_0": "Цена продажи должна быть больше 0!",
        "sel_xarx": "Введите цену продажи!",
        "mj_tel": "📞 Номер телефона:",
        "mj_name": "Введите имя клиента",
        "mj": "👤 Имя клиента:",
        "mijoz": "👤 Информация для клиентов",
        "noturi": "❌ Неправильная цена",
        "foyda/zarar": "💹 Прибыль/Убыток: $0.00",
        "sel_entry": "Введите цену продажи",
        "sell_info": "Цена продажи ($):",
        "narx_info": "💰 Информация о ценах",
        "tel_info": "📋 Информация о телефоне",
        "sell_tel": "📱 Продажи по телефону",
        "davr": "Выберите период",
        "sotilgan_san": "Дата продажи",
        "savdo_st": "📊 Статистика продаж",
        "sotuvga_ut": "Поступить в продажу",
        "yop": "закрывать",
        "chop_et": "печать",
        "sot": "Распродажа",
        "about": "О телефоне",
        "tel_tanla": "Пожалуйста, выберите телефона!",
        "xato": "Oшибка",
        "qushil": "Дата добавления",
        "hol": "Статус",
        "san": "Дата",
        "tur": "Тип",
        "yangilash": "обновлять",
        "bekor_q": "❌ Отмена",
        "saqla": "✅ Сохранять",
        "qush": "добавление...",
        "tel_qush": "📱 Подключение телефона...",
        "tasdiq": "✅ Подтверждение",
        "malumot": ["Новый", "Очень хорошо", "Хорошо", "Средне", "Требуется улучшение"],
        "tel_hol": "⚡ Статус телефона:",
        "qush_mal": "📝 Дополнительная информация",
        "bug": "📅 сегодня",  
        "sell_sana": "📅 Дата покупки:",
        "sell_narx": "💰 Цена покупки ($):",     
        "Moliyaviy": "💰 Финансовая информация",
        "turi": "🏷️ Тип телефона:",
        "nomi": "📱 Имя телефона:",
        "asosiy": "📋 Основная информация",
        "tel_index": "телефонный справочник",
        "title": "Программа магазина телефонов",
        "phone_menu": "Телефонные товары",
        "add_phone": "📱 Добавить телефон",
        "delete_phone": "❌ Удалить телефон",
        "view_phones": "📋 Список телефонов",
        "info_menu": "Информация",
        "settings": "Настройки",
        "success": "Успешно",
        "error": "Ошибка",
        "added": " добавлен!",
        "deleted": " удалён!",
        "no_phones": "Телефонов нет!",
        "enter_name": "Введите название телефона:",
        "enter_model": "Введите модель телефона:",
        "enter_date": "Введите дату добавления:",
        "enter_price": "Введите цену телефона:",
        "enter_delete": "Введите название для удаления:",
        "phone_name_label": "Название телефона",
        "model_label": "Модель",
        "price_label": "Цена",
        "date_label": "Дата добавления",
        "change_language": "Сменить язык",
        "dark_mode": "Ночной режим",
        "login_title": "Окно входа",
        "username": "Имя:",
        "password": "Пароль:",
        "login": "Выход",
        "welcome": "Добро пожаловать, уважаемый",
        "not_found": "не найден!",
        "logout": "Выход",
        "search": "Поиск",
        "search_placeholder": "Введите название телефона...",
        "save_data": "Сохранить данные",
        "data_saved": "Данные сохранены!",
        "load_data": "Загрузить данные",
        "data_loaded": "Данные загружены!",
        "export_excel": "Экспорт в Excel",
        "export_success": "Данные экспортированы!",
        "phone_stats": "Статистика телефонов",
        "total_phones": "Всего телефонов:",
        "avg_price": "Средняя цена:",
        "highest_price": "Самый дорогой:",
        "lowest_price": "Самый дешевый:",
        "edit_phone": "Редактировать телефон",
        "update": "Обновить",
        "sort_by": "Сортировать по:",
        "sort_name": "Названию",
        "sort_price_asc": "Цене (возр.)",
        "sort_price_desc": "Цене (убыв.)",
        "sort_date": "Дате",
        "close": "Закрыть",
        "confirm_delete": "Вы действительно хотите удалить?",
        "yes": "Да",
        "no": "Нет",
        "edit": "Редактировать",
        "today": "Сегодня",
        "fill_all": "Заполните все поля!",
        "report": "Отчет",
        "generate_report": "Создать отчет",
        "theme": "Тема",
        "classic": "Классическая",
        "blue": "Синяя тема",
        "green": "Зеленая тема",
        "white": "дневная тема",
        "black": "вечерняя тема",
        "phone_image": "Изображение телефона",
        "about": "О программе",
        "total_price": "Общая сумма:",
        "about_text": "Программа магазина телефонов\nВерсия 2.0\n\nПрограмма создана для управления товарами в магазине телефонов.\n\n©2025 Все права защищены.",
        "tur": "тип",
        "index": "индекс",
        "holat": "состояние",
        "qushilgan": "дата въезда",
        "kunduzgi_theme": "тема дня",
        "kechgi_theme": " тема ноч",
        "muviqli": "Успешный"

    }
}

# Ranglar sxemalari
themes = {
    "classic": {
        "light": {
            "bg": "#DFFFD6",
            "fg": "#C5CAC7",
            "button_bg": "#1E88E5",
            "button_fg": "#FFFFFF",
            "entry_bg": "#FFFFFF",
            "entry_fg": "#000000",
            "highlight_bg": "#4932CD",
            "border": "#35228B",
            "menu_bg": "#DFFFD6",   # <-- Qo'shildi
            "menu_fg": "#5C3131" 
        },
        "dark": {
            "bg": "#1E1E1E",
            "fg": "#C5CAC7",
            "button_bg": "#1E88E5",
            "button_fg": "#FFFFFF",
            "entry_bg": "#333333",
            "entry_fg": "#FFFFFF",
            "highlight_bg": "#3A5F0B",
            "border": "#3A5F0B",
            "menu_bg": "#1E1E1E",   # <-- Qo'shildi
            "menu_fg": "#FFFFFF" 
        }
    },
    "blue": {
        "light": {
            "bg": "#E6F2FF",
            "fg": "#C5CAC7",
            "button_bg": "#1E88E5",
            "button_fg": "#FFFFFF",
            "entry_bg": "#FFFFFF",
            "entry_fg": "#000000",
            "highlight_bg": "#64B5F6",
            "border": "#1E88E5",
            "menu_bg": "#1E1E1E",   # <-- Qo'shildi
            "menu_fg": "#FFFFFF" 
        },
        "dark": {
            "bg": "#0A1929",
            "fg": "#C5CAC7",
            "button_bg": "#1976D2",
            "button_fg": "#FFFFFF",
            "entry_bg": "#102A43",
            "entry_fg": "#FFFFFF",
            "highlight_bg": "#1565C0",
            "border": "#1565C0",
            "menu_bg": "#1E1E1E",   # <-- Qo'shildi
            "menu_fg": "#FFFFFF" 
        }
    },
    "green": {
        "light": {
            "bg": "#E8F5E9",
            "fg": "#C5CAC7",
            "button_bg": "#1E88E5",
            "button_fg": "#FFFFFF",
            "entry_bg": "#FFFFFF",
            "entry_fg": "#000000",
            "highlight_bg": "#81C784",
            "border": "#43A047",
            "menu_bg": "#1E1E1E",   # <-- Qo'shildi
            "menu_fg": "#FFFFFF" 
        },
        "dark": {
            "bg": "#0A1F0A",
            "fg": "#C5CAC7",
            "button_bg": "#2E7D32",
            "button_fg": "#FFFFFF",
            "entry_bg": "#1B5E20",
            "entry_fg": "#FFFFFF",
            "highlight_bg": "#2E7D32",
            "border": "#2E7D32",
            "menu_bg": "#1E1E1E",   # <-- Qo'shildi
            "menu_fg": "#FFFFFF" 
        }
    },

    "white": {  # Kunduzgi tema
        "light": {
            "bg": "#FFFFFF",
            "fg": "#C5CAC7",
            "button_bg": "#1E88E5",
            "button_fg": "#FFFFFF", 
            "entry_bg": "#F5F5F5",
            "entry_fg": "#333333",
            "highlight_bg": "#81C784",
            "border": "#4CAF50",
            "frame_bg": "#F8F9FA",
            "frame_border": "#DEE2E6",
            "menu_bg": "#FFFFFF",
            "menu_fg": "#333333",
            "selected_bg": "#E8F5E9",
            "selected_fg": "#2E7D32",
            "hover_bg": "#C8E6C9"
        },
        "dark": {  # Fallback for dark mode
            "bg": "#FFFFFF",
            "fg": "#C5CAC7",
            "button_bg": "#4CAF50",
            "button_fg": "#FFFFFF",
            "entry_bg": "#F5F5F5",
            "entry_fg": "#333333",
            "highlight_bg": "#81C784", 
            "border": "#4CAF50"
        }
    },

    "black": {  # Kechki tema
        "light": {  # Fallback for light mode 
            "bg": "#121212",
            "fg": "#C5CAC7",
            "button_bg": "#BB86FC",
            "button_fg": "#000000",
            "entry_bg": "#1E1E1E",
            "entry_fg": "#FFFFFF",
            "highlight_bg": "#3700B3",
            "border": "#BB86FC"
        },
        "dark": {
            "bg": "#121212",
            "fg": "#C5CAC7",
            "button_bg": "#BB86FC",
            "button_fg": "#000000",
            "entry_bg": "#1E1E1E", 
            "entry_fg": "#FFFFFF",
            "highlight_bg": "#3700B3",
            "border": "#BB86FC",
            "frame_bg": "#1E1E1E",
            "frame_border": "#333333",
            "menu_bg": "#121212",
            "menu_fg": "#FFFFFF",
            "selected_bg": "#3700B3",
            "selected_fg": "#FFFFFF",
            "hover_bg": "#6200EE"
        }
    }
    
}







# # Joriy mavzu
current_theme = "classic"
colors = themes[current_theme]["dark" if dark_mode else "light"]

# Telefon rasmining o'rni
phone_images = {
    "iPhone": "iphone.png",
    "Samsung": "samsung.png",
    "Xiaomi": "xiaomi.png",
    "default": "phone.png"
}

try:
    # Rasmlarni saqlash uchun katalog yaratish
    if not os.path.exists("images"):
        os.makedirs("images")
except:
    pass


# Oynani markazlashtirish funksiyasi (kerakli funksiyani qo'shdik)
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))


# Mavzuni o'zgartirish funksiyasi (qo'shildi)
# def change_theme(theme_name):
#     global current_theme, colors
#     current_theme = theme_name
#     colors = themes[current_theme]["dark" if dark_mode else "light"]
#     # Mavzuni qo'llash kodlari (root_app configuratsiyasi)
#     if 'root_app' in globals():
#         root_app.configure(bg=colors["bg"])
#         # Boshqa UI elementlarini yangilash...

# # Kunduzgi mavzuga o'tish uchun
#     change_theme("white")

#     # Kechki mavzuga o'tish uchun
#     change_theme("black")


    # Menu qismiga qo'shish


def lock_application():
    from tkinter import messagebox
    answer = messagebox.askyesno("Chiqish", "Dasturdan chiqishni istaysizmi?")
    if answer:
        root_app.destroy()  # dastur butunlay yopiladi


# Tungi rejimni o'zgartirish funksiyasi (qo'shildi)
def toggle_dark_mode():
    global dark_mode, colors
    dark_mode = not dark_mode
    colors = themes[current_theme]["dark" if dark_mode else "light"]
    # Mavzuni qo'llash kodlari (root_app configuratsiyasi)
    if 'root_app' in globals():
        root_app.configure(bg=colors["bg"])
        # Boshqa UI elementlarini yangilash...





# Optimallashtirish uchun funksiyalar
def save_data():
    try:
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(phones, f, ensure_ascii=False, indent=4)
        messagebox.showinfo(translations[language]["success"], translations[language]["data_saved"])
    except Exception as e:
        messagebox.showerror(translations[language]["error"], str(e))


def load_data():
    global phones, sold_phones, deleted_phones
    try:
        # Telefon ma'lumotlarini yuklash
        if os.path.exists(data_file):
            with open(data_file, 'r', encoding='utf-8') as f:
                phones = json.load(f)
        else:
            phones = []
        
        # Sotilgan telefonlar ma'lumotlarini yuklash
        sold_file = "sold_phones.json"
        if os.path.exists(sold_file):
            with open(sold_file, 'r', encoding='utf-8') as f:
                sold_phones = json.load(f)
        else:
            sold_phones = []
            if sold_phones:
                messagebox.showinfo("saqlandi", "sotilgan telefonlar fayli qayta saqlandi")
            
        
        # O'chirilgan telefonlar ma'lumotlarini yuklash
        deleted_file = "deleted_phones.json"
        if os.path.exists(deleted_file):
            with open(deleted_file, 'r', encoding='utf-8') as f:
                deleted_phones = json.load(f)
        else:
            deleted_phones = []
    except Exception as e:
        messagebox.showerror(translations[language]["error"], str(e))


def on_exit():
    if messagebox.askyesno(translations[language]["save_data"], "Dasturdan chiqishdan oldin ma'lumotlarni saqlashni xohlaysizmi?"):
        save_data()
    root_app.destroy()

    # Telefon uchun rasmni olish
# Telefon rasmlari uchun lug‘at
phone_images = {
    "iphone": "📲",
    "samsung": "📱",
    "xiaomi": "🎛",
    "default": "💻"
}

def get_phone_image(phone_name):
    """
    Telefon nomiga qarab mos rasmni qaytaradi.
    Agar telefon topilmasa, default rasm qaytariladi.
    """
    for key in phone_images:
        if key.lower() in phone_name.lower():
            image_path = phone_images[key]
            if os.path.exists(image_path):
                return PhotoImage(file=image_path)  # Tkinter rasm obyektini qaytaradi
                return tk.PhotoImage(file=image_path)  # Tkinter rasm obyektini qaytaradi
    # Default rasmni qaytarish
    default_path = phone_images["default"]
    if os.path.exists(default_path):
        return PhotoImage(file=default_path)
    else:
        return None  # Agar fayl topilmasa, hech narsa qaytarmaydi


# Login funksiyasi (qo'shildi)
def show_login_screen():
    login_window = tk.Toplevel(root_app)
    login_window.title(translations[language]["login_title"])
    login_window.geometry("500x500")
    login_window.configure(bg=colors["bg"])
    login_window.resizable(False, False)
    login_window.transient(root_app)
    login_window.grab_set()

    center_window(login_window)

    # Login forma
    tk.Label(login_window, text=translations[language]["username"],
             bg=colors["bg"], fg=colors["fg"]).pack(pady=(20, 5))
    username_entry = tk.Entry(login_window, bg=colors["entry_bg"], fg=colors["entry_fg"])
    username_entry.pack(pady=5, padx=20, fill="x")

    tk.Label(login_window, text=translations[language]["password"],
             bg=colors["bg"], fg=colors["fg"]).pack(pady=5)
    password_entry = tk.Entry(login_window, bg=colors["entry_bg"], fg=colors["entry_fg"], show="*")
    password_entry.pack(pady=5, padx=20, fill="x")

    def login_action():
        username_input = username_entry.get()
        password_input = password_entry.get()

        # Sodda tekshirish (amaliy dasturda to'g'ri autentifikatsiya qo'llanishi kerak)
        # To'g'ri login va parol
        correct_username = "IDEAL MOBILE"
        correct_password = "9959"

        if username == CORRECT_USERNAME and password == CORRECT_PASSWORD:
            login_window.destroy()
            messagebox.showinfo(translations[language]["Muvaffaqiyat"], f"Xush kelibsiz, {correct_username}!")
        else:
            messagebox.showerror("Xatolik", "Login yoki parol noto‘g‘ri!")

    login_btn = tk.Button(login_window, text=translations[language]["login"],
                          bg=colors["button_bg"], fg=colors["button_fg"],
                          font=("Arial", 10, "bold"), command=login_action)
    login_btn.pack(pady=15)



def add_phone():
    """Telefon qo'shish funksiyasi - zamonaviy dizayn va avtomatik indeks bilan"""
    global phones
    
    # Zamonaviy qo'shish oynasi
    add_window = ctk.CTkToplevel()
    add_window.title(translations[language]["add_phone"])
    add_window.geometry("650x800")
    add_window.configure(fg_color=("#f8f9fa", "#1a1a1a"))
    add_window.resizable(False, False)
    
    # Oynani markazlashtirish
    add_window.update_idletasks()
    x = (add_window.winfo_screenwidth() // 2) - (650 // 2)
    y = (add_window.winfo_screenheight() // 2) - (800 // 2)
    add_window.geometry(f"650x800+{x}+{y}")
    
    # Modal oyna qilish
    add_window.transient()
    add_window.grab_set()
    add_window.focus_set()

    # Asosiy sarlavha
    title_label = ctk.CTkLabel(
        add_window,
        text=translations[language]["add_phone"],
        font=ctk.CTkFont(size=28, weight="bold"),
        text_color=("#2c3e50", "#ecf0f1")
    )
    title_label.pack(pady=(20, 30))

    index = translations[language]["tel_index"]
    # Avtomatik indeks ko'rsatish
    next_index = len(phones) + 1
    index_label = ctk.CTkLabel(
        add_window,
        text=f"{index} #{next_index:03d}",
        font=ctk.CTkFont(size=16, weight="bold"),
        text_color=("#3498db", "#5dade2"),
        fg_color=("#ecf0f1", "#2c3e50"),
        corner_radius=20,
        width=200,
        height=40
    )
    index_label.pack(pady=(0, 20))

    # Asosiy form frame
    main_frame = ctk.CTkScrollableFrame(add_window, width=580, height=500)
    main_frame.pack(pady=(0, 20), padx=30, fill="both", expand=True)

    # Telefon ma'lumotlari bo'limi
    info_frame = ctk.CTkFrame(main_frame)
    info_frame.pack(pady=(0, 20), padx=20, fill="x")

    malum = translations[language]["asosiy"]
    info_title = ctk.CTkLabel(
        info_frame,
        text=malum,
        font=ctk.CTkFont(size=18, weight="bold"),
        text_color=("#34495e", "#bdc3c7")
    )
    info_title.pack(pady=(15, 20))


    nomi = translations[language]["nomi"]
    # Telefon nomi
    name_label = ctk.CTkLabel(
        info_frame,
        text=nomi,
        font=ctk.CTkFont(size=14),
        text_color=("#2c3e50", "#ecf0f1"),
        anchor="w"
    )
    name_label.pack(pady=(5, 5), padx=20, fill="x")

    name_entry = ctk.CTkEntry(
        info_frame,
        placeholder_text="iPhone 15 Pro Max, Samsung Galaxy S24, Xiaomi 14...",
        font=ctk.CTkFont(size=14),
        height=45,
        corner_radius=10
    )
    name_entry.pack(pady=(0, 15), padx=20, fill="x")

    # IMEI/Model
    model_label = ctk.CTkLabel(
        info_frame,
        text="🔢 IMEI / Model:",
        font=ctk.CTkFont(size=14),
        text_color=("#2c3e50", "#ecf0f1"),
        anchor="w"
    )
    model_label.pack(pady=(5, 5), padx=20, fill="x")

    model_entry = ctk.CTkEntry(
        info_frame,
        placeholder_text="123456789012345 yoki A2848",
        font=ctk.CTkFont(size=14),
        height=45,
        corner_radius=10
    )
    model_entry.pack(pady=(0, 15), padx=20, fill="x")

    turi = translations[language]["turi"]
    # Telefon turi
    type_label = ctk.CTkLabel(
        info_frame,
        text=turi,
        font=ctk.CTkFont(size=14),
        text_color=("#2c3e50", "#ecf0f1"),
        anchor="w"
    )
    type_label.pack(pady=(5, 5), padx=20, fill="x")

    phone_types = ["iPhone", "Samsung", "Xiaomi", "Huawei", "OnePlus", "Google Pixel", "Oppo", "Vivo", "Realme", "Other"]
    type_combo = ctk.CTkComboBox(
        info_frame,
        values=phone_types,
        font=ctk.CTkFont(size=14),
        height=45,
        corner_radius=10,
        state="readonly"
    )
    type_combo.set("iPhone")
    type_combo.pack(pady=(0, 20), padx=20, fill="x")

    # Narx va sana bo'limi
    price_date_frame = ctk.CTkFrame(main_frame)
    price_date_frame.pack(pady=(0, 20), padx=20, fill="x")


    Moliyaviy = translations[language]["Moliyaviy"]
    price_date_title = ctk.CTkLabel(
        price_date_frame,
        text=Moliyaviy,
        font=ctk.CTkFont(size=18, weight="bold"),
        text_color=("#34495e", "#bdc3c7")
    )
    price_date_title.pack(pady=(15, 20))


    sell = translations[language]["sell_narx"]
    # Narx
    price_label = ctk.CTkLabel(
        price_date_frame,
        text=sell,
        font=ctk.CTkFont(size=14),
        text_color=("#2c3e50", "#ecf0f1"),
        anchor="w"
    )
    price_label.pack(pady=(5, 5), padx=20, fill="x")

    price_entry = ctk.CTkEntry(
        price_date_frame,
        placeholder_text="999.99",
        font=ctk.CTkFont(size=14),
        height=45,
        corner_radius=10
    )
    price_entry.pack(pady=(0, 15), padx=20, fill="x")

    sell_sana2 = translations[language]["sell_sana"]
    # Sana
    date_label = ctk.CTkLabel(
        price_date_frame,
        text=sell_sana2,
        font=ctk.CTkFont(size=14),
        text_color=("#2c3e50", "#ecf0f1"),
        anchor="w"
    )
    date_label.pack(pady=(5, 5), padx=20, fill="x")

    # Sana frame
    date_frame = ctk.CTkFrame(price_date_frame, fg_color="transparent")
    date_frame.pack(pady=(0, 20), padx=20, fill="x")

    date_entry = ctk.CTkEntry(
        date_frame,
        placeholder_text="DD/MM/YYYY",
        font=ctk.CTkFont(size=14),
        height=45,
        corner_radius=10
    )
    date_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

    def set_today_date():
        today = datetime.now().strftime("%d/%m/%Y")
        date_entry.delete(0, "end")
        date_entry.insert(0, today)


    bug = translations[language]["bug"]
    today_button = ctk.CTkButton(
        date_frame,
        text=bug,
        command=set_today_date,
        font=ctk.CTkFont(size=14, weight="bold"),
        fg_color=("#3498db", "#2980b9"),
        hover_color=("#2980b9", "#3498db"),
        width=100,
        height=45,
        corner_radius=10
    )
    today_button.pack(side="right")

    # Qo'shimcha ma'lumotlar bo'limi
    extra_frame = ctk.CTkFrame(main_frame)
    extra_frame.pack(pady=(0, 20), padx=20, fill="x")

    qush_mal = translations[language]["qush_mal"]
    extra_title = ctk.CTkLabel(
        extra_frame,
        text=qush_mal,
        font=ctk.CTkFont(size=18, weight="bold"),
        text_color=("#34495e", "#bdc3c7")
    )
    extra_title.pack(pady=(15, 20))


    tel_hol = translations[language]["tel_hol"]
    # Holat
    condition_label = ctk.CTkLabel(
        extra_frame,
        text=tel_hol,
        font=ctk.CTkFont(size=14),
        text_color=("#2c3e50", "#ecf0f1"),
        anchor="w"
    )
    condition_label.pack(pady=(5, 5), padx=20, fill="x")


    malumot = translations[language]["malumot"]
    conditions = malumot
    condition_combo = ctk.CTkComboBox(
        extra_frame,
        values=conditions,
        font=ctk.CTkFont(size=14),
        height=45,
        corner_radius=10,
        state="readonly"
    )
    condition_combo.set("Yangi")
    condition_combo.pack(pady=(0, 15), padx=20, fill="x")


    # Validatsiya funksiyalari
    def validate_price(price_str):
        """Narxni tekshirish"""
        try:
            price = float(re.sub(r'[^\d.]', '', price_str))
            return price > 0, price
        except ValueError:
            return False, 0

    def validate_date(date_str):
        """Sanani tekshirish"""
        try:
            datetime.strptime(date_str, "%d/%m/%Y")
            return True
        except ValueError:
            return False

    def save_phone():
        """Telefonni saqlash funksiyasi"""
        # Ma'lumotlarni olish
        name = name_entry.get().strip()
        model = model_entry.get().strip()
        date = date_entry.get().strip()
        price_str = price_entry.get().strip()
        phone_type = type_combo.get()
        condition = condition_combo.get()
        # note = note_entry.get("1.0", "end").strip()

        # Asosiy maydonlarni tekshirish
        if not name:
            messagebox.showerror("❌ Xatolik", "Telefon nomini kiriting!")
            name_entry.focus()
            return

        if not model:
            messagebox.showerror("❌ Xatolik", "IMEI yoki model raqamini kiriting!")
            model_entry.focus()
            return

        if not date:
            messagebox.showerror("❌ Xatolik", "Sotib olingan sanani kiriting!")
            date_entry.focus()
            return

        if not price_str:
            messagebox.showerror("❌ Xatolik", "Narxni kiriting!")
            price_entry.focus()
            return

        # Narxni tekshirish
        is_valid_price, price = validate_price(price_str)
        if not is_valid_price:
            messagebox.showerror("❌ Xatolik", "Noto'g'ri narx formati!\nFaqat raqam kiriting.")
            price_entry.focus()
            return

        # Sanani tekshirish
        if not validate_date(date):
            messagebox.showerror("❌ Xatolik", "Noto'g'ri sana formati!\nDD/MM/YYYY formatida kiriting.")
            date_entry.focus()
            return

        # Tasdiqlash
        confirm_text = (
            "📱 TELEFON QO'SHISH TASDIQLASH\n"

            f"🆔 Indeks: #{next_index:03d}\n"
            f"📱 Nomi: {name}\n"
            f"🔢 IMEI/Model: {model}\n"
            f"🏷️ Turi: {phone_type}\n"
            f"💰 Narx: ${price:.2f}\n"
            f"📅 Sana: {date}\n"
            f"⚡ Holat: {condition}\n"
            # f"📝 Eslatma: {note if note else 'Yuq'}\n"

            "❓ Telefonni qo'shishni tasdiqlaysizmi?"
        )

        if not messagebox.askyesno("✅ Tasdiqlash", confirm_text):
            return

        # Progress oynasi
        progress_window = ctk.CTkToplevel(add_window)
        progress_window.title(translations[language]["tel_qush"])
        progress_window.geometry("400x200")
        progress_window.configure(fg_color=("#f8f9fa", "#1a1a1a"))
        progress_window.resizable(False, False)
        progress_window.transient(add_window)
        progress_window.grab_set()
        
        # Progress oynasini markazlashtirish
        progress_window.update_idletasks()
        x = (progress_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (progress_window.winfo_screenheight() // 2) - (200 // 2)
        progress_window.geometry(f"400x200+{x}+{y}")


        qush = translations[language]["qush"]
        # Progress elementi
        progress_label = ctk.CTkLabel(
            progress_window,
            text=f"📱 {name} {qush}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("#2c3e50", "#ecf0f1")
        )
        progress_label.pack(pady=(30, 20))

        progress_bar = ctk.CTkProgressBar(
            progress_window,
            width=300,
            height=20,
            corner_radius=10
        )
        progress_bar.pack(pady=10)
        progress_bar.set(0)

        progress_percent = ctk.CTkLabel(
            progress_window,
            text="0%",
            font=ctk.CTkFont(size=14),
            text_color=("#7f8c8d", "#bdc3c7")
        )
        progress_percent.pack(pady=5)

        def animate_progress():
            """Progress animatsiyasi"""
            for i in range(101):
                progress_bar.set(i / 100)
                progress_percent.configure(text=f"{i}%")
                progress_window.update()
                import time

                print("Jarayon boshlanmoqda...")
                time.sleep(0.01)  # 0.01 soniya kutadi
                print("Yakunlandi.")

                # time.sleep(0.03)

            # Telefon ma'lumotlarini yaratish
            phone_data = {
                "index": next_index,
                "nomi": name,
                "modeli": model,
                "turi": phone_type,
                "narx": f"${price:.2f}",
                "sana": date,
                "holat": condition,
                "qoshilgan_sana": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }





            # Global ro'yxatga qo'shish
            phones.append(phone_data)
            progress_window.destroy()

            
            try:
                with open("telefon_data.json", "w") as f1:
                    json.dump(phones, f1, indent=4)
                    
                    messagebox.showinfo("✅ Muvaffaqiyatli", 
                        f"🎉 {name} muvaffaqiyatli qo'shildi!\n\n"
                        f"🆔 Indeks: #{next_index:03d}\n"
                        f"💰 Narx: ${price:.2f}")
                    add_window.destroy()
                    
            except NameError:
                print("Nomida xatolik bor")
            
            messagebox.showinfo("bajarildi", "hammasi yaxshi bajarildi:)")
                # Progress animatsiyasini alohida thread da ishga tushirish
        threading.Thread(target=animate_progress, daemon=True).start()
        







    # 🔽 Tugmalar uchun pastki frame
    buttons_frame = ctk.CTkFrame(add_window, fg_color="transparent")
    buttons_frame.pack(side="bottom", pady=15, fill="x")


    saqlash = translations[language]["saqla"]
    # ✅ Saqlash tugmasi
    save_button = ctk.CTkButton(
        buttons_frame,
        text=saqlash,
        command=save_phone,
        font=ctk.CTkFont(size=16, weight="bold"),
        fg_color=("#2ecc71", "#27ae60"),
        hover_color=("#27ae60", "#2ecc71"),
        text_color="white",
        width=150,
        height=50,
        corner_radius=25
    )
    save_button.pack(side="left", padx=20, expand=True)


    bekor = translations[language]["bekor_q"]
    # ❌ Bekor qilish tugmasi
    cancel_button = ctk.CTkButton(
        buttons_frame,
        text=bekor,
        command=add_window.destroy,
        font=ctk.CTkFont(size=16, weight="bold"),
        fg_color=("#e74c3c", "#c0392b"),
        hover_color=("#c0392b", "#e74c3c"),
        text_color="white",
        width=150,
        height=50,
        corner_radius=25
    )
    cancel_button.pack(side="right", padx=20, expand=True)





    # Klaviatura tugmalari bilan boshqaruv
    def on_enter(event):
        save_phone()  # Enter bosilganda saqlash

    def on_escape(event):
        add_window.destroy()  # Escape bosilganda yopish

    add_window.bind('<Return>', on_enter)        # Enter tugmasi
    add_window.bind('<Control-Return>', on_enter)  # Ctrl + Enter
    add_window.bind('<Escape>', on_escape)         # Escape tugmasi


    # Birinchi inputga focus berish
    name_entry.focus()

    # Bugungi sanani avtomatik qo'yish
    set_today_date()




# Telefon o'chirish funksiyasi
def delete_phone():
    if not phones:
        messagebox.showerror(translations[language]["error"], translations[language]["no_phones"])
        return

    # Telefon tanlash oynasi
    delete_window = tk.Toplevel(root_app)
    delete_window.title(translations[language]["delete_phone"])
    delete_window.geometry("600x400")
    delete_window.configure(bg=colors["bg"])
    delete_window.transient(root_app)
    delete_window.grab_set()

    # Formani o'rta joylashtirish
    center_window(delete_window)

    # Sarlavha
    header = tk.Label(delete_window, text=translations[language]["delete_phone"],
                      font=("Arial", 14, "bold"), bg=colors["bg"], fg=colors["fg"])
    header.pack(pady=(15, 10))

    # Qidirish maydoni
    search_frame = tk.Frame(delete_window, bg=colors["bg"])
    search_frame.pack(fill="x", padx=20, pady=10)

    tk.Label(search_frame, text=translations[language]["search"],
             bg=colors["bg"], fg=colors["fg"]).pack(side=tk.LEFT, padx=(0, 5))

    search_var = tk.StringVar()
    search_entry = tk.Entry(search_frame, textvariable=search_var,
                            bg=colors["entry_bg"], fg=colors["entry_fg"], width=40)
    search_entry.pack(side=tk.LEFT, padx=5, fill="x", expand=True)

    # Jadval
    frame = tk.Frame(delete_window, bg=colors["bg"])
    frame.pack(pady=10, padx=20, fill="both", expand=True)

    # Jadval uslubi
    style = ttk.Style(delete_window)
    style.theme_use("clam")
    style.configure("Treeview",
                    background=colors["entry_bg"],
                    foreground=colors["entry_fg"],
                    fieldbackground=colors["entry_bg"],
                    font=('Arial', 10))
    style.configure("Treeview.Heading", font=('Arial', 11, 'bold'))

    columns = ("phone", "model", "price", "date")
    tree = ttk.Treeview(frame, columns=columns, show="headings", selectmode="browse")
    tree.heading("phone", text=translations[language]["phone_name_label"])
    tree.heading("model", text=translations[language]["model_label"])
    tree.heading("price", text=translations[language]["price_label"])
    tree.heading("date", text=translations[language]["date_label"])

    tree.column("phone", anchor="center", width=120)
    tree.column("model", anchor="center", width=120)
    tree.column("price", anchor="center", width=100)
    tree.column("date", anchor="center", width=100)

    # Skroll
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    # Ma'lumotlarni yuklash
    def load_tree_data(search_text=""):
        tree.delete(*tree.get_children())
        for i, phone in enumerate(phones):
            if search_text.lower() in phone["nomi"].lower() or search_text.lower() in phone["modeli"].lower():
                tree.insert("", tk.END, values=(phone["nomi"], phone["modeli"], phone["narx"], phone["sana"]),
                            iid=str(i))

    load_tree_data()

    # Qidirishni yangilash
    def search_phones(event=None):
        search_text = search_var.get()
        load_tree_data(search_text)

    search_var.trace("w", lambda name, index, mode: search_phones())
    search_entry.bind("<Return>", search_phones)

    # Telefon o'chirish funksiyasi
    def confirm_delete():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror(translations[language]["error"],
                                translations[language]["not_found"])
            return

        index = int(selected_item[0])
        phone = phones[index]
        phone_name = f"{phone['nomi']} {phone['modeli']}"

        # O'chirish tasdiqlash
        confirm = messagebox.askyesno(translations[language]["confirm_delete"],
                                    f"{phone_name} - {translations[language]['confirm_delete']}")
        if confirm:
            # O'chirilgan telefonni deleted_phones ga qo'shish
            deleted_phone = phones[index].copy()
            deleted_phone["o'chirilgan_sana"] = datetime.now().strftime("%d/%m/%Y")
            deleted_phones.append(deleted_phone)
            
            # deleted_phones.json ga saqlash
            try:
                with open("deleted_phones.json", "w", encoding="utf-8") as f:
                    json.dump(deleted_phones, f, ensure_ascii=False, indent=4)
            except Exception as e:
                print(f"Xatolik: {e}")

            # Telefonni o'chirish
            del phones[index]
            save_data()
            load_tree_data(search_var.get())
            messagebox.showinfo(translations[language]["success"],
                                f"{phone_name} {translations[language]['deleted']}")

    # Tugmalar
    btn_frame = tk.Frame(delete_window, bg=colors["bg"])
    btn_frame.pack(pady=15, fill="x", padx=20)

    delete_btn = ctk.CTkButton(
        btn_frame,
        text=translations[language]["delete_phone"],
        command=confirm_delete,
        fg_color="#3ec953",
        hover_color="green",
        height=50,
        width=130
    )
    delete_btn.pack(side=tk.LEFT, padx=5)

    close_btn = ctk.CTkButton(
        btn_frame,
        text=translations[language]["close"],
        command=delete_window.destroy,
        fg_color="#FF6B6B",
        hover_color="#FF4B4B",
        height=50,
        width=120
    )
    close_btn.pack(side=tk.LEFT, padx=5)

    # Enter bosilganda o'chirish
    tree.bind('<Double-1>', lambda event: confirm_delete())
    delete_window.bind('<Return>', lambda event: confirm_delete())


# Telefonlarni ko'rish funksiyasi
def edit_phone():
    if not phones:
        messagebox.showerror(translations[language]["error"], translations[language]["no_phones"])
        return

    # Telefon tanlash oynasi
    edit_window = tk.Toplevel(root_app)
    edit_window.title(translations[language]["edit_phone"])
    edit_window.geometry("800x600")
    edit_window.configure(bg=colors["bg"])
    edit_window.transient(root_app)
    edit_window.grab_set()

    # Formani o'rta joylashtirish
    center_window(edit_window)

    # Sarlavha
    header = tk.Label(edit_window, text=translations[language]["edit_phone"],
                      font=("Arial", 14, "bold"), bg=colors["bg"], fg=colors["fg"])
    header.pack(pady=(15, 10))

    # Qidirish maydoni
    search_frame = tk.Frame(edit_window, bg=colors["bg"])
    search_frame.pack(fill="x", padx=20, pady=10)

    tk.Label(search_frame, text=translations[language]["search"],
             bg=colors["bg"], fg=colors["fg"]).pack(side=tk.LEFT, padx=(0, 5))

    search_var = tk.StringVar()
    search_entry = tk.Entry(search_frame, textvariable=search_var,
                            bg=colors["entry_bg"], fg=colors["entry_fg"], width=40)
    search_entry.pack(side=tk.LEFT, padx=5, fill="x", expand=True)

    # Jadval
    frame = tk.Frame(edit_window, bg=colors["bg"])
    frame.pack(pady=10, padx=20, fill="both", expand=True)

    # Jadval uslubi
    style = ttk.Style(edit_window)
    style.theme_use("clam")
    style.configure("Treeview",
                    background=colors["entry_bg"],
                    foreground=colors["entry_fg"],
                    fieldbackground=colors["entry_bg"],
                    font=('Arial', 10))
    style.configure("Treeview.Heading", font=('Arial', 11, 'bold'))

    columns = ("phone", "model", "price", "date")
    tree = ttk.Treeview(frame, columns=columns, show="headings", selectmode="browse")
    tree.heading("phone", text=translations[language]["phone_name_label"])
    tree.heading("model", text=translations[language]["model_label"])
    tree.heading("price", text=translations[language]["price_label"])
    tree.heading("date", text=translations[language]["date_label"])

    tree.column("phone", anchor="center", width=120)
    tree.column("model", anchor="center", width=120)
    tree.column("price", anchor="center", width=100)
    tree.column("date", anchor="center", width=100)

    # Skroll
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    # Ma'lumotlarni yuklash
    def load_tree_data(search_text=""):
        tree.delete(*tree.get_children())
        for i, phone in enumerate(phones):
            if search_text.lower() in phone["nomi"].lower() or search_text.lower() in phone["modeli"].lower():
                tree.insert("", tk.END, values=(phone["nomi"], phone["modeli"], phone["narx"], phone["sana"]),
                            iid=str(i))

    load_tree_data()

    # Qidirishni yangilash
    def search_phones(event=None):
        search_text = search_var.get()
        load_tree_data(search_text)

    search_var.trace("w", lambda name, index, mode: search_phones())
    search_entry.bind("<Return>", search_phones)

    # Telefonni tahrirlash oynasi


    def open_edit_form():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror(translations[language]["error"], translations[language]["not_found"])
            return

        index = int(selected_item[0])
        phone = phones[index]

        form_window = ctk.CTkToplevel(edit_window)
        form_window.title(translations[language]["edit_phone"])
        form_window.geometry("600x600")
        form_window.transient(edit_window)
        form_window.grab_set()

        center_window(form_window)

        ctk.CTkLabel(form_window, text=translations[language]["phone_name_label"], font=("Arial", 16)).pack(pady=10)
        name_entry = ctk.CTkEntry(form_window, width=400, height=35, font=("Arial", 14))
        name_entry.insert(0, phone["nomi"])
        name_entry.pack(pady=5)

        ctk.CTkLabel(form_window, text=translations[language]["model_label"], font=("Arial", 16)).pack(pady=10)
        model_entry = ctk.CTkEntry(form_window, width=400, height=35, font=("Arial", 14))
        model_entry.insert(0, phone["modeli"])
        model_entry.pack(pady=5)

        ctk.CTkLabel(form_window, text=translations[language]["tur"], font=("Arial", 16)).pack(pady=10)
        turi_entry = ctk.CTkEntry(form_window, width=400, height=35, font=("Arial", 14))
        turi_entry.insert(0, phone["turi"])
        turi_entry.pack(pady=5)

        ctk.CTkLabel(form_window, text=translations[language]["price_label"], font=("Arial", 16)).pack(pady=10)
        price_entry = ctk.CTkEntry(form_window, width=400, height=35, font=("Arial", 14))
        price_entry.insert(0, phone["narx"])
        price_entry.pack(pady=5)

        ctk.CTkLabel(form_window, text=translations[language]["holat"], font=("Arial", 16)).pack(pady=10)
        holat_entry = ctk.CTkEntry(form_window, width=400, height=35, font=("Arial", 14))
        holat_entry.insert(0, phone["holat"])
        holat_entry.pack(pady=5)

# save datA FUNKSIYASI 
        def save_data():
            try:
                with open("telefon_data.json", "w", encoding="utf-8") as f:
                    json.dump(phones, f, ensure_ascii=False, indent=4)
                print("Ma'lumotlar muvaffaqiyatli saqlandi.")
            except Exception as e:
                print(f"Saqlashda xatolik: {e}")

        # Saqlash (agar save_data funksiyasi mavjud bo'lmasa)
        try:
            save_data()
        except NameError:
            # Faylga saqlash
            try:
                with open("telefon_data.json", "w", encoding="utf-8") as f:
                    json.dump(phones, f, ensure_ascii=False, indent=4)
            except Exception as e:
                print(f"Saqlashda xatolik: {e}")

            




        def save_changes():
            phone["nomi"] = name_entry.get().strip()
            phone["modeli"] = model_entry.get().strip()
            phone["turi"] = turi_entry.get().strip()
            phone["narx"] = price_entry.get().strip()
            phone["holat"] = holat_entry.get().strip()


            save_data()
            load_tree_data(search_var.get())
            form_window.destroy()


        yangilash = translations[language]["yangilash"]
        # Saqlash tugmasi
        save_btn = ctk.CTkButton(
            form_window, 
            text=yangilash, 
            command=save_changes, 
            fg_color="#4CAF50", 
            hover_color="#45A049",
            font=("Arial", 16),
            width=200,
            height=40
        )
        save_btn.pack(pady=30)







    # Tahrirlash tugmasi
    edit_btn = ctk.CTkButton(edit_window, 
                            text=translations[language]["edit"],
                            command=open_edit_form, 
                            bg_color="green",
                            fg_color=("#3498db", "#2980b9"),
                            hover_color=("#2980b9", "#3498db"),
                            font=ctk.CTkFont(size=14, weight="bold"),
    )
    edit_btn.pack(pady=15)


    
def view_phones():
    # global tree # add this line
    if not phones:
        messagebox.showerror(translations[language]["error"], translations[language]["no_phones"])
        return

    view_window = tk.Toplevel(root_app)
    view_window.title(translations[language]["view_phones"])
    view_window.state("zoomed")
    view_window.configure(bg=colors["bg"])
    view_window.transient(root_app)

    # Oynani o'rta joylashtirish
    center_window(view_window)

    # Sarlavha
    header = tk.Label(view_window, text=translations[language]["view_phones"],
                      font=("Arial", 16, "bold"), bg=colors["bg"], fg=colors["fg"])
    header.pack(pady=(15, 10))

    # Saralash va qidirish paneli
    control_frame = tk.Frame(view_window, bg=colors["bg"])
    control_frame.pack(fill="x", padx=20, pady=10)

    # Qidirish
    search_frame = tk.Frame(control_frame, bg=colors["bg"])
    search_frame.pack(side=tk.LEFT, fill="x", expand=True)

    tk.Label(search_frame, text=translations[language]["search"],
             bg=colors["bg"], fg=colors["fg"]).pack(side=tk.LEFT, padx=(0, 5))

    search_var = tk.StringVar()
    search_entry = tk.Entry(search_frame, textvariable=search_var,
                            bg=colors["entry_bg"], fg=colors["entry_fg"], width=30)
    search_entry.pack(side=tk.LEFT, padx=5)

    # Saralash
    sort_frame = tk.Frame(control_frame, bg=colors["bg"])
    sort_frame.pack(side=tk.RIGHT)

    tk.Label(sort_frame, text=translations[language]["sort_by"],
             bg=colors["bg"], fg=colors["fg"]).pack(side=tk.LEFT, padx=(0, 5))

    sort_options = [
        translations[language]["sort_date"],
        translations[language]["sort_price_asc"],
        translations[language]["sort_price_desc"],
        translations[language]["sort_name"]
    ]

    sort_var = tk.StringVar()
    sort_var.set(sort_options[0])

    sort_combo = ttk.Combobox(sort_frame, textvariable=sort_var, values=sort_options,
                              state="readonly", width=15)
    sort_combo.pack(side=tk.LEFT, padx=5)

    # Jadval
    table_frame = tk.Frame(view_window, bg=colors["bg"])
    table_frame.pack(pady=10, padx=20, fill="both", expand=True)

    # Jadval uslubi
    style = ttk.Style(view_window)
    style.theme_use("clam")

    # Asosiy jadval stili
    style.configure("Treeview",
                    background=colors["entry_bg"],
                    foreground=colors["entry_fg"],
                    fieldbackground=colors["entry_bg"],
                    font=('Arial', 10),
                    rowheight=30,
                    borderwidth=0,
                    relief="flat")

    # Sarlavha stili
    style.configure("Treeview.Heading",
                    font=('Arial', 11, 'bold'),
                    background=colors["button_bg"],
                    foreground=colors["button_fg"])

    # Tanlangan qator stili
    style.map('Treeview',
              background=[('selected', '#FF4444')],
              foreground=[('selected', 'white')])


    # Jadval ustunlari va treeview yaratish
    columns = ("index", "nomi", "modeli", "turi", "narx", "sana", "holat", "qushilgan_sana")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")

    # Jadval sarlavhalari
    tree.heading("index", text="index")
    tree.heading("nomi", text=translations[language]["phone_name_label"])
    tree.heading("modeli", text=translations[language]["model_label"])
    tree.heading("turi", text=translations[language]["tur"])
    tree.heading("narx", text=translations[language]["price_label"])
    tree.heading("sana", text=translations[language]["san"])
    tree.heading("holat", text=translations[language]["hol"])
    tree.heading("qushilgan_sana", text=translations[language]["qushil"])

    # Ustun o'lchamlari va joylashuvi
    tree.column("index", anchor="center", width=50)
    tree.column("nomi", anchor="center", width=100)
    tree.column("modeli", anchor="center", width=100)
    tree.column("turi", anchor="center", width=100)
    tree.column("narx", anchor="center", width=100)
    tree.column("sana", anchor="center", width=50)
    tree.column("holat", anchor="center", width=100)
    tree.column("qushilgan_sana", anchor="center", width=100)

    # Skroll
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    # Qator tanlash uchun rang o'zgartirish (optional)
    def on_select(event):
        for item in tree.get_children():
            tree.item(item, tags=())
        selected_items = tree.selection()
        if selected_items:
            tree.item(selected_items[0], tags=("selected_row",))
    tree.tag_configure("selected_row", background="#FF4444", foreground="white")
    tree.bind('<<TreeviewSelect>>', on_select)

    # ID ustuniga bosilganda usha id tanlangan bo'lsin va select_phone chaqirilsin
    def on_tree_click(event):
        region = tree.identify("region", event.x, event.y)
        if region == "cell":
            col = tree.identify_column(event.x)
            row = tree.identify_row(event.y)
            if col == "#1" and row:  # "#1" is the first column, i.e., "id"
                tree.selection_set(row)
                select_phone(tree)
    tree.bind("<Button-1>", on_tree_click, add="+")  # add="+" to not override other bindings

    # Double click orqali tanlash oynasini ochish
    tree.bind('<Double-1>', lambda e: select_phone(tree))




    # Ma'lumotlarni yuklash
    def load_tree_data(search_text=""):
        tree.delete(*tree.get_children())  # Eski qatorlarni tozalash
        sorted_phones = sort_phones(phones.copy())  # Saralangan ro‘yxat

        for i, phone in enumerate(sorted_phones):
            # Faqat nomi yoki modeli bo‘yicha izlayapmiz
            if search_text.lower() in phone["nomi"].lower() or search_text.lower() in phone["modeli"].lower():
                # Bu telefon phones[] ro‘yxatida qayerda joylashganini topamiz
                try:
                    real_index = phones.index(phone)  # Asl phones[] ro‘yxatdagi index
                except ValueError:
                    continue  # telefon topilmasa, o‘tkazib yuboriladi

                tree.insert(
                    "", tk.END,
                    values=(
                        i + 1,  # Foydalanuvchiga ko‘rsatiladigan tartib raqami
                        phone["nomi"],
                        phone["modeli"],
                        phone["turi"],
                        phone["narx"],
                        phone["sana"],
                        phone["holat"],
                        phone.get("qoshilgan_sana", "")
                    ),
                    iid=str(real_index)  # phones[] ro‘yxatdagi haqiqiy index
                )




    # Telefonlarni saralash
    def clean_price(price):
        """ Narxdan kerakmas belgilarni olib tashlab, faqat son qismi qaytariladi """
        return float(re.sub(r"[^\d.]", "", price))  # Faqat raqam va nuqta qoldiriladi

    def sort_phones(phone_list):
        sort_choice = sort_var.get()

        if sort_choice == translations[language]["sort_date"]:
            return sorted(phone_list, key=lambda x: datetime.strptime(x["sana"], "%d/%m/%Y"), reverse=True)
        elif sort_choice == translations[language]["sort_price_asc"]:
            return sorted(phone_list, key=lambda x: clean_price(x["narx"]), reverse=True)  # Eng kattasidan kichigiga
        elif sort_choice == translations[language]["sort_price_desc"]:
            return sorted(phone_list, key=lambda x: clean_price(x["narx"]))  # Eng kichigidan kattasiga
        elif sort_choice == translations[language]["sort_name"]:
            return sorted(phone_list, key=lambda x: x["nomi"], reverse=True)  # Alfavit bo‘yicha teskari tartib

        return phone_list



    # Qidirishni yangilash
    def search_phones(event=None):
        search_text = search_var.get()
        load_tree_data(search_text)

    search_var.trace("w", lambda name, index, mode: search_phones())
    search_entry.bind("<Return>", search_phones)

    # Saralashni yangilash
    def update_sort(event=None):
        load_tree_data(search_var.get())

    sort_combo.bind("<<ComboboxSelected>>", update_sort)

    
    def select_phone(tree):
        """Tanlangan telefonni qayta ishlash funksiyasi"""
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror(translations[language]["xato"], translations[language]["tel_tanla"])
            return
            
        selected_values = tree.item(selected_item)['values']
        phone_data = {
            "index": selected_values[0],
            "nomi": selected_values[1],
            "modeli": selected_values[2],
            "turi": selected_values[3],
            "narx": selected_values[4],
            "sana": selected_values[5],
            "holat": selected_values[6],
            "qushilgan_sana": selected_values[7]
        }
        
        # Tanlash oynasi 
        select_window = tk.Toplevel()
        select_window.title("Telefon ma'lumotlari")
        select_window.geometry("400x500")
        select_window.configure(bg=colors["bg"])
        center_window(select_window)
        
        # Telefon ma'lumotlari
        info_frame = tk.LabelFrame(select_window, text=translations[language]["about"], 
                                bg=colors["bg"], fg=colors["fg"],
                                font=("Arial", 12, "bold"))
        info_frame.pack(pady=20, padx=20, fill="x")
        
        tk.Label(info_frame, 
                text=f"index: {phone_data['index']}\n"
                    f"Telefon: {phone_data['nomi']}\n"
                    f"IMEI: {phone_data['modeli']}\n"
                    f"Turi: {phone_data['turi']}\n"
                    f"Narx: {phone_data['narx']}\n"
                    f"Sana: {phone_data['sana']}\n"
                    f"Holat: {phone_data['holat']}\n"
                    f"Qushilgan_sana {phone_data['qushilgan_sana']}\n",
                bg=colors["bg"], fg=colors["fg"],
                font=("Arial", 12),
                justify=tk.LEFT).pack(pady=20, padx=20)
                
        # Amallar paneli
        btn_frame = tk.Frame(select_window, bg=colors["bg"])
        btn_frame.pack(pady=20)
        
        # Sotish tugmasi
        ctk.CTkButton(btn_frame,
                    text=translations[language]["sot"],
                    command=lambda: sell_phone(tree), 
                    fg_color="#34eb6b",
                    hover_color="#2bc456",
                    width=120,
                    height=40).pack(side=tk.LEFT, padx=5)
                    
        # Chop etish tugmasi  
        ctk.CTkButton(btn_frame,
                    text=translations[language]["chop_et"],
                    command=lambda: [print_selected_phone(tree), select_window.destroy()],
                    fg_color="#3498db", 
                    hover_color="#2980b9",
                    width=120,
                    height=40).pack(side=tk.LEFT, padx=5)
                    
        # Yopish tugmasi
        ctk.CTkButton(btn_frame,
                    text=translations[language]["yop"],
                    command=select_window.destroy,
                    fg_color="#e74c3c",
                    hover_color="#c0392b", 
                    width=120,
                    height=40).pack(side=tk.LEFT, padx=5)


    # Tugmalar
    btn_frame = tk.Frame(view_window, bg=colors["bg"])
    btn_frame.pack(pady=15, fill="x", padx=20)

    # Sotish tugmasini tree bilan birga uzatish
    sell_btn = ctk.CTkButton(btn_frame, 
            text=translations[language]["sot"], 
            command=lambda: sell_phone(tree),  # tree ni parametr sifatida uzatish
            fg_color="#eb9934",  # sotish rang
            hover_color="#d9eb34",  # Hover ranggi
            text_color="white", 
            width=120,  # Kattaroq tugma
            height=50,
            corner_radius=10,
            font=("Arial", 14, "bold"))
    sell_btn.pack(side=tk.LEFT, padx=5)

    ctk.CTkButton(btn_frame,
            text=translations[language]["sotuvga_ut"],
            command=open_sales_file,
            fg_color="#34eb6b",  # sotish rang
            hover_color="#d9eb34",  # Hover ranggi
            text_color="white", 
            width=120,  # Kattaroq tugma
            height=50,
            corner_radius=10,
            font=("Arial", 14, "bold")).pack(side=tk.LEFT, padx=5)

    btn_frame = tk.Frame(view_window, bg=colors["bg"])
    btn_frame.pack(pady=15, fill="x", padx=20)

    # Telefon tanlash
    tree.bind('<Double-1>', lambda e: select_phone(tree))



    # Enter bosilganda sotish funksiyasi
    def handle_enter(event):
        selected_items = tree.selection()
        if selected_items:
            sell_phone(tree)

    # Tree ga Enter tugmasi bog'lanishi
    tree.bind('<Return>', handle_enter)
    # Tree ga Double-click bog'lanishi
    tree.bind('<Double-1>', handle_enter)

    # Treeview ga fokus berish
    tree.focus_set()




    # Ma'lumotlarni yuklash
    load_tree_data()
    load_sold_phones()

    # Double click orqali tahrirlash
    tree.bind('<Double-1>', lambda event: edit_phone())

    


    def view_phoneis():
        # ...existing code...

        # Tugmalar
        btn_frame = tk.Frame(view_window, bg=colors["bg"])
        btn_frame.pack(pady=15, fill="x", padx=20)

        # Chop etish tugmasi
        print_btn = tk.Button(btn_frame, 
                            text=translations[language]["chop_et"],
                            command=lambda: print_selected_phone(tree),
                            bg=colors["button_bg"],
                            fg=colors["button_fg"],
                            font=("Arial", 10, "bold"))
        print_btn.pack(side=tk.LEFT, padx=5)

        # Yopish tugmasi
        close_btn = tk.Button(btn_frame, 
                            text=translations[language]["close"],
                            command=view_window.destroy, 
                            bg="#FF6B6B",
                            fg="white", 
                            font=("Arial", 10))
        close_btn.pack(side=tk.LEFT, padx=5)

        # Ma'lumotlarni yuklash
        load_tree_data()







# Telefon statistikasi funksiyasi
def show_phone_stats():
    if not phones:
        messagebox.showerror(translations[language]["error"], translations[language]["no_phones"])
        return
        
    def clean_price(price_str):
        """Narxdan faqat raqamlarni ajratib olish"""
        try:
            # Narxdan $ belgisi va bo'sh joylarni olib tashlash
            price = price_str.replace('$', '').replace(' ', '')
            # Faqat raqamlar va nuqtani qoldirish
            return float(''.join(c for c in price if c.isdigit() or c == '.'))
        except:
            return 0.0

    stats_window = tk.Toplevel(root_app)
    stats_window.title(translations[language]["phone_stats"])
    stats_window.geometry("500x400")
    stats_window.configure(bg=colors["bg"])
    stats_window.transient(root_app)
    stats_window.grab_set()

    center_window(stats_window)

    header = tk.Label(stats_window, text=translations[language]["phone_stats"],
                     font=("Arial", 16, "bold"), bg=colors["bg"], fg=colors["fg"])
    header.pack(pady=(15, 20))

    stats_frame = tk.Frame(stats_window, bg=colors["bg"], bd=1, relief=tk.GROOVE)
    stats_frame.pack(pady=10, padx=20, fill="x")

    # Statistika hisoblash
    try:
        total_phones = len(phones)
        
        # Narxlarni tozalash va hisoblash
        prices = [clean_price(phone["narx"]) for phone in phones]
        prices = [p for p in prices if p > 0]  # Nol bo'lmagan narxlar
        
        if prices:
            avg_price = sum(prices) / len(prices)
            max_price = max(prices)
            min_price = min(prices)
            total_price = sum(prices)  # Jami narx
            
            # Eng qimmat va arzon telefonlarni topish
            most_expensive = next(phone for phone in phones 
                                if clean_price(phone["narx"]) == max_price)
            cheapest = next(phone for phone in phones 
                          if clean_price(phone["narx"]) == min_price)
        else:
            raise ValueError("Narxlar topilmadi")
            
    except Exception as e:
        print(f"Xato: {e}")  # Debug uchun
        total_phones = len(phones)
        avg_price = 0
        total_price = 0  # Jami narx
        most_expensive = {"nomi": "N/A", "modeli": "N/A", "narx": "0"}
        cheapest = {"nomi": "N/A", "modeli": "N/A", "narx": "0"}

    # Statistika ma'lumotlari
    stats = [
        (translations[language]["total_phones"], f"{total_phones} dona"),
        (translations[language]["avg_price"], f"{avg_price:.2f} $"),
        (translations[language]["highest_price"], 
         f"{most_expensive['nomi']} - {most_expensive['narx']}"),
        (translations[language]["lowest_price"], 
         f"{cheapest['nomi']} - {cheapest['narx']}"),
        ("Jami narx:", f"{total_price:.2f} $")  # Yangi qator
    ]

    # Ma'lumotlarni ko'rsatish
    for i, (label, value) in enumerate(stats):
        tk.Label(stats_frame, text=label, bg=colors["bg"], fg=colors["fg"],
                font=("Arial", 11, "bold"), anchor="w").grid(row=i, column=0,
                sticky="w", padx=20, pady=10)
        tk.Label(stats_frame, text=value, bg=colors["bg"], fg=colors["fg"],
                font=("Arial", 11), anchor="e").grid(row=i, column=1,
                sticky="e", padx=20, pady=10)

    # Tugmalar
    btn_frame = tk.Frame(stats_window, bg=colors["bg"])
    btn_frame.pack(pady=20)






def center_window(window):
    """Oynani ekran markaziga joylashtirish"""
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))






def show_sales_summary():
    """Sotilgan telefonlar statistikasini ko'rsatish"""
    if not sold_phones:
        messagebox.showerror("Xatolik", "Sotilgan telefonlar mavjud emas!")
        return

    summary_window = tk.Toplevel(root_app)
    summary_window.title(translations[language]["savdo_st"])
    summary_window.geometry("800x600")
    summary_window.configure(bg=colors["bg"])
    center_window(summary_window)

    # Sarlavha
    header = tk.Label(summary_window, text=translations[language]["savdo_st"],
                     font=("Arial", 16, "bold"), bg=colors["bg"], fg=colors["fg"])
    header.pack(pady=(15, 10))

    # Jadval
    table_frame = tk.Frame(summary_window, bg=colors["bg"])
    table_frame.pack(pady=10, padx=20, fill="both", expand=True)

    columns = ("id", "phone", "model", "price", "date")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")
    
    tree.heading("id", text="ID")
    tree.heading("phone", text=translations[language]["phone_name_label"])
    tree.heading("model", text="IMEI")
    tree.heading("price", text=translations[language]["price_label"])
    tree.heading("date", text=translations[language]["sotilgan_san"])

    tree.column("id", width=50, anchor="center")
    tree.column("phone", width=150, anchor="center")
    tree.column("model", width=150, anchor="center")
    tree.column("price", width=100, anchor="center")
    tree.column("date", width=100, anchor="center")

    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    # Statistika paneli
    stats_frame = tk.Frame(summary_window, bg=colors["bg"])
    stats_frame.pack(fill="x", padx=20, pady=10)

    # Statistika hisoblash funksiyasi
    def calculate_stats(days=None):
        """Tanlangan davr uchun statistikani hisoblash"""
        total_sales = 0
        filtered_phones = []
        
        if days is None:
            filtered_phones = sold_phones
        else:
            cutoff_date = datetime.now() - timedelta(days=days-1)
            for phone in sold_phones:
                sale_date = datetime.strptime(phone["sana"], "%d/%m/%Y")
                if sale_date.date() >= cutoff_date.date():
                    filtered_phones.append(phone)

        # Jadvalni yangilash
        tree.delete(*tree.get_children())
        for i, phone in enumerate(filtered_phones, 1):
            tree.insert("", "end", values=(
                i,
                phone["nomi"],
                phone["modeli"],
                phone["narx"],
                phone["sana"]
            ))
            try:
                price = float(phone["narx"].replace("$", "").strip())
                total_sales += price
            except:
                continue

        count = len(filtered_phones)
        avg_sale = total_sales/count if count > 0 else 0
        
        period = "Barcha" if days is None else f"Oxirgi {days} kunlik"
        stats_text = f"{period} statistika:\n"
        stats_text += f"Sotilgan telefonlar: {count} dona\n"
        stats_text += f"Umumiy savdo: ${total_sales:.2f}\n"
        stats_text += f"O'rtacha savdo: ${avg_sale:.2f}"
        
        stats_label.config(text=stats_text)

    # Davr tanlash tugmalari
    buttons_frame = tk.Frame(stats_frame, bg=colors["bg"])
    buttons_frame.pack(fill="x", pady=5)

    periods = [
        ("Bugun", 1),
        ("Hammasi", None)
    ]

    for text, days in periods:
        btn = tk.Button(buttons_frame,
                       text=text,
                       command=lambda d=days: calculate_stats(d),
                       bg=colors["button_bg"],
                       fg=colors["button_fg"],
                       font=("Arial", 10))
        btn.pack(side=tk.LEFT, padx=5)

    stats_label = tk.Label(stats_frame,
                          text=translations[language]["davr"],
                          bg=colors["bg"],
                          fg=colors["fg"],
                          font=("Arial", 12),
                          justify=tk.LEFT)
    stats_label.pack(pady=10)

    # Yopish tugmasi
    close_btn = tk.Button(summary_window,
                         text=translations[language]["yop"],
                         command=summary_window.destroy,
                         bg="#FF6B6B",
                         fg="white",
                         font=("Arial", 10))
    close_btn.pack(pady=15)

    # Dastlabki statistikani ko'rsatish
    calculate_stats(None)

########################################
########################################
########################################




def sell_phone(tree=None):
    """Tanlangan telefonni sotish funksiyasi - tuzatilgan versiya"""
    global sold_phones, phones
    
    if tree is None:
        messagebox.showerror(translations[language]["xato"], translations[language]["tel_jad"])
        return

    def get_selected_phone():
        try:
            selected_items = tree.selection()
            if not selected_items:
                messagebox.showerror(translations[language]["xato"], translations[language]["tel_tanla"])
                return None, None, None

            selected_item = selected_items[0]  # Bu — iid, ya'ni phones[] dagi index
            index = int(selected_item)

            if index < 0 or index >= len(phones):
                messagebox.showerror(translations[language]["xato"], translations[language]["tel_jad_yuq"])
                return None, None, None

            phone = phones[index]

            # Narxni float ko‘rinishga keltirish
            price_str = str(phone.get('narx', '0'))
            cleaned_price = re.sub(r"[^\d.]", "", price_str)
            if not cleaned_price:
                raise ValueError("Narx formati noto‘g‘ri")

            original_price = float(cleaned_price)

            return phone, original_price, index

        except Exception as e:
            messagebox.showerror("Xatolik", f"Kutilmagan xatolik: {str(e)}")
            return None, None, None



    # Telefon ma'lumotlarini olish
    phone_data, original_price, phone_index = get_selected_phone()
    if phone_data is None:
        return

    # Zamonaviy sotish oynasi
    sell_window = ctk.CTkToplevel()
    sell_window.title(translations[language]["sell_tel"])
    sell_window.geometry("800x950")
    sell_window.configure(fg_color=("#f0f0f0", "#1a1a1a"))
    
    # Oynani markazlashtirish
    sell_window.update_idletasks()
    x = (sell_window.winfo_screenwidth() // 2) - (800 // 2)
    y = (sell_window.winfo_screenheight() // 2) - (1000 // 2)
    sell_window.geometry(f"800x950+{x}+{y}")
    
    # Oynani modal qilish
    sell_window.transient()
    sell_window.grab_set()
    sell_window.focus_set()

    # Asosiy sarlavha
    title_label = ctk.CTkLabel(
        sell_window,
        text=translations[language]["sell_tel"],
        font=ctk.CTkFont(size=28, weight="bold"),
        text_color=("#2c3e50", "#ecf0f1")
    )
    title_label.pack(pady=(20, 30))

    # Telefon ma'lumotlari frame
    info_frame = ctk.CTkFrame(sell_window)
    info_frame.pack(pady=(0, 20), padx=30, fill="x")

    info_title = ctk.CTkLabel(
        info_frame,
        text=translations[language]["tel_info"],
        font=ctk.CTkFont(size=18, weight="bold"),
        text_color=("#34495e", "#bdc3c7")
    )
    info_title.pack(pady=(15, 10))

    # Telefon tafsilotlari
    index = phone_data.get('index', "Noma'lum")
    nomi = phone_data.get('nomi', "Noma'lum")
    modeli = phone_data.get('modeli', "Noma'lum")
    holat = phone_data.get('holat', "Noma'lum")

    details_text = (
        f"// index {index}\n"
        f"📱 Telefon: {nomi}\n"
        f"🔢 IMEI: {modeli}\n"
        f"📋 Holati: {holat}\n"
        f"💰 Asl Narx: ${original_price:.2f}"
    )



    details_label = ctk.CTkLabel(
        info_frame,
        text=details_text,
        font=ctk.CTkFont(size=14),
        justify="left",
        text_color=("#2c3e50", "#ecf0f1")
    )
    details_label.pack(pady=(0, 15), padx=20)

    # Narx ma'lumotlari frame
    price_frame = ctk.CTkFrame(sell_window)
    price_frame.pack(pady=(0, 20), padx=30, fill="x")

    price_title = ctk.CTkLabel(
        price_frame,
        text=translations[language]["narx_info"],
        font=ctk.CTkFont(size=18, weight="bold"),
        text_color=("#34495e", "#bdc3c7")
    )
    price_title.pack(pady=(15, 10))

    # Sotish narxi input
    price_label = ctk.CTkLabel(
        price_frame,
        text=translations[language]["sell_info"],
        font=ctk.CTkFont(size=14),
        text_color=("#2c3e50", "#ecf0f1")
    )
    price_label.pack(pady=(5, 5))

    price_entry = ctk.CTkEntry(
        price_frame,
        placeholder_text=translations[language]["sel_entry"],
        font=ctk.CTkFont(size=14),
        height=40,
        width=200
    )
    price_entry.insert(0, str(original_price))
    price_entry.pack(pady=(0, 10))

    # Foyda/zarar ko'rsatkichi
    profit_label = ctk.CTkLabel(
        price_frame,
        text=translations[language]["foyda/zarar"],
        font=ctk.CTkFont(size=16, weight="bold"),
        text_color=("#27ae60", "#2ecc71")
    )
    profit_label.pack(pady=(0, 15))

    def update_profit(*args):
        try:
            selling_price = float(price_entry.get().replace('$', '').strip())
            profit = selling_price - original_price
            
            if profit >= 0:
                color = ("#27ae60", "#2ecc71")  # Yashil
                emoji = "📈"
            else:
                color = ("#e74c3c", "#c0392b")  # Qizil
                emoji = "📉"
            
            profit_label.configure(
                text=f"{emoji} Foyda/Zarar: ${profit:.2f}",
                text_color=color
            )
        except ValueError:
            profit_label.configure(
                text=translations[language]["noturi"],
                text_color=("#e74c3c", "#c0392b")
            )

    # Narx o'zgarganda foyda/zaralni yangilash
    price_entry.bind('<KeyRelease>', update_profit)

    # Mijoz ma'lumotlari frame
    customer_frame = ctk.CTkFrame(sell_window)
    customer_frame.pack(pady=(0, 20), padx=30, fill="x")

    customer_title = ctk.CTkLabel(
        customer_frame,
        text="👤 Mijoz Ma'lumotlari",
        font=ctk.CTkFont(size=18, weight="bold"),
        text_color=("#34495e", "#bdc3c7")
    )
    customer_title.pack(pady=(15, 15))

    # Mijoz ismi
    name_label = ctk.CTkLabel(
        customer_frame,
        text=translations[language]["mj"],
        font=ctk.CTkFont(size=14),
        text_color=("#2c3e50", "#ecf0f1")
    )
    name_label.pack(pady=(5, 5))

    customer_name = ctk.CTkEntry(
        customer_frame,
        placeholder_text=translations[language]["mj_name"],
        font=ctk.CTkFont(size=14),
        height=40,
        width=300
    )
    customer_name.pack(pady=(0, 10))

    # Mijoz telefoni
    phone_label = ctk.CTkLabel(
        customer_frame,
        text=translations[language]["mj_tel"],
        font=ctk.CTkFont(size=14),
        text_color=("#2c3e50", "#ecf0f1")
    )
    phone_label.pack(pady=(5, 5))

    customer_phone = ctk.CTkEntry(
        customer_frame,
        placeholder_text="+998 90 123 45 67",
        font=ctk.CTkFont(size=14),
        height=40,
        width=300
    )
    customer_phone.pack(pady=(0, 15))

    def confirm_sell():
        try:
            # Narxni tekshirish
            sell_price_str = price_entry.get().replace('$', '').strip()
            if not sell_price_str:
                messagebox.showerror(translations[language]["xato"], translations[language]["sel_narx"])
                return
                
            sell_price = float(sell_price_str)
            if sell_price <= 0:
                messagebox.showerror(translations[language]["xato"], translations[language]["sel_0"])
                return
            
            # Mijoz ma'lumotlarini tekshirish
            customer_info = {
                "name": customer_name.get().strip(),
                "phone": customer_phone.get().strip()
            }
            
            if not customer_info["name"]:
                messagebox.showerror(translations[language]["xato"], translations[language]["mj_name"])
                customer_name.focus()
                return
                
            if not customer_info["phone"]:
                messagebox.showerror(translations[language]["xato"], translations[language]["ero"])
                customer_phone.focus()
                return

            profit = sell_price - original_price
            
            # Sotish ma'lumotlarini yaratish
            sale_record = {
                "nomi": phone_data.get('nomi', 'Noma\'lum'),
                "modeli": phone_data.get('modeli', 'Noma\'lum'),
                "asl_narx": f"${original_price:.2f}",
                "sotish_narx": f"${sell_price:.2f}",
                "foyda": f"${profit:.2f}",
                "sotilgan_sana": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "mijoz_ismi": customer_info["name"],
                "mijoz_telefon": customer_info["phone"]
            }

            # Tasdiqlash oynasi
            profit_emoji = "📈" if profit >= 0 else "📉"
            profit_color = "🟢" if profit >= 0 else "🔴"
            


            "📋 Telefon Ma'lumotlari:"
            nomi = {phone_data.get('nomi', 'Noma\'lum')}
            imai = {phone_data.get('modeli', 'Noma\'lum')}

            confirm_text = (
                "📱 SOTISH TASDIQLASH \n"

                f"• Nomi: {nomi}\n"
                f"• IMEI: {imai}\n"

                "💰 Narx Ma'lumotlari:\n"
                # org_price = f"{original_price:.2f}"
                # seel_price = {sell_price:.2f}

                f"• Asl narx: ${original_price:.2f}"
                f"• Sotish narxi: ${sell_price:.2f}"
                f"• {profit_emoji} Foyda/Zarar: ${profit:.2f} {profit_color}"

                "👤 Mijoz Ma'lumotlari:\n"
                f"• Ismi: {customer_info['name']}"
                f"• Telefoni: {customer_info['phone']}"

                f"📅 Sana: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"

                "❓ Sotishni tasdiqlaysizmi?"
            )

            if messagebox.askyesno(translations[language]["tasdiq"], confirm_text):
                try:
                    # sotish_file.json ga saqlash
                    try:
                        with open("sotish_file.json", 'r', encoding='utf-8') as f:
                            sales_data = json.load(f)
                    except (FileNotFoundError, json.JSONDecodeError):
                        sales_data = []
                    
                    sales_data.append(sale_record)
                    
                    with open("sotish_file.json", 'w', encoding='utf-8') as f:
                        json.dump(sales_data, f, ensure_ascii=False, indent=4)

                    # Telefonni ro'yxatdan olib tashlash
                    phones.pop(phone_index)
                    sold_phones.append(sale_record)
                    
                    # Ma'lumotlarni saqlash (agar funktsiyalar mavjud bo'lsa)
                    try:
                        save_data()
                        save_sold_phones()
                    except NameError:
                        pass  # Funktsiyalar mavjud emas
                    
                    messagebox.showinfo("✅ Muvaffaqiyatli", 
                                      f"🎉 {phone_data.get('nomi', 'Telefon')} muvaffaqiyatli sotildi!\n\n"
                                      f"💰 Foyda: ${profit:.2f}")
                    sell_window.destroy()

                except Exception as e:
                    messagebox.showerror(translations[language]["xato"], f"Saqlashda xatolik yuz berdi:\n{str(e)}")

        except ValueError:
            messagebox.showerror(translations[language]["xato"], translations[language]["neto"])
        except Exception as e:
            messagebox.showerror(translations[language]["xato"], f"Kutilmagan xatolik:\n{str(e)}")

    # Tugmalar frame
    btn_frame = ctk.CTkFrame(sell_window, fg_color="transparent")
    btn_frame.pack(pady=20)

    # Sotish tugmasi
    sell_btn = ctk.CTkButton(
        btn_frame,
        text=translations[language]["sot"],
        command=confirm_sell,
        font=ctk.CTkFont(size=16, weight="bold"),
        fg_color=("#2ecc71", "#27ae60"),
        hover_color=("#27ae60", "#2ecc71"),
        text_color="white",
        width=150,
        height=45,
        corner_radius=25
    )
    sell_btn.pack(side=tk.LEFT, padx=10)

    # Bekor qilish tugmasi
    cancel_btn = ctk.CTkButton(
        btn_frame,
        text=translations[language]["bekor_q"],
        command=sell_window.destroy,
        font=ctk.CTkFont(size=16, weight="bold"),
        fg_color=("#e74c3c", "#c0392b"),
        hover_color=("#c0392b", "#e74c3c"),
        text_color="white",
        width=150,
        height=45,
        corner_radius=25
    )
    cancel_btn.pack(side=tk.LEFT, padx=10)

    # Klaviatura shortcutlari
    def on_enter(event):
        confirm_sell()
    
    def on_escape(event):
        sell_window.destroy()
    
    sell_window.bind('<Return>', on_enter)
    sell_window.bind('<Return>', on_enter)  # To'g'ri  # Numpad Enter
    sell_window.bind('<Escape>', on_escape)
    
    # Birinchi input ga focus berish
    customer_name.focus()
    
    # Dastlabki foyda/zarar hisobini yangilash
    update_profit()

# Yordamchi funksiya - oynani markazlashtirish
def center_window(window, width=600, height=750):
    """Oynani ekran markaziga joylashtirish"""
    window.update_idletasks()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

# Test uchun ma'lumotlar (haqiqiy kodda bu global o'zgaruvchilar bo'lishi kerak)
phones = []
sold_phones = []

def save_data():
    """Ma'lumotlarni saqlash funksiyasi (haqiqiy kodda bo'lishi kerak)"""
    pass








# Sotilgan telefonlarni faylga saqlash funksiyasi
def save_sold_phones():
    try:
        with open("sold_phones.json", 'w', encoding='utf-8') as f:
            json.dump(sold_phones, f, ensure_ascii=False, indent=4)
    except Exception as e:
        messagebox.showerror(translations[language]["error"], str(e))

# Sotilgan telefonlarni fayldan yuklash funksiyasi
def load_sold_phones():
    global sold_phones
    try:
        if os.path.exists("sold_phones.json"):
            with open("sold_phones.json", 'r', encoding='utf-8') as f:
                sold_phones = json.load(f)
        else:
            sold_phones = []
    except Exception as e:
        messagebox.showerror(translations[language]["error"], str(e))

# sotilgan telefonlar faylini ochish funksiyasi
def open_sales_file():
    """Sotish faylini ochish"""
    try:
        subprocess.Popen([sys.executable, "sotish_file.py"])
    except FileNotFoundError:
        messagebox.showerror(translations[language]["xato"], "sotish_file.py fayli topilmadi!")
    except Exception as e:
        messagebox.showerror(translations[language]["xato"], f"Xatolik yuz berdi: {str(e)}")


# eslatmalar faylini ochish funksiyasi
def open_eslatma_file():
    """Sotish faylini ochish"""
    try:
        subprocess.Popen([sys.executable, "notebook.py"])
    except FileNotFoundError:
        messagebox.showerror(translations[language]["xato"], "sotish_file.py fayli topilmadi!")
    except Exception as e:
        messagebox.showerror(translations[language]["xato"], f"Xatolik yuz berdi: {str(e)}")


# Dastur haqida ma'lumot
def show_about():
    about_window = tk.Toplevel(root_app)
    about_window.title(translations[language]["about"])
    about_window.geometry("400x300")
    about_window.configure(bg=colors["bg"])
    about_window.transient(root_app)
    about_window.grab_set()

    # Oynani o'rta joylashtirish
    center_window(about_window)

    # Sarlavha
    header = tk.Label(about_window, text=translations[language]["about"],
                      font=("Arial", 16, "bold"), bg=colors["bg"], fg=colors["fg"])
    header.pack(pady=(20, 15))

    # Ma'lumot
    about_text = tk.Label(about_window, text=translations[language]["about_text"],
                          bg=colors["bg"], fg=colors["fg"], justify=tk.CENTER,
                          font=("Arial", 11))
    about_text.pack(pady=10)

    # Yopish tugmasi
    close_btn = tk.Button(about_window, text=translations[language]["close"],
                          bg=colors["button_bg"], fg=colors["button_fg"],
                          font=("Arial", 10), command=about_window.destroy)
    close_btn.pack(pady=20)

def view_all_history():
    """Sotilgan va o'chirilgan telefonlar tarixini ko'rish funksiyasi"""
    try:
        # Ma'lumotlarni yuklash
        global sold_phones, deleted_phones
        deleted_phones = []
        if os.path.exists("deleted_phones.json"):
            try:
                with open("deleted_phones.json", "r", encoding="utf-8") as f:
                    deleted_phones = json.load(f)
            except Exception:
                deleted_phones = []

        if not sold_phones and not deleted_phones:
            messagebox.showerror(translations[language]["xato"], translations[language]["mavj"])
            return

        # Asosiy oyna
        history_window = tk.Toplevel(root_app)
        history_window.title(translations[language]["tel_istory"])
        history_window.state("zoomed")
        history_window.configure(bg=colors["bg"])
        history_window.transient(root_app)
        center_window(history_window)

        # Sarlavha
        header = tk.Label(history_window, text=translations[language]["tel_istory"],
                        font=("Arial", 16, "bold"), bg=colors["bg"], fg=colors["fg"])
        header.pack(pady=(15, 10))

        # Qidiruv paneli
        search_frame = tk.Frame(history_window, bg=colors["bg"])
        search_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(search_frame, text=translations[language]["qdr"],
                bg=colors["bg"], fg=colors["fg"]).pack(side=tk.LEFT, padx=(0, 5))

        search_var = tk.StringVar()
        search_entry = ctk.CTkEntry(search_frame, 
                                  textvariable=search_var,
                                  width=300,
                                  height=35,
                                  placeholder_text=translations[language]["qdr_matn"])
        search_entry.pack(side=tk.LEFT, padx=5)

        # Jadval
        table_frame = tk.Frame(history_window, bg=colors["bg"])
        table_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Jadval ustunlari
        columns = (
            "id", "nomi", "modeli", "asl_narx", "sotish_narx", 
            "foyda", "mijoz_ismi", "mijoz_telefon", "holat", "sana"
        )
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")

        # Ustun sozlamalari
        column_settings = {
            "id": ("ID", 50),
            "nomi": ("Telefon nomi", 150),
            "modeli": ("IMEI", 150),
            "asl_narx": ("Asl narx", 90),
            "sotish_narx": ("Sotish narxi", 90),
            "foyda": ("Foyda", 80),
            "mijoz_ismi": ("Mijoz ismi", 120),
            "mijoz_telefon": ("Mijoz telefoni", 120),
            "holat": ("Holati", 90),
            "sana": ("Sana", 100)
        }

        for col, (heading, width) in column_settings.items():
            tree.heading(col, text=heading)
            tree.column(col, anchor="center", width=width)

        # Skroll
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(side="left", fill="both", expand=True)

        # Ma'lumotlarni saqlash
        all_history = []

        def load_data():
            # Sotilgan telefonlar
            for phone in sold_phones:
                all_history.append({
                    "nomi": phone.get("nomi", ""),
                    "modeli": phone.get("modeli", ""),
                    "asl_narx": phone.get("asl_narx", ""),
                    "sotish_narx": phone.get("sotish_narx", ""),
                    "foyda": phone.get("foyda", ""),
                    "mijoz_ismi": phone.get("mijoz_ismi", ""),
                    "mijoz_telefon": phone.get("mijoz_telefon", ""),
                    "holat": "Sotilgan",
                    "sana": phone.get("sotilgan_sana", phone.get("sana", ""))
                })

            # O'chirilgan telefonlar
            for phone in deleted_phones:
                all_history.append({
                    "nomi": phone.get("nomi", ""),
                    "modeli": phone.get("modeli", ""),
                    "asl_narx": phone.get("narx", "****"),
                    "sotish_narx": "****",
                    "foyda": "****",
                    "mijoz_ismi": "****",
                    "mijoz_telefon": "****",
                    "holat": "O'chirilgan",
                    "sana": phone.get("sana", "")
                })

        def display_data(data_list, search_text=""):
            tree.delete(*tree.get_children())
            for i, phone in enumerate(data_list, 1):
                if search_text.lower() in str(phone).lower():
                    values = [
                        i,
                        phone["nomi"],
                        phone["modeli"],
                        "****",  # asl_narx
                        "****",  # sotish_narx
                        "****",  # foyda
                        phone["mijoz_ismi"],
                        phone["mijoz_telefon"],
                        phone["holat"],
                        phone["sana"]
                    ]
                    tree.insert("", tk.END, values=values, tags=(phone["holat"],))

        def show_price(event):
            region = tree.identify("region", event.x, event.y)
            if region == "cell":
                col = tree.identify_column(event.x)
                row = tree.identify_row(event.y)
                
                if col in ("#4", "#5", "#6"):  # Narx ustunlari
                    code = simpledialog.askstring(
                        "Kod", 
                        "Narxni ko'rish uchun kodni kiriting:", 
                        show="*",
                        parent=history_window
                    )
                    
                    if code == "0630":
                        item = tree.selection()[0]
                        idx = tree.index(item)
                        if idx < len(all_history):
                            phone = all_history[idx]
                            col_map = {"#4": "asl_narx", "#5": "sotish_narx", "#6": "foyda"}
                            value = phone.get(col_map[col], "Ma'lumot mavjud emas")
                            messagebox.showinfo("Narx", f"Qiymat: {value}", parent=history_window)
                    elif code is not None:
                        messagebox.showerror("Xatolik", "Kod noto'g'ri!")

        # Rangli belgilash
        tree.tag_configure("Sotilgan", background="#90EE90")
        tree.tag_configure("O'chirilgan", background="#FFB6C1")

        # Eventlarni bog'lash
        tree.bind("<Button-1>", show_price)
        search_var.trace("w", lambda *args: display_data(all_history, search_var.get()))

        # Statistika
        def update_stats():
            total_sold = sum(float(p.get("sotish_narx", "0").replace("$", "").strip() or 0) 
                           for p in sold_phones)
            total_deleted = sum(float(p.get("narx", "0").replace("$", "").strip() or 0) 
                              for p in deleted_phones)


            total = translations[language]["total"]
            sel = translations[language]["sel"]
            uchrl = translations[language]["uchrl"]
            umumiy = translations[language]["umumiy"]
            stats_text = (
                f"{total}: {len(all_history)} dona | "
                f"{sel}: {len(sold_phones)} dona (${total_sold:.2f}) | "
                f"{uchrl}: {len(deleted_phones)} dona (${total_deleted:.2f}) | "
                f"{umumiy}: ${(total_sold + total_deleted):.2f}"
            )
            
            stats_label.config(text=stats_text)

        stats_frame = tk.Frame(history_window, bg=colors["bg"])
        stats_frame.pack(pady=10, fill="x", padx=20)
        
        stats_label = tk.Label(stats_frame, 
                             bg=colors["bg"], 
                             fg=colors["fg"],
                             font=("Arial", 12))
        stats_label.pack(pady=5)

        # Yopish tugmasi
        close_btn = ctk.CTkButton(
            history_window,
            text=translations[language]["yop"],
            command=history_window.destroy,
            fg_color="#FF6B6B",
            hover_color="#FF4B4B",
            height=40,
            width=120
        )
        close_btn.pack(pady=50)

        

        # Ma'lumotlarni yuklash va ko'rsatish
        load_data()
        display_data(all_history)
        update_stats()
    except Exception as e:
        messagebox("Xatolik", f"Kutilmagan xatolik yuz berdi: {str(e)}")
        # print(f"Xatolik tafsilotlari: {e}")  # Debug uchun
    

        



def print_phone_details(phone_data):
    """
    Print phone details on standard receipt paper (80mm x 40mm)
    """
    try:
        # Get default printer
        printer_name = win32print.GetDefaultPrinter()
        
        # Create device context
        hprinter = win32print.OpenPrinter(printer_name)
        printer_info = win32print.GetPrinter(hprinter, 2)
        
        # Create DC
        hdc = win32ui.CreateDC()
        hdc.CreatePrinterDC(printer_name)
        
        # Start document
        hdc.StartDoc('Telefon Cheki')
        hdc.StartPage()
        
        # Set fonts
        font_name = "Arial"
        font_size = 50  # Increased font size
        title_font = win32ui.CreateFont({
            "name": font_name,
            "height": font_size + 15,  # Larger size for title
            "weight": 1500
        })
        font_bold = win32ui.CreateFont({
            "name": font_name,
            "height": font_size,
            "weight": 1500
        })
        font_normal = win32ui.CreateFont({
            "name": font_name,
            "height": font_size,
            "weight": 1500
        })
        
        # Page settings
        margin_left = 200
        margin_top = 500
        line_height = font_size + 25
        col_width = 250  # Width between label and value
        
        # Current position
        x = margin_left
        y = margin_top
        
        # Print header with larger font
        hdc.SelectObject(title_font)
        hdc.TextOut(x, y, "TELEFON MA'LUMOTLARI")
        y += line_height * 2
        
        # Print date and time
        hdc.SelectObject(font_normal)
        current_date = datetime.now().strftime("%d/%m/%Y %H:%M")
        hdc.TextOut(x, y, f"Sana: {current_date}")
        y += line_height * 2
        
        # Print separator
        hdc.TextOut(x, y, "=" * 40)
        y += line_height
        
        # Print phone details with better spacing
        details = [
            ("Telefon nomi:", phone_data["nomi"]),
            ("IMEI:", phone_data["modeli"]),
            ("Narxi:", phone_data["narx"]),
            ("Qo'shilgan sana:", phone_data["sana"])
        ]
        
        for label, value in details:
            # Print label in bold
            hdc.SelectObject(font_bold)
            hdc.TextOut(x, y, label)
            
            # Print value in normal font
            hdc.SelectObject(font_normal)
            hdc.TextOut(x + col_width, y, str(value))
            y += line_height
        
        # Add footer with separators
        y += line_height
        hdc.SelectObject(font_normal)
        hdc.TextOut(x, y, "=" * 40)
        y += line_height
        
        # Add store info
        store_info = "Telefon Do'koni"
        hdc.SelectObject(font_bold)
        text_width = hdc.GetTextExtent(store_info)[0]
        x_centered = x + (400 - text_width) // 2  # Center text
        hdc.TextOut(x_centered, y, store_info)
        
        y += line_height
        hdc.SelectObject(font_normal)
        copyright_text = "© xaridingiz uchun rahmat!"
        text_width = hdc.GetTextExtent(copyright_text)[0]
        x_centered = x + (400 - text_width) // 2  # Center text
        hdc.TextOut(x_centered, y, copyright_text)
        
        # Finish printing
        hdc.EndPage()
        hdc.EndDoc()
        
        # Cleanup
        hdc.DeleteDC()
        win32print.ClosePrinter(hprinter)
        
        messagebox.showinfo("Muvaffaqiyatli", "Chek muvaffaqiyatli chop etildi!")
        
    except win32print.error as we:
        messagebox.showerror("Printer xatosi", 
                           f"Printerda xatolik: {str(we)}\nPrinter ulangan va yoqilganligini tekshiring")
    except Exception as e:
        messagebox.showerror("Xatolik", 
                           f"Chop etishda kutilmagan xatolik yuz berdi: {str(e)}")

def print_selected_phone(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Xatolik", "Iltimos, telefon tanlang!")
        return
        
    # Get selected phone data
    selected_values = tree.item(selected_item)['values']
    phone_data = {
        "nomi": selected_values[1],
        "modeli": selected_values[2],
        "narx": selected_values[3],
        "sana": selected_values[4]
    }
    
    # Print phone details
    print_phone_details(phone_data)
    def redirect_to_print_file():
        print2.view_print_screen()

    redirect_to_print_file()
def view_print_screen():
    
    # return print_file.view_print_screen()
    
    if not phones:
        messagebox.showerror(translations[language]["error"], "Telefonlar mavjud emas!")
        return

    print_window = tk.Toplevel(root_app)
    print_window.title("Chop etish bo'limi")
    print_window.state("zoomed")
    print_window.configure(bg=colors["bg"])
    center_window(print_window)

    # Sarlavha
    header = tk.Label(print_window, text="🖨️ Telefonni chop etish",
                      font=("Arial", 16, "bold"), bg=colors["bg"], fg=colors["fg"])
    header.pack(pady=(15, 10))

    # Jadval
    table_frame = tk.Frame(print_window, bg=colors["bg"])
    table_frame.pack(pady=10, padx=20, fill="both", expand=True)

    columns = ("id", "phone", "model", "price", "date")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
    
    tree.heading("id", text="ID")
    tree.heading("phone", text="Telefon nomi")
    tree.heading("model", text="IMEI")
    tree.heading("price", text="Narxi")
    tree.heading("date", text="Sana")

    tree.column("id", anchor="center", width=50)
    tree.column("phone", anchor="center", width=150)
    tree.column("model", anchor="center", width=150)
    tree.column("price", anchor="center", width=100)
    tree.column("date", anchor="center", width=100)

    # Skroll
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    # Ma'lumotlarni yuklash
    for i, phone in enumerate(phones, 1):
        tree.insert("", tk.END, values=(
            i,
            phone["nomi"],
            phone["modeli"],
            phone["narx"],
            phone["sana"]
        ))

    # Tugmalar
    btn_frame = tk.Frame(print_window, bg=colors["bg"])
    btn_frame.pack(pady=15)

    def print_selected():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Xatolik", "Iltimos, telefon tanlang!")
            return
            
        selected_values = tree.item(selected_item)['values']
        phone_data = {
            "nomi": selected_values[1],
            "modeli": selected_values[2],
            "narx": selected_values[3],
            "sana": selected_values[4]
        }
        
        print_phone_details(phone_data)

    # Chop etish tugmasi
    print_btn = tk.Button(btn_frame, 
                         text=translations[language]["chop_et"],
                         command=print_selected,
                         bg=colors["button_bg"],
                         fg=colors["button_fg"],
                         font=("Arial", 12, "bold"))
    print_btn.pack(side=tk.LEFT, padx=5)

    # Yopish tugmasi
    close_btn = tk.Button(btn_frame, 
                         text=translations[language]["yop"],
                         command=print_window.destroy,
                         bg="#FF6B6B",
                         fg="white",
                         font=("Arial", 12))
    close_btn.pack(side=tk.LEFT, padx=5)

    # Double click bilan chop etish
    tree.bind('<Double-1>', lambda e: print_selected())

def printer_file_ochish():
    try:
        # tuliq fayil kursatish
        file_path = os.path.join(os.path.dirname(__file__), "print2.py")

        # pythonni tuliq yuli bilan ishga tushirish
        python_exe = sys.executable
        subprocess.Popen([python_exe, file_path])
    except FileNotFoundError:
        messagebox.showerror("Xatolik", "printer_file.py fayli topilmadi!")
    except Exception as e:
        messagebox.showerror("Xatolik", f"Xatolik yuz berdi: {str(e)}")

############################
def open_search():
    """qidruv funksiyasi yangi fayilga saqlandi uni avvalgi versiyasida bir nechta xatoliklar borligi sabab
    yangi fayilga chroylirq formatga uchrib kurchirldi"""
    try:
        # tuliq fayil kursatish
        def run_search():
            file_path = os.path.join(os.path.dirname(__file__), "SEARCH.py")
            python_exe = sys.executable
            subprocess.Popen([python_exe, file_path])
        threading.Thread(target=run_search, daemon=True).start()
    except FileNotFoundError:
        messagebox.showerror("Xatolik", "SEARCH.py fayli topilmadi!")
    except Exception as e:
        messagebox.showerror("Xatolik", f"Xatolik yuz berdi: {str(e)}")

############################


def factory_reset():
    """Dastur ma'lumotlarini tozalash va noldan boshlash (ichki parol saqlanadi)"""
    if not messagebox.askyesno("Diqqat!", "Barcha ma'lumotlar (telefonlar, sotilganlar, login paroli, username) o'chiriladi. Davom etasizmi?"):
        return

    # Kod so‘rash
    kod = simpledialog.askstring("Xavfsizlik kodi", "Dastur tozalash kodi kiriting:", show="*")
    if kod != "aL9@Z!f4#pX$7vB1":  # bu yerni xohlagan kodga o‘zgartirishingiz mumkin
        messagebox.showerror("Xato", "Noto‘g‘ri kod kiritildi. Tozalash bekor qilindi.")
        return

    # O'chiriladigan fayllar ro'yxati
    files_to_delete = [
        "telefon_data.json",
        "sotish_file.json",
        "app_config.json",
        "data.json",
        "deleted_phones.json",
        "notebook_data.json",
        "selected_phone.json",
        "sold_phones.json"
    ]
    for file in files_to_delete:
        if os.path.exists(file):
            try:
                os.remove(file)
            except Exception as e:
                messagebox.showerror("Xatolik", f"{file} faylini o'chirishda xatolik: {str(e)}")

    # internal_codes.json faqat ichki parolni saqlab qoladi
    codes_file = "internal_codes.json"
    codes = {"IDEAL MOBILE": "ichki123"}
    with open(codes_file, "w", encoding="utf-8") as f:
        json.dump(codes, f, ensure_ascii=False, indent=4)

    messagebox.showinfo("Tayyor", "Dastur tozalandi! Qayta ishga tushadi.")
    python = sys.executable
    os.execl(python, python, *sys.argv)
        
    

language = "ru"  # yoki "ru"
menu_items = {}
button_items = {}



def change_language():
    global language
    language = "ru" if language == "uz" else "uz"
    update_ui_texts()

def update_ui_texts():
    # Dastur sarlavhasi
    if 'root_app' in globals():
        root_app.title(translations[language]["title"])



    # Menyular
    if "phone_menu" in menu_items:
        phone_menu = menu_items["phone_menu"]
        phone_menu.entryconfig(0, label=translations[language]["add_phone"])
        phone_menu.entryconfig(1, label=translations[language]["delete_phone"])
        phone_menu.entryconfig(2, label=translations[language]["view_phones"])

    if "yangilar" in menu_items:
        yangilar_menu = menu_items["yangilar"]
        yangilar_menu.entryconfig(0, label=translations[language]["phone_stats"])
        yangilar_menu.entryconfig(1, label=translations[language]["chop_et"])
        yangilar_menu.entryconfig(2, label=translations[language]["print"])
        yangilar_menu.entryconfig(3, label=translations[language]["qdr"])



    if "info_menu" in menu_items:
        info_menu = menu_items["info_menu"]
        info_menu.entryconfig(0, label=translations[language]["save_data"])
        info_menu.entryconfig(1, label=translations[language]["load_data"])
        info_menu.entryconfig(3, label=translations[language]["about"])

    if "settings_menu" in menu_items:
        settings_menu = menu_items["settings_menu"]
        settings_menu.entryconfig(0, label=translations[language]["change_language"])
        settings_menu.entryconfig(1, label=translations[language]["dark_mode"])
        settings_menu.entryconfig(3, label=translations[language]["login"])


    

    if "theme_menu" in menu_items:
        theme_menu = menu_items["theme_menu"]
        keys = ["classic", "white", "black"]
        for i, key in enumerate(keys):
            theme_menu.entryconfig(i, label=translations[language][key])

    # Tugmalar
    for key, btn in button_items.items():
        if key in translations[language]:
            btn.configure(text=translations[language][key])
    
    if "sidebar" in menu_items:
        for section, btn_list in menu_items["sidebar"].items():
            for i, btn in enumerate(btn_list):
                key = None
                if section == "phone_menu":
                    key = ["add_phone", "delete_phone", "view_phones", "phone_stats"][i]
                elif section == "info_menu":
                    key = ["save_data", "load_data", "about"][i]
                elif section == "settings":
                    key = ["change_language", "dark_mode", "reset", "login_title"][i]
                if key and key in translations[language]:
                    btn.configure(text=translations[language][key])
                    
    if "section_labels" in menu_items:
        for key, lbl in menu_items["section_labels"].items():
            if key in translations[language]:
                lbl.configure(text=translations[language][key])


            
            



def main_application():
    global root_app
    root_app = tk.Tk()
    root_app.title(translations[language]["title"])
    root_app.state('zoomed')
    root_app.configure(bg=colors["bg"])
    center_window(root_app)
    
    


    # Menu
    menubar = tk.Menu(root_app)
    root_app.config(menu=menubar)

    # Sidebar for navigation (replaces the menubar)
    sidebar_frame = ctk.CTkFrame(root_app, width=250, fg_color=colors["menu_bg"], corner_radius=0)
    sidebar_frame.pack(side="left", fill="y")

    # Phone Menu Section
    phone_label = ctk.CTkLabel(
        sidebar_frame,
        text=translations[language]["phone_menu"],
        font=ctk.CTkFont(size=18, weight="bold"),
        text_color=colors["fg"]
    )
    phone_label.pack(pady=(20, 10), anchor="w", padx=20)

    btn_add_phone = ctk.CTkButton(
        sidebar_frame,
        text=translations[language]["add_phone"],
        command=add_phone,
        width=200,
        fg_color=colors["button_bg"],
        hover_color=colors["button_fg"],
        corner_radius=10
    )
    btn_add_phone.pack(pady=5, padx=20)

    btn_delete_phone = ctk.CTkButton(
        sidebar_frame,
        text=translations[language]["delete_phone"],
        command=delete_phone,
        width=200,
        fg_color=colors["button_bg"],
        hover_color=colors["button_fg"],
        corner_radius=10
    )
    btn_delete_phone.pack(pady=5, padx=20)

    btn_view_phones = ctk.CTkButton(
        sidebar_frame,
        text=translations[language]["view_phones"],
        command=view_phones,
        width=200,
        fg_color=colors["button_bg"],
        hover_color=colors["button_fg"],
        corner_radius=10
    )
    btn_view_phones.pack(pady=5, padx=20)

    btn_phone_stats = ctk.CTkButton(
        sidebar_frame,
        text=translations[language]["phone_stats"],
        command=show_phone_stats,
        width=200,
        fg_color=colors["button_bg"],
        hover_color=colors["button_fg"],
        corner_radius=10
    )
    btn_phone_stats.pack(pady=5, padx=20)

    # Info Menu Section
    info_label = ctk.CTkLabel(
        sidebar_frame,
        text=translations[language]["info_menu"],
        font=ctk.CTkFont(size=18, weight="bold"),
        text_color=colors["fg"]
    )
    info_label.pack(pady=(20, 10), anchor="w", padx=20)

    btn_save_data = ctk.CTkButton(
        sidebar_frame,
        text=translations[language]["save_data"],
        command=save_data,
        width=200,
        fg_color=colors["button_bg"],
        hover_color=colors["button_fg"],
        corner_radius=10
    )
    btn_save_data.pack(pady=5, padx=20)

    btn_load_data = ctk.CTkButton(
        sidebar_frame,
        text=translations[language]["load_data"],
        command=load_data,
        width=200,
        fg_color=colors["button_bg"],
        hover_color=colors["button_fg"],
        corner_radius=10
    )
    btn_load_data.pack(pady=5, padx=20)

    btn_about = ctk.CTkButton(
        sidebar_frame,
        text=translations[language]["about"],
        command=show_about,
        width=200,
        fg_color=colors["button_bg"],
        hover_color=colors["button_fg"],
        corner_radius=10
    )
    btn_about.pack(pady=5, padx=20)

    # Settings Menu Section
    settings_label = ctk.CTkLabel(
        sidebar_frame,
        text=translations[language]["settings"],
        font=ctk.CTkFont(size=18, weight="bold"),
        text_color=colors["fg"]
    )
    settings_label.pack(pady=(20, 10), anchor="w", padx=20)

    btn_change_language = ctk.CTkButton(
        sidebar_frame,
        text=translations[language]["change_language"],
        command=change_language,
        width=200,
        fg_color=colors["button_bg"],
        hover_color=colors["button_fg"],
        corner_radius=10
    )
    btn_change_language.pack(pady=5, padx=20)

    btn_toggle_dark_mode = ctk.CTkButton(
        sidebar_frame,
        text=translations[language]["dark_mode"],
        command=toggle_dark_mode,
        width=200,
        fg_color=colors["button_bg"],
        hover_color=colors["button_fg"],
        corner_radius=10
    )
    btn_toggle_dark_mode.pack(pady=5, padx=20)
    
    btn_reset = ctk.CTkButton(
        sidebar_frame,
        text=translations[language]["reset"],
        command=factory_reset,
        width=200,
        fg_color=colors["button_bg"],
        hover_color=colors["button_fg"],
        corner_radius=10
    )
    btn_reset.pack(pady=5, padx=20)

    btn_login = ctk.CTkButton(
        sidebar_frame,
        text=translations[language]["login_title"],
        command=lock_application,
        width=200,
        fg_color=colors["button_bg"],
        hover_color=colors["button_fg"],
        corner_radius=10
    )
    btn_login.pack(pady=5, padx=20)
    

    
    
    


    # Save sidebar buttons in menu_items dictionary if needed later
    menu_items["sidebar"] = {
        "phone_menu": [btn_add_phone, btn_delete_phone, btn_view_phones, btn_phone_stats],
        "info_menu": [btn_save_data, btn_load_data, btn_about],
        "settings": [btn_change_language, btn_toggle_dark_mode, btn_reset, btn_login],
        "reset": []  # bo‘sh tugma ro‘yxati
    }
    
    # label til almashishlari
    menu_items["section_labels"] = {
        "phone_menu": phone_label,
        "info_menu": info_label,
        "settings": settings_label
    }







    # Asosiy soha
    main_frame = tk.Frame(root_app, bg=colors["bg"])
    main_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Sarlavha
    title_label = tk.Label(main_frame, text="IDEAL MOBILE", font=("Arial", 24, "bold"),
                           bg=colors["bg"], fg=colors["fg"])
    title_label.pack(pady=20)

    # Tugmalar paneli
    button_frame = tk.Frame(main_frame, bg=colors["bg"])
    button_frame.pack(pady=20)

    # Chap va o'ng tugma panellari
    left_button_frame = ctk.CTkFrame(main_frame, fg_color="#2c3e50", corner_radius=15, border_width=2,
                                     border_color="#34495e", width=400, height=800)
    left_button_frame.pack(side=tk.LEFT, pady=20, padx=50, anchor="nw", fill="both", expand=True)

    right_button_frame = ctk.CTkFrame(main_frame, fg_color="#2c3e50", corner_radius=15, border_width=2,
                                      border_color="#2c3e50", width=400, height=800)
    right_button_frame.pack(side=tk.RIGHT, pady=20, padx=50, anchor="nw", fill="both", expand=True)

    # Tugmalar ro‘yxati
    left_buttons = [
        ("add_phone", add_phone),
        ("delete_phone", delete_phone),
        ("view_phones", view_phones),
        ("seel_phon", open_sales_file),
        ("note", open_eslatma_file)


    ]

    # Chap tugmalarni yaratish va ro‘yxatga olish
    for key, command in left_buttons:
        btn = ctk.CTkButton(
            left_button_frame,
            text=translations[language][key],
            command=command,
            fg_color="#3498db",
            hover_color="#2980b9",
            text_color="white",
            font=("Arial", 20, "bold"),
            width=320,
            height=75,
            corner_radius=10,
            border_width=5,
            border_color="#2980b9"
        )
        btn.pack(pady=25, padx=30, anchor="center")
        button_items[key] = btn  # Ro‘yxatga olish

    # O'ng panelga 1ta bo‘sh tugma (istasa kengaytirasan)
    right_buttons = [
        ("phone_istory", view_all_history),
        ("phone_stats", show_phone_stats),
        ("chop_et", view_print_screen),
        ("print", printer_file_ochish),
        ("qdr", open_search)
    ]



    for key, command in right_buttons:
        btn = ctk.CTkButton(
            right_button_frame,
            text=translations[language][key],
            command=command,
            fg_color="#3498db",
            hover_color="#2980b9",
            text_color="white",
            font=("Arial", 20, "bold"),
            width=320,
            height=75,
            corner_radius=10,
            border_width=5,
            border_color="#2980b9"
        )
        btn.pack(pady=25, padx=30, anchor="center")
        button_items[key] = btn  # Ro‘yxatga olish
        
    clock_label = tk.Label(
        root_app,
        font=("Consolas", 16, "bold"),
        bg=colors["bg"],
        fg="#dbdee0"
    )
    # clock_label.place(relx=0.0, rely=0.0, anchor="sw", x=20, y=880)
    clock_label.place(relx=0.0, rely=1.0, anchor="sw", x=30, y=-80)


    # clock_label.place(relx=1.0, rely=0.0, anchor="ne", x=-20, y=20)  # O'ng yuqori burchakda
    import datetime
    def update_clock():
        now = datetime.datetime.now()
        # Format: YYYY-MM-DD
        date_str = now.strftime("%Y-%m-%d")
        # Format: HH:MM:SS:MS
        time_str = now.strftime("%H:%M:%S") + f":{int(now.microsecond/1000):03d}"
        clock_label.config(text=f"{date_str}\n{time_str}")
        root_app.after(50, update_clock)  # Har 50 ms da yangilansin

    update_clock()
    
    # camera_frame = tk.Frame(root_app, width=250, height=180, bg="#222", highlightbackground="#3498db", highlightthickness=3)
    # camera_frame.place(relx=0.01, rely=0.85, anchor="sw")  # Chap pastki burchakda

    # # Kamera oynasi labeli
    # camera_label = tk.Label(camera_frame, bg="#222")
    # camera_label.pack(fill="both", expand=True)

    # # Kamera stream funksiyasi
    # def show_camera():
    #     cap = cv2.VideoCapture(0)
    #     def update():
    #         ret, frame = cap.read()
    #         if ret:
    #             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #             img = Image.fromarray(frame)
    #             img = img.resize((210, 220))
    #             imgtk = ImageTk.PhotoImage(image=img)
    #             camera_label.imgtk = imgtk
    #             camera_label.config(image=imgtk)
    #         camera_label.after(30, update)
    #     update()
    # show_camera()

# Kamera frame
    camera_frame = tk.Frame(root_app, width=250, height=180, bg="#222", highlightbackground="#3498db", highlightthickness=3)
    camera_frame.place(relx=0.01, rely=0.85, anchor="sw")

    # Kamera label
    camera_label = tk.Label(camera_frame, bg="#222")
    camera_label.pack(fill="both", expand=True)

    cap = cv2.VideoCapture(0)

    def update():
        if not camera_label.winfo_exists():
            cap.release()
            return  # Agar label yo‘q bo‘lsa, davom etmasin

        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = img.resize((210, 220))
            imgtk = ImageTk.PhotoImage(image=img)
            camera_label.imgtk = imgtk
            camera_label.config(image=imgtk)

        camera_label.after(30, update)

    update()  # kamerani ishga tushirish

    def on_closing():
        cap.release()  # kamera resursini bo‘shat
        root_app.destroy()

    root_app.protocol("WM_DELETE_WINDOW", on_closing) 

        

    # Dastlabki yuklashlar
    load_data()
    load_sold_phones()

    root_app.mainloop()



if __name__ == "__main__":       
    main_application()
    



