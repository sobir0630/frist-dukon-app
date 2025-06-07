import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog, ttk, filedialog
import os
import json
import time
import threading
import random
from datetime import datetime
import re
import sys
from tkinter import font
import customtkinter as ctk
import win32print
import win32ui
from PIL import Image, ImageDraw
import subprocess
import os
import sys
import subprocess
from tkinter import messagebox
import hashlib
from ichki_codes import LoginWindow, PasswordManager


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
        "title": "IDEAL MOBILE",
        "phone_menu": "Tovarlar",
        "add_phone": "📱 Telefon qo‘shish",
        "delete_phone": "❌ Telefonni o‘chirish",
        "view_phones": "📋 Telefonlar ro‘yxati",
        "info_menu": "Ma'lumotlar",
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
        "toggle_dark_mode": "Tungi rejim",
        "login_title": "Kirish oynasi",
        "username": "Ism:",
        "password": "Parol:",
        "login": "Kirish",
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
        "qushilgan": "qushilgan sana"

    },
    "ru": {
        "title": "Программа магазина телефонов",
        "phone_menu": "Телефонные товары",
        "add_phone": "Добавить телефон",
        "delete_phone": "Удалить телефон",
        "view_phones": "Список телефонов",
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
        "toggle_dark_mode": "Ночной режим",
        "login_title": "Окно входа",
        "username": "Имя:",
        "password": "Пароль:",
        "login": "Войти",
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
        "qushilgan": "дата въезда"

    }
}

# Ranglar sxemalari
themes = {
    "classic": {
        "light": {
            "bg": "#DFFFD6",
            "fg": "#000000",
            "button_bg": "#228B22",
            "button_fg": "#FFFFFF",
            "entry_bg": "#FFFFFF",
            "entry_fg": "#000000",
            "highlight_bg": "#9ACD32",
            "border": "#228B22"
        },
        "dark": {
            "bg": "#1E1E1E",
            "fg": "#FFFFFF",
            "button_bg": "#228B22",
            "button_fg": "#FFFFFF",
            "entry_bg": "#333333",
            "entry_fg": "#FFFFFF",
            "highlight_bg": "#3A5F0B",
            "border": "#3A5F0B"
        }
    },
    "blue": {
        "light": {
            "bg": "#E6F2FF",
            "fg": "#000000",
            "button_bg": "#1E88E5",
            "button_fg": "#FFFFFF",
            "entry_bg": "#FFFFFF",
            "entry_fg": "#000000",
            "highlight_bg": "#64B5F6",
            "border": "#1E88E5"
        },
        "dark": {
            "bg": "#0A1929",
            "fg": "#FFFFFF",
            "button_bg": "#1976D2",
            "button_fg": "#FFFFFF",
            "entry_bg": "#102A43",
            "entry_fg": "#FFFFFF",
            "highlight_bg": "#1565C0",
            "border": "#1565C0"
        }
    },
    "green": {
        "light": {
            "bg": "#E8F5E9",
            "fg": "#000000",
            "button_bg": "#43A047",
            "button_fg": "#FFFFFF",
            "entry_bg": "#FFFFFF",
            "entry_fg": "#000000",
            "highlight_bg": "#81C784",
            "border": "#43A047"
        },
        "dark": {
            "bg": "#0A1F0A",
            "fg": "#FFFFFF",
            "button_bg": "#2E7D32",
            "button_fg": "#FFFFFF",
            "entry_bg": "#1B5E20",
            "entry_fg": "#FFFFFF",
            "highlight_bg": "#2E7D32",
            "border": "#2E7D32"
        }
    },

    "white": {  # Kunduzgi tema
        "light": {
            "bg": "#FFFFFF",
            "fg": "#333333",
            "button_bg": "#4CAF50",
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
            "fg": "#333333",
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
            "fg": "#FFFFFF",
            "button_bg": "#BB86FC",
            "button_fg": "#000000",
            "entry_bg": "#1E1E1E",
            "entry_fg": "#FFFFFF",
            "highlight_bg": "#3700B3",
            "border": "#BB86FC"
        },
        "dark": {
            "bg": "#121212",
            "fg": "#FFFFFF",
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

# Kunduzgi mavzuga o'tish uchun
    change_theme("white")

    # Kechki mavzuga o'tish uchun
    change_theme("black")


    # Menu qismiga qo'shish
    theme_menu.add_separator()
    theme_menu.add_command(label="Kunduzgi mavzu", command=lambda: change_theme("white"))
    theme_menu.add_command(label="Kechki mavzu", command=lambda: change_theme("black"))
    theme_menu.add_separator()
    theme_menu.add_command(label="Mavzu rejimini almashtirish", command=toggle_theme_mode)

def toggle_theme_mode():
    """Kunduzgi/Kechki mavzuni almashtirish"""
    global dark_mode, current_theme
    dark_mode = not dark_mode
    
    # Agar joriy mavzu white yoki black bo'lsa
    if current_theme in ["white", "black"]:
        # Kunduzgi/Kechki mavzularni almashtirish
        current_theme = "black" if dark_mode else "white"
    
    # Mavzuni qo'llash
    change_theme(current_theme)
    
    # Sozlamalarni saqlash
    save_theme_settings()




def change_theme(theme_name):
    """Dastur mavzusini o'zgartirish"""
    global current_theme, colors
    
    # Mavzuni saqlash
    current_theme = theme_name
    colors = themes[current_theme]["dark" if dark_mode else "light"]
    
    try:
        # Asosiy oyna ranglarini yangilash
        root_app.configure(bg=colors["bg"])
        
        # Barcha framelarni yangilash
        for widget in root_app.winfo_children():
            if isinstance(widget, (tk.Frame, tk.LabelFrame)):
                widget.configure(bg=colors["bg"])
                # Frame ichidagi elementlarni yangilash
                for child in widget.winfo_children():
                    update_widget_colors(child)
        
        # Menyu ranglarini yangilash
        update_menu_colors(root_app.nametowidget(root_app.cget("menu")))
        
        # Theme sozlamalarini saqlash
        save_theme_settings()
        
        messagebox.showinfo("Muvaffaqiyatli", f"{theme_name} mavzusi o'rnatildi!")
        
    except Exception as e:
        messagebox.showerror("Xatolik", f"Mavzuni o'zgartirishda xatolik: {str(e)}")

def update_widget_colors(widget):
    """Widget ranglarini yangilash"""
    try:
        if isinstance(widget, (tk.Label, tk.Button, tk.Entry, tk.Text)):
            widget.configure(
                bg=colors["entry_bg"] if isinstance(widget, tk.Entry) else colors["bg"],
                fg=colors["fg"],
                highlightbackground=colors["border"]
            )
            
        elif isinstance(widget, ttk.Treeview):
            style = ttk.Style()
            style.configure(
                "Treeview",
                background=colors["entry_bg"],
                foreground=colors["entry_fg"],
                fieldbackground=colors["entry_bg"]
            )
            style.configure(
                "Treeview.Heading",
                background=colors["button_bg"],
                foreground=colors["button_fg"]
            )
            
        elif isinstance(widget, ctk.CTkButton):
            widget.configure(
                fg_color=colors["button_bg"],
                hover_color=colors["highlight_bg"],
                text_color=colors["button_fg"]
            )
            
        # Ichki elementlarni rekursiv yangilash
        for child in widget.winfo_children():
            update_widget_colors(child)
            
    except Exception:
        pass

def update_menu_colors(menu):
    """Menyu ranglarini yangilash"""
    try:
        menu.configure(
            bg=colors["bg"],
            fg=colors["fg"],
            activebackground=colors["highlight_bg"],
            activeforeground=colors["button_fg"]
        )
        # Barcha submenularni yangilash
        for item in menu.winfo_children():
            if isinstance(item, tk.Menu):
                update_menu_colors(item)
    except Exception:
        pass

def save_theme_settings():
    """Mavzu sozlamalarini saqlash"""
    try:
        settings = {
            "theme": current_theme,
            "dark_mode": dark_mode
        }
        with open("theme_settings.json", "w") as f:
            json.dump(settings, f)
    except Exception:
        pass

def load_theme_settings():
    """Saqlangan mavzu sozlamalarini yuklash"""
    global current_theme, dark_mode
    try:
        if os.path.exists("theme_settings.json"):
            with open("theme_settings.json", "r") as f:
                settings = json.load(f)
                current_theme = settings.get("theme", "classic")
                dark_mode = settings.get("dark_mode", False)
    except Exception:
        current_theme = "classic"
        dark_mode = False

# Tungi rejimni o'zgartirish funksiyasi (qo'shildi)
def toggle_dark_mode():
    global dark_mode, colors
    dark_mode = not dark_mode
    colors = themes[current_theme]["dark" if dark_mode else "light"]
    # Mavzuni qo'llash kodlari (root_app configuratsiyasi)
    if 'root_app' in globals():
        root_app.configure(bg=colors["bg"])
        # Boshqa UI elementlarini yangilash...


# Tilni o'zgartirish funksiyasi (qo'shildi)
def change_language():
    global language
    language = "ru" if language == "uz" else "uz"
    # Tarjimalarni yangilash kodlari (root_app configuratsiyasi)
    if 'root_app' in globals():
        root_app.title(translations[language]["title"])
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
    global phones
    try:
        if os.path.exists(data_file):
            with open(data_file, 'r', encoding='utf-8') as f:
                phones = json.load(f)
        else:
            # Demo rejimda ma'lumotlarni generatsiya qilish
            generate_demo_data()
    except Exception as e:
        messagebox.showerror(translations[language]["error"], str(e))


def on_exit():
    if messagebox.askyesno(translations[language]["save_data"], "Dasturdan chiqishdan oldin ma'lumotlarni saqlashni xohlaysizmi?"):
        save_data()
    root_app.destroy()


def generate_demo_data():


    # 10 ta telefon generatsiya qilish
    phones = []
    pass
    for _ in range(10):
        brand_data = random.choice(phone_models)
        brand = brand_data["brand"]
        model = random.choice(brand_data["models"])

        # Random narx
        min_price, max_price = price_ranges[brand]
        price = f"{random.randint(min_price, max_price)} $"

        # Random narx
        date_str = ""


        # Random sana (oxirgi 6 oy ichida)
        days_ago = random.randint(1, 180)
        date_obj = datetime.now()
        date_obj = datetime.now() - timedelta(days=days_ago)
        if date_obj.day > 28:
            date_obj = date_obj.replace(day=28)
        date_str = date_obj.strftime("%d/%m/%Y")

        phones.append({
            "nomi": brand,
            "modeli": model,
            "narx": price,
            "sana": date_str
        })


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
        correct_username = "Sobir"
        correct_password = "0630"

        if username == CORRECT_USERNAME and password == CORRECT_PASSWORD:
            login_window.destroy()
            messagebox.showinfo("Muvaffaqiyat", f"Xush kelibsiz, {correct_username}!")
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
    add_window.title("📱 Yangi Telefon Qo'shish")
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
        text="📱 Yangi Telefon Qo'shish",
        font=ctk.CTkFont(size=28, weight="bold"),
        text_color=("#2c3e50", "#ecf0f1")
    )
    title_label.pack(pady=(20, 30))

    # Avtomatik indeks ko'rsatish
    next_index = len(phones) + 1
    index_label = ctk.CTkLabel(
        add_window,
        text=f"🔢 Telefon Indeksi: #{next_index:03d}",
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

    info_title = ctk.CTkLabel(
        info_frame,
        text="📋 Asosiy Ma'lumotlar",
        font=ctk.CTkFont(size=18, weight="bold"),
        text_color=("#34495e", "#bdc3c7")
    )
    info_title.pack(pady=(15, 20))

    # Telefon nomi
    name_label = ctk.CTkLabel(
        info_frame,
        text="📱 Telefon Nomi:",
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

    # Telefon turi
    type_label = ctk.CTkLabel(
        info_frame,
        text="🏷️ Telefon Turi:",
        font=ctk.CTkFont(size=14),
        text_color=("#2c3e50", "#ecf0f1"),
        anchor="w"
    )
    type_label.pack(pady=(5, 5), padx=20, fill="x")

    phone_types = ["iPhone", "Samsung", "Xiaomi", "Huawei", "OnePlus", "Google Pixel", "Oppo", "Vivo", "Realme", "Boshqa"]
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

    price_date_title = ctk.CTkLabel(
        price_date_frame,
        text="💰 Moliyaviy Ma'lumotlar",
        font=ctk.CTkFont(size=18, weight="bold"),
        text_color=("#34495e", "#bdc3c7")
    )
    price_date_title.pack(pady=(15, 20))

    # Narx
    price_label = ctk.CTkLabel(
        price_date_frame,
        text="💰 Sotib Olingan Narx ($):",
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

    # Sana
    date_label = ctk.CTkLabel(
        price_date_frame,
        text="📅 Sotib Olingan Sana:",
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

    today_button = ctk.CTkButton(
        date_frame,
        text="📅 Bugun",
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

    extra_title = ctk.CTkLabel(
        extra_frame,
        text="📝 Qo'shimcha Ma'lumotlar",
        font=ctk.CTkFont(size=18, weight="bold"),
        text_color=("#34495e", "#bdc3c7")
    )
    extra_title.pack(pady=(15, 20))

    # Holat
    condition_label = ctk.CTkLabel(
        extra_frame,
        text="⚡ Telefon Holati:",
        font=ctk.CTkFont(size=14),
        text_color=("#2c3e50", "#ecf0f1"),
        anchor="w"
    )
    condition_label.pack(pady=(5, 5), padx=20, fill="x")

    conditions = ["Yangi", "Juda Yaxshi", "Yaxshi", "O'rtacha", "Tuzatishga Muhtoj"]
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

    # Eslatma
    note_label = ctk.CTkLabel(
        extra_frame,
        text="📝 Eslatma:",
        font=ctk.CTkFont(size=14),
        text_color=("#2c3e50", "#ecf0f1"),
        anchor="w"
    )
    note_label.pack(pady=(5, 5), padx=20, fill="x")

    # note_entry = ctk.CTkTextbox(
    #     extra_frame,
    #     placeholder_text="Qo'shimcha ma'lumotlar yoki eslatmalar...",
    #     font=ctk.CTkFont(size=14),
    #     height=100,
    #     corner_radius=10
    # )
    # note_entry.pack(pady=(20), padx=20, fill="x")

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

            f"🆔 Indeks: #{next_index:03d}"
            f"📱 Nomi: {name}"
            f"🔢 IMEI/Model: {model}"
            f"🏷️ Turi: {phone_type}"
            f"💰 Narx: ${price:.2f}"
            f"📅 Sana: {date}"
            f"⚡ Holat: {condition}"
            # f"📝 Eslatma: {note if note else 'Yuq'}\n"

            "❓ Telefonni qo'shishni tasdiqlaysizmi?"
        )

        if not messagebox.askyesno("✅ Tasdiqlash", confirm_text):
            return

        # Progress oynasi
        progress_window = ctk.CTkToplevel(add_window)
        progress_window.title("📱 Telefon Qo'shilmoqda...")
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

        # Progress elementi
        progress_label = ctk.CTkLabel(
            progress_window,
            text=f"📱 {name} qo'shilmoqda...",
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
                time.sleep(0.02)

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
            
            # saqlash fayli
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


            progress_window.destroy()
            messagebox.showinfo("✅ Muvaffaqiyatli", 
                              f"🎉 {name} muvaffaqiyatli qo'shildi!\n\n"
                              f"🆔 Indeks: #{next_index:03d}\n"
                              f"💰 Narx: ${price:.2f}")
            add_window.destroy()

        # Progress animatsiyasini alohida thread da ishga tushirish
        threading.Thread(target=animate_progress, daemon=True).start()







    # 🔽 Tugmalar uchun pastki frame
    buttons_frame = ctk.CTkFrame(add_window, fg_color="transparent")
    buttons_frame.pack(side="bottom", pady=15, fill="x")

    # ✅ Saqlash tugmasi
    save_button = ctk.CTkButton(
        buttons_frame,
        text="✅ Saqlash",
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

    # ❌ Bekor qilish tugmasi
    cancel_button = ctk.CTkButton(
        buttons_frame,
        text="❌ Bekor qilish",
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

        form_window = tk.Toplevel(edit_window)
        form_window.title(translations[language]["edit_phone"])
        form_window.geometry("400x300")
        form_window.configure(bg=colors["bg"])
        form_window.transient(edit_window)
        form_window.grab_set()

        center_window(form_window)



        tk.Label(form_window, text=translations[language]["phone_name_label"],
                 bg=colors["bg"], fg=colors["fg"]).pack(pady=5)
        name_entry = tk.Entry(form_window, bg=colors["entry_bg"], fg=colors["entry_fg"])
        name_entry.insert(0, phone["nomi"])
        name_entry.pack(pady=5)

        tk.Label(form_window, text=translations[language]["model_label"],
                 bg=colors["bg"], fg=colors["fg"]).pack(pady=5)
        model_entry = tk.Entry(form_window, bg=colors["entry_bg"], fg=colors["entry_fg"])
        model_entry.insert(0, phone["modeli"])
        model_entry.pack(pady=5)

        
        tk.Label(form_window, text=translations[language]["tur"], 
                bg=colors["bg"],
                fg=colors["fg"],
                ).pack(pady=5)
        turi_entry = tk.Entry(form_window, bg=colors["entry_bg"], fg=colors["entry_fg"])
        turi_entry.insert(0, phone["turi"])
        turi_entry.pack(pady=5)

        tk.Label(form_window, text=translations[language]["price_label"],
                 bg=colors["bg"], fg=colors["fg"]).pack(pady=5)
        price_entry = tk.Entry(form_window, bg=colors["entry_bg"], fg=colors["entry_fg"])
        price_entry.insert(0, phone["narx"])
        price_entry.pack(pady=5)

        tk.Label(form_window, text=translations[language]["date_label"],
                 bg=colors["bg"], fg=colors["fg"]).pack(pady=5)
        date_entry = tk.Entry(form_window, bg=colors["entry_bg"], fg=colors["entry_fg"])
        date_entry.insert(0, phone["sana"])
        date_entry.pack(pady=5)

                
        tk.Label(form_window, text=translations[language]["holat"], 
                bg=colors["bg"],
                fg=colors["fg"],
                ).pack(pady=5)
        holat_entry = tk.Entry(form_window, bg=colors["entry_bg"], fg=colors["entry_fg"])
        holat_entry.insert(0, phone["holat"])
        holat_entry.pack(pady=5)

                
        tk.Label(form_window, text=translations[language]["qushilgan"], 
                bg=colors["bg"],
                fg=colors["fg"],
                ).pack(pady=5)
        qushilgan_entry = tk.Entry(form_window, bg=colors["entry_bg"], fg=colors["entry_fg"])
        qushilgan_entry.insert(0, phone.get("qushilgan_sana"))
        qushilgan_entry.pack(pady=5)

        def save_changes():
            phone["index"] = name_entry.get().strip()
            phone["nomi"] = model_entry.get().strip()
            phone["modeli"] = price_entry.get().strip()
            phone["narx"] = name_entry.get().strip()
            phone["turi"] = date_entry.get().strip()
            phone["sana"] = model_entry.get().strip()
            phone["holat"] = price_entry.get().strip()
            phone["qushilgan_sana"] = date_entry.get().strip()

            save_data()
            load_tree_data(search_var.get())
            form_window.destroy()

            def on_enter(event):
                save_changes()
            add_window.bind('<Return>', on_enter)
            # add_window.bind('<Control-Return>', on_enter)

            # save_btn = tk.Button(form_window, 
            #                     text=translations[language]["update"],
            #                     command=save_changes(),
            #                     bg=colors["bg"],
            #                     fg=color["fg"],
            #                     font=tk.Font(size=14, weight="bold")
            # ).pack(pady=10)

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
        translations[language]["sort_name"],
        translations[language]["sort_price_asc"],
        translations[language]["sort_price_desc"],
        translations[language]["sort_date"]
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
    tree.heading("turi", text="turi")
    tree.heading("narx", text=translations[language]["price_label"])
    tree.heading("sana", text="sana")
    tree.heading("holat", text="holat")
    tree.heading("qushilgan_sana", text="qushilgan_sana")

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



        tree.delete(*tree.get_children())
        sorted_phones = sort_phones(phones.copy())

        for i, phone in enumerate(sorted_phones):
            if (
                search_text.lower() in phone["nomi"].lower()
                or search_text.lower() in phone["modeli"].lower()
            ):
                tree.insert("", tk.END, values=(
                    i + 1,
                    phone.get("nomi", ""),
                    phone.get("modeli", ""),
                    phone.get("turi", ""),
                    phone.get("narx", ""),
                    phone.get("sana", ""),
                    phone.get("holat", ""),
                    phone.get("qoshilgan_sana", "")
                ))


    # Telefonlarni saralash
    def clean_price(price):
        """ Narxdan kerakmas belgilarni olib tashlab, faqat son qismi qaytariladi """
        return float(re.sub(r"[^\d.]", "", price))  # Faqat raqam va nuqta qoldiriladi

    def sort_phones(phone_list):
        sort_choice = sort_var.get()

        if sort_choice == translations[language]["sort_name"]:
            return sorted(phone_list, key=lambda x: x["nomi"], reverse=True)  # Alfavit bo‘yicha teskari tartib
        elif sort_choice == translations[language]["sort_price_asc"]:
            return sorted(phone_list, key=lambda x: clean_price(x["narx"]), reverse=True)  # Eng kattasidan kichigiga
        elif sort_choice == translations[language]["sort_price_desc"]:
            return sorted(phone_list, key=lambda x: clean_price(x["narx"]))  # Eng kichigidan kattasiga
        elif sort_choice == translations[language]["sort_date"]:
            return sorted(phone_list, key=lambda x: datetime.strptime(x["sana"], "%d/%m/%Y"),
                          reverse=True)  # Eng yangi sanadan eski sanaga

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
            messagebox.showerror("Xatolik", "Iltimos, telefon tanlang!")
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
        info_frame = tk.LabelFrame(select_window, text="Telefon haqida", 
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
                    text="Sotish",
                    command=lambda: sell_phone(tree), 
                    fg_color="#34eb6b",
                    hover_color="#2bc456",
                    width=120,
                    height=40).pack(side=tk.LEFT, padx=5)
                    
        # Chop etish tugmasi  
        ctk.CTkButton(btn_frame,
                    text="Chop etish",
                    command=lambda: [print_selected_phone(tree), select_window.destroy()],
                    fg_color="#3498db", 
                    hover_color="#2980b9",
                    width=120,
                    height=40).pack(side=tk.LEFT, padx=5)
                    
        # Yopish tugmasi
        ctk.CTkButton(btn_frame,
                    text="Yopish",
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
            text="Sotish", 
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
            text="Sotuvga utish",
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
                            text="🖨️ Chop etish",
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

    def generate_report():
        # Hisobot yaratish kodini qo'shish mumkin
        messagebox.showinfo("Hisobot", "Hisobot yaratildi!")

    report_btn = tk.Button(btn_frame, text=translations[language]["generate_report"],
                          bg=colors["button_bg"], fg=colors["button_fg"],
                          font=("Arial", 10, "bold"), command=generate_report)
    report_btn.pack(side=tk.LEFT, padx=5)

    close_btn = tk.Button(btn_frame, text=translations[language]["close"],
                         bg="#FF6B6B", fg="white", font=("Arial", 10),
                         command=stats_window.destroy)
    close_btn.pack(side=tk.LEFT, padx=5)




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
    summary_window.title("Savdo statistikasi")
    summary_window.geometry("800x600")
    summary_window.configure(bg=colors["bg"])
    center_window(summary_window)

    # Sarlavha
    header = tk.Label(summary_window, text="📊 Savdo statistikasi",
                     font=("Arial", 16, "bold"), bg=colors["bg"], fg=colors["fg"])
    header.pack(pady=(15, 10))

    # Jadval
    table_frame = tk.Frame(summary_window, bg=colors["bg"])
    table_frame.pack(pady=10, padx=20, fill="both", expand=True)

    columns = ("id", "phone", "model", "price", "date")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")
    
    tree.heading("id", text="ID")
    tree.heading("phone", text="Telefon nomi")
    tree.heading("model", text="IMEI")
    tree.heading("price", text="Narxi")
    tree.heading("date", text="Sotilgan sana")

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
                          text="Davrni tanlang",
                          bg=colors["bg"],
                          fg=colors["fg"],
                          font=("Arial", 12),
                          justify=tk.LEFT)
    stats_label.pack(pady=10)

    # Yopish tugmasi
    close_btn = tk.Button(summary_window,
                         text="Yopish",
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


import tkinter as tk
from tkinter import messagebox, ttk
import customtkinter as ctk
import json
import re
from datetime import datetime

def sell_phone(tree=None):
    """Tanlangan telefonni sotish funksiyasi - tuzatilgan versiya"""
    global sold_phones, phones
    
    if tree is None:
        messagebox.showerror("Xatolik", "Telefonlar jadvali topilmadi!")
        return

    def get_selected_phone():
        """Tanlangan telefonni to'g'ri olish"""
        try:
            selected_items = tree.selection()
            if not selected_items:
                messagebox.showerror("Xatolik", "Iltimos, telefonni tanlang!")
                return None, None, None
            
            # Birinchi tanlangan elementni olish
            selected_item = selected_items[0]
            values = tree.item(selected_item)['values']
            
            if not values or len(values) < 2:
                messagebox.showerror("Xatolik", "Telefon ma'lumotlari topilmadi!")
                return None, None, None
            
            # Indeksni to'g'ri olish (2-ustun indeks bo'lishi kerak)
            try:
                index = int(values[0]) - 1  # 1-dan boshlanuvchi indeksni 0-dan boshlanuvchiga o'tkazish
                if index < 0 or index >= len(phones):
                    raise IndexError("Noto'g'ri telefon indeksi")
                
                phone = phones[index]
                
                # Narxni to'g'ri olish
                price_str = str(phone.get('narx', '0'))
                cleaned_price = re.sub(r"[^\d.]", "", price_str)
                if not cleaned_price:
                    raise ValueError("Narx formati noto'g'ri")
                original_price = float(cleaned_price)
                
                return phone, original_price, index
                
            except (IndexError, ValueError) as e:
                messagebox.showerror("Xatolik", f"Telefon ma'lumotlarini olishda xatolik: {str(e)}")
                return None, None, None
                
        except Exception as e:
            messagebox.showerror("Xatolik", f"Kutilmagan xatolik: {str(e)}")
            return None, None, None

    # Telefon ma'lumotlarini olish
    phone_data, original_price, phone_index = get_selected_phone()
    if phone_data is None:
        return

    # Zamonaviy sotish oynasi
    sell_window = ctk.CTkToplevel()
    sell_window.title("📱 Telefon Sotish")
    sell_window.geometry("600x750")
    sell_window.configure(fg_color=("#f0f0f0", "#1a1a1a"))
    
    # Oynani markazlashtirish
    sell_window.update_idletasks()
    x = (sell_window.winfo_screenwidth() // 2) - (600 // 2)
    y = (sell_window.winfo_screenheight() // 2) - (750 // 2)
    sell_window.geometry(f"600x750+{x}+{y}")
    
    # Oynani modal qilish
    sell_window.transient()
    sell_window.grab_set()
    sell_window.focus_set()

    # Asosiy sarlavha
    title_label = ctk.CTkLabel(
        sell_window,
        text="📱 Telefon Sotish",
        font=ctk.CTkFont(size=28, weight="bold"),
        text_color=("#2c3e50", "#ecf0f1")
    )
    title_label.pack(pady=(20, 30))

    # Telefon ma'lumotlari frame
    info_frame = ctk.CTkFrame(sell_window)
    info_frame.pack(pady=(0, 20), padx=30, fill="x")

    info_title = ctk.CTkLabel(
        info_frame,
        text="📋 Telefon Ma'lumotlari",
        font=ctk.CTkFont(size=18, weight="bold"),
        text_color=("#34495e", "#bdc3c7")
    )
    info_title.pack(pady=(15, 10))

    # Telefon tafsilotlari
    nomi = phone_data.get('nomi', "Noma'lum")
    modeli = phone_data.get('modeli', "Noma'lum")

    details_text = (
        f"📱 Telefon: {nomi}\n"
        f"🔢 IMEI: {modeli}\n"
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
        text="💰 Narx Ma'lumotlari",
        font=ctk.CTkFont(size=18, weight="bold"),
        text_color=("#34495e", "#bdc3c7")
    )
    price_title.pack(pady=(15, 10))

    # Sotish narxi input
    price_label = ctk.CTkLabel(
        price_frame,
        text="Sotish Narxi ($):",
        font=ctk.CTkFont(size=14),
        text_color=("#2c3e50", "#ecf0f1")
    )
    price_label.pack(pady=(5, 5))

    price_entry = ctk.CTkEntry(
        price_frame,
        placeholder_text="Sotish narxini kiriting",
        font=ctk.CTkFont(size=14),
        height=40,
        width=200
    )
    price_entry.insert(0, str(original_price))
    price_entry.pack(pady=(0, 10))

    # Foyda/zarar ko'rsatkichi
    profit_label = ctk.CTkLabel(
        price_frame,
        text="💹 Foyda/Zarar: $0.00",
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
                text="❌ Noto'g'ri narx",
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
        text="👤 Mijoz Ismi:",
        font=ctk.CTkFont(size=14),
        text_color=("#2c3e50", "#ecf0f1")
    )
    name_label.pack(pady=(5, 5))

    customer_name = ctk.CTkEntry(
        customer_frame,
        placeholder_text="Mijoz ismini kiriting",
        font=ctk.CTkFont(size=14),
        height=40,
        width=300
    )
    customer_name.pack(pady=(0, 10))

    # Mijoz telefoni
    phone_label = ctk.CTkLabel(
        customer_frame,
        text="📞 Telefon Raqami:",
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
                messagebox.showerror("Xatolik", "Sotish narxini kiriting!")
                return
                
            sell_price = float(sell_price_str)
            if sell_price <= 0:
                messagebox.showerror("Xatolik", "Sotish narxi 0 dan katta bo'lishi kerak!")
                return
            
            # Mijoz ma'lumotlarini tekshirish
            customer_info = {
                "name": customer_name.get().strip(),
                "phone": customer_phone.get().strip()
            }
            
            if not customer_info["name"]:
                messagebox.showerror("Xatolik", "Mijoz ismini kiriting!")
                customer_name.focus()
                return
                
            if not customer_info["phone"]:
                messagebox.showerror("Xatolik", "Mijoz telefon raqamini kiriting!")
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

            if messagebox.askyesno("✅ Tasdiqlash", confirm_text):
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
                    messagebox.showerror("❌ Xatolik", f"Saqlashda xatolik yuz berdi:\n{str(e)}")

        except ValueError:
            messagebox.showerror("❌ Xatolik", "Noto'g'ri narx formati!\nFaqat raqam kiriting.")
        except Exception as e:
            messagebox.showerror("❌ Xatolik", f"Kutilmagan xatolik:\n{str(e)}")

    # Tugmalar frame
    btn_frame = ctk.CTkFrame(sell_window, fg_color="transparent")
    btn_frame.pack(pady=20)

    # Sotish tugmasi
    sell_btn = ctk.CTkButton(
        btn_frame,
        text="✅ Sotish",
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
        text="❌ Bekor qilish",
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
    sell_window.bind('<KPEnter>', on_enter)  # Numpad Enter
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

def save_sold_phones():
    """Sotilgan telefonlar ma'lumotlarini saqlash funksiyasi"""
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
        messagebox.showerror("Xatolik", "sotish_file.py fayli topilmadi!")
    except Exception as e:
        messagebox.showerror("Xatolik", f"Xatolik yuz berdi: {str(e)}")


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
            messagebox.showerror("Xatolik", "Sotilgan yoki o'chirilgan telefonlar mavjud emas!")
            return

        # Asosiy oyna
        history_window = tk.Toplevel(root_app)
        history_window.title("Telefon tarixi")
        history_window.state("zoomed")
        history_window.configure(bg=colors["bg"])
        history_window.transient(root_app)
        center_window(history_window)

        # Sarlavha
        header = tk.Label(history_window, text="📱 Telefon tarixi",
                        font=("Arial", 16, "bold"), bg=colors["bg"], fg=colors["fg"])
        header.pack(pady=(15, 10))

        # Qidiruv paneli
        search_frame = tk.Frame(history_window, bg=colors["bg"])
        search_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(search_frame, text="Qidirish:",
                bg=colors["bg"], fg=colors["fg"]).pack(side=tk.LEFT, padx=(0, 5))

        search_var = tk.StringVar()
        search_entry = ctk.CTkEntry(search_frame, 
                                  textvariable=search_var,
                                  width=300,
                                  height=35,
                                  placeholder_text="Qidirish uchun matn kiriting...")
        search_entry.pack(side=tk.LEFT, padx=5)

        # Jadval
        table_frame = tk.Frame(history_window, bg=colors["bg"])
        table_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Jadval ustunlari
        columns = (
            "id", "nomi", "modeli", "asl_narx", "sotish_narx", "foyda", 
            "mijoz_ismi", "mijoz_telefon", "holat", "sana"
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
            
            stats_text = (
                f"Jami: {len(all_history)} dona | "
                f"Sotilgan: {len(sold_phones)} dona (${total_sold:.2f}) | "
                f"O'chirilgan: {len(deleted_phones)} dona (${total_deleted:.2f}) | "
                f"Umumiy: ${(total_sold + total_deleted):.2f}"
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
            text="Yopish",
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
        print_file.view_print_screen()

    redirect_to_print_file()
def view_print_screen():
    
#    return print_file.view_print_screen()
    
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
                         text="🖨️ Chop etish",
                         command=print_selected,
                         bg=colors["button_bg"],
                         fg=colors["button_fg"],
                         font=("Arial", 12, "bold"))
    print_btn.pack(side=tk.LEFT, padx=5)

    # Yopish tugmasi
    close_btn = tk.Button(btn_frame, 
                         text="Yopish",
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
        file_path = os.path.join(os.path.dirname(__file__), "print_file.py")

        # pythonni tuliq yuli bilan ishga tushirish
        python_exe = sys.executable
        subprocess.Popen([python_exe, file_path])
    except FileNotFoundError:
        messagebox.showerror("Xatolik", "printer_file.py fayli topilmadi!")
    except Exception as e:
        messagebox.showerror("Xatolik", f"Xatolik yuz berdi: {str(e)}")

############################
def search_phone_by_imei():
    """IMEI raqamning oxirgi 4 ta raqami orqali telefonni qidirish"""
    search_window = tk.Toplevel(root_app)
    search_window.title("Telefon qidirish")
    search_window.geometry("500x400")
    search_window.configure(bg=colors["bg"])
    center_window(search_window)
    
    # Sarlavha
    header = tk.Label(search_window, text="🔍 IMEI orqali telefon qidirish",
                      font=("Arial", 16, "bold"), bg=colors["bg"], fg=colors["fg"])
    header.pack(pady=(15, 20))
    
    # Qidiruv formasi
    search_frame = tk.Frame(search_window, bg=colors["bg"])
    search_frame.pack(pady=10, padx=20, fill="x")
    
    tk.Label(search_frame, text="IMEI oxirgi 4 raqam:", bg=colors["bg"], fg=colors["fg"],
             font=("Arial", 12)).pack(side=tk.LEFT, padx=(0, 10))
    
    search_entry = tk.Entry(search_frame, font=("Arial", 12), width=15,
                           bg=colors["entry_bg"], fg=colors["entry_fg"])
    search_entry.pack(side=tk.LEFT, padx=(0, 10))
    search_entry.focus()  # Kursor qidiruv maydoniga joylashadi
    
    # Natijalar uchun jadval
    result_frame = tk.Frame(search_window, bg=colors["bg"])
    result_frame.pack(pady=10, padx=20, fill="both", expand=True)
    
    # Scrollable frame for results
    results_canvas = tk.Canvas(result_frame, bg=colors["bg"], highlightthickness=0)
    results_canvas.pack(side=tk.LEFT, fill="both", expand=True)
    
    scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=results_canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill="y")
    
    results_canvas.configure(yscrollcommand=scrollbar.set)
    
    results_frame = tk.Frame(results_canvas, bg=colors["bg"])
    results_canvas.create_window((0, 0), window=results_frame, anchor="nw")
    
    results_frame.bind("<Configure>", lambda e: results_canvas.configure(scrollregion=results_canvas.bbox("all")))
    
    # Qidiruv natijalarini ko'rsatish
    def display_results(search_text):
        # Avvalgi natijalarni o'chirish
        for widget in results_frame.winfo_children():
            widget.destroy()
        
        if not search_text:
            tk.Label(results_frame, text="IMEI raqamning oxirgi 4 ta raqamini kiriting",
                    bg=colors["bg"], fg=colors["fg"], font=("Arial", 12)).pack(pady=10)
            return
        
        # Telefonlar ro'yxatidan qidirish
        found_phones = []
        
        # Avval faol telefonlar ichidan qidirish
        for phone in phones:
            imei = phone["modeli"]
            if imei[-4:] == search_text:
                found_phones.append((phone, "active"))
        
        # Sotilgan telefonlar ichidan qidirish
        for phone in sold_phones:
            imei = phone["modeli"]
            if imei[-4:] == search_text:
                found_phones.append((phone, "sold"))
        
        if not found_phones:
            tk.Label(results_frame, text=f"'{search_text}' raqamli IMEI bilan telefon topilmadi.",
                    bg=colors["bg"], fg="#FF6B6B", font=("Arial", 12)).pack(pady=10)
            return
        
        # Topilgan telefonlarni ko'rsatish
        tk.Label(results_frame, text=f"{len(found_phones)} ta natija topildi:",
                bg=colors["bg"], fg=colors["fg"], font=("Arial", 12, "bold")).pack(pady=(10, 15), anchor="w")
        
        for i, (phone, status) in enumerate(found_phones):
            # Har bir telefon uchun alohida panel
            phone_frame = tk.Frame(results_frame, bg="#ffffff", bd=1, relief=tk.SOLID)
            phone_frame.pack(fill="x", pady=5, padx=5)
            
            # Telefon ma'lumotlari
            info_frame = tk.Frame(phone_frame, bg="#ffffff")
            info_frame.pack(fill="x", padx=10, pady=10)
            
            # Sarlavha - telefon nomi va holati
            status_text = "✅ Mavjud" if status == "active" else "💰 Sotilgan"
            status_color = "#4CAF50" if status == "active" else "#FF9800"
            
            header_frame = tk.Frame(info_frame, bg="#ffffff")
            header_frame.pack(fill="x", pady=(0, 5))
            
            tk.Label(header_frame, text=phone["nomi"], bg="#ffffff", fg="#333333",
                    font=("Arial", 12, "bold")).pack(side=tk.LEFT)
            
            tk.Label(header_frame, text=status_text, bg=status_color, fg="white",
                    font=("Arial", 10), padx=5, pady=2).pack(side=tk.RIGHT)
            
            # IMEI va narx
            details_frame = tk.Frame(info_frame, bg="#ffffff")
            details_frame.pack(fill="x", pady=2)
            
            tk.Label(details_frame, text=f"IMEI: {phone['modeli']}", bg="#ffffff", fg="#666666",
                    font=("Arial", 11)).pack(side=tk.LEFT, padx=(0, 20))
            
            tk.Label(details_frame, text=f"Narx: {phone['narx']}", bg="#ffffff", fg="#666666",
                    font=("Arial", 11)).pack(side=tk.LEFT)
            
            # Sana
            date_frame = tk.Frame(info_frame, bg="#ffffff")
            date_frame.pack(fill="x", pady=2)
            
            date_label = "Qo'shilgan sana: " if status == "active" else "Sotilgan sana: "
            tk.Label(date_frame, text=f"{date_label}{phone['sana']}", bg="#ffffff", fg="#666666",
                    font=("Arial", 11)).pack(side=tk.LEFT)
            
            # Amallar uchun tugmalar
            if status == "active":
                # Mavjud telefon uchun sotish tugmasi
                def sell_this_phone(phone_idx):
                    search_window.destroy()
                    # Kerakli telefon indeksini o'rnatish
                    idx = -1
                    for i, p in enumerate(phones):
                        if p["modeli"] == phone["modeli"]:
                            idx = i
                            break
                    
                    if idx != -1:
                        # Telefonni tanlash
                        phone_tree.selection_set(phone_tree.get_children()[idx])
                        # Sotish funksiyasini chaqirish
                        sell_phone()
                
                # Telefon indeksini topish
                for i, p in enumerate(phones):
                    if p["modeli"] == phone["modeli"]:
                        # break4

                    # ...existing code...
    
                        for i, (phone, status) in enumerate(found_phones):
                            if status == "active":
                                phone_frame = tk.Frame(results_frame, bg="#ffffff", bd=1, relief=tk.SOLID)
                                phone_frame.pack(fill="x", pady=5, padx=5)
                                
                                info_frame = tk.Frame(phone_frame, bg="#ffffff")
                                info_frame.pack(fill="x", padx=10, pady=10)
                                
                                # ...phone info labels...
                                
                                # Sotish tugmasi
                                def sell_this_phone_action(phone_data):
                                    def confirm_and_sell():
                                        # Mijoz ma'lumotlarini so'rash
                                        customer_name = simpledialog.askstring("Mijoz ismi", "Mijoz ismini kiriting:", parent=search_window)
                                        if not customer_name:
                                            return
                                        customer_phone = simpledialog.askstring("Mijoz telefoni", "Mijoz telefon raqamini kiriting:", parent=search_window)
                                        if not customer_phone:
                                            return
                                        sell_price = simpledialog.askstring("Sotish narxi", "Sotish narxini kiriting ($ bilan):", parent=search_window)
                                        if not sell_price:
                                            return
                                        try:
                                            # Narxni float ga o'tkazish
                                            sell_price_val = float(str(sell_price).replace("$", "").strip())
                                            original_price_val = float(re.sub(r"[^\d.]", "", str(phone_data['narx'])))
                                            profit = sell_price_val - original_price_val
                                        except Exception:
                                            messagebox.showerror("Xatolik", "Noto'g'ri narx kiritildi!")
                                            return

                                        confirm_text = (
                                            f"Sotish ma'lumotlari:\n\n"
                                            f"Telefon: {phone_data['nomi']}\n"
                                            f"IMEI: {phone_data['modeli']}\n"
                                            f"Asl narx: {phone_data['narx']}\n"
                                            f"Sotish narx: ${sell_price_val:.2f}\n"
                                            f"Foyda: ${profit:.2f}\n\n"
                                            f"Mijoz: {customer_name}\n"
                                            f"Telefon: {customer_phone}\n\n"
                                            f"Sotishni tasdiqlaysizmi?"
                                        )
                                        if not messagebox.askyesno("Tasdiqlash", confirm_text, parent=search_window):
                                            return

                                        # Sotilganlar ro'yxatiga qo'shish
                                        sale_record = {
                                            "nomi": phone_data["nomi"],
                                            "modeli": phone_data["modeli"],
                                            "asl_narx": phone_data["narx"],
                                            "sotish_narx": f"${sell_price_val:.2f}",
                                            "foyda": f"${profit:.2f}",
                                            "sotilgan_sana": datetime.now().strftime("%d/%m/%Y"),
                                            "mijoz_ismi": customer_name,
                                            "mijoz_telefon": customer_phone
                                        }
                                        try:
                                            # Faylga yozish
                                            try:
                                                with open("sotish_file.json", 'r', encoding='utf-8') as f:
                                                    sales_data = json.load(f)
                                            except (FileNotFoundError, json.JSONDecodeError):
                                                sales_data = []
                                            sales_data.append(sale_record)
                                            with open("sotish_file.json", 'w', encoding='utf-8') as f:
                                                json.dump(sales_data, f, ensure_ascii=False, indent=4)
                                        except Exception:
                                            pass
                                        # phones dan o'chirish va sold_phones ga qo'shish
                                        for idx, p in enumerate(phones):
                                            if p["modeli"] == phone_data["modeli"]:
                                                phones.pop(idx)
                                                break
                                        sold_phones.append(sale_record)
                                        save_data()
                                        save_sold_phones()
                                        messagebox.showinfo("Muvaffaqiyatli", f"{phone_data['nomi']} muvaffaqiyatli sotildi!", parent=search_window)
                                        search_window.destroy()

                                    sell_btn = tk.Button(info_frame,
                                                        text="Sotish",
                                                        command=on_sell_click,
                                                        bg="#4CAF50",
                                                        fg="white",
                                                        font=("Arial", 10, "bold"),
                                                        padx=10)
                                    sell_btn.pack(anchor="e", pady=(5, 0))

                                sell_this_phone_action(phone)
    
    # Qidiruv tugmasi bosilganda
    def search():
        search_text = search_entry.get().strip()
        if len(search_text) > 4:
            search_text = search_text[-4:]  # Faqat oxirgi 4 ta raqamni olish
            search_entry.delete(0, tk.END)
            search_entry.insert(0, search_text)
        
        display_results(search_text)
    
    # Qidiruv tugmasi
    search_btn = tk.Button(search_frame, text="Qidirish", command=search,
                          bg=colors["button_bg"], fg=colors["button_fg"],
                          font=("Arial", 12))
    search_btn.pack(side=tk.LEFT)
    
    # Enter tugmasi bosilganda ham qidirish
    search_entry.bind("<Return>", lambda event: search())
    
    # Dastlabki ko'rinish
    tk.Label(results_frame, text="IMEI raqamning oxirgi 4 ta raqamini kiriting",
            bg=colors["bg"], fg=colors["fg"], font=("Arial", 12)).pack(pady=10)
    
    # Yopish tugmasi
    close_btn = tk.Button(search_window, text="Yopish", command=search_window.destroy,
                         bg="#FF6B6B", fg="white", font=("Arial", 12))
    close_btn.pack(pady=15)
############################

# Asosiy dastur oynasi
def main_application():   
    global root_app

    root_app = tk.Tk()
    root_app.title(translations[language]["title"])
    root_app.state('zoomed')
    root_app.configure(bg=colors["bg"])

    # Oynani o'rta joylashtirish
    center_window(root_app)

    # Menu
    menubar = tk.Menu(root_app)
    root_app.config(menu=menubar)

    # Telefon menu
    phone_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label=translations[language]["phone_menu"], menu=phone_menu)
    phone_menu.add_command(label=translations[language]["add_phone"], command=add_phone)
    phone_menu.add_command(label=translations[language]["delete_phone"], command=delete_phone)
    phone_menu.add_command(label=translations[language]["view_phones"], command=view_phones)
    phone_menu.add_separator()
    phone_menu.add_command(label=translations[language]["phone_stats"], command=show_phone_stats)

    # Ma'lumot menu
    info_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label=translations[language]["info_menu"], menu=info_menu)
    info_menu.add_command(label=translations[language]["save_data"], command=save_data)
    info_menu.add_command(label=translations[language]["load_data"], command=load_data)
    info_menu.add_separator()
    info_menu.add_command(label=translations[language]["about"], command=show_about)

    # Sozlamalar menu
    settings_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label=translations[language]["settings"], menu=settings_menu)

    # Til menu
    settings_menu.add_command(label=translations[language]["change_language"], command=change_language)


    # Tungi rejim menu
    settings_menu.add_command(label=translations[language]["toggle_dark_mode"], command=toggle_dark_mode)

    # Mavzu menu
    theme_menu = tk.Menu(settings_menu, tearoff=0)
    settings_menu.add_cascade(label=translations[language]["theme"], menu=theme_menu)
    theme_menu.add_command(label=translations[language]["classic"], command=lambda: change_theme("classic"))
    theme_menu.add_command(label=translations[language]["blue"], command=lambda: change_theme("blue"))
    theme_menu.add_command(label=translations[language]["green"], command=lambda: change_theme("green"))

    theme_menu.add_command(label=translations[language]["white"], command=lambda: change_theme("white"))
    theme_menu.add_command(label=translations[language]["black"], command=lambda: change_theme("black"))

    # Login tugmasi
    settings_menu.add_separator()
    settings_menu.add_command(label=translations[language]["login"], command=show_login_screen)

    # Asosiy soha
    main_frame = tk.Frame(root_app, bg=colors["bg"])
    main_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Logo/sarlavha
    title_label = tk.Label(main_frame, text=translations[language]["title"],
                           font=("Arial", 24, "bold"), bg=colors["bg"], fg=colors["fg"])
    title_label.pack(pady=20)

    # Tugmalar paneli
    button_frame = tk.Frame(main_frame, bg=colors["bg"])
    button_frame.pack(pady=20)

    # tugmalar uchun chap tomon va o'ng tomon paneli
# Left button frame styling
    left_button_frame = ctk.CTkFrame(
        main_frame,
        fg_color="#2c3e50",  # To'q ko'k rang
        corner_radius=15,
        border_width=2,
        border_color="#34495e",
        width=400,
        height=800
    )
    left_button_frame.pack(
        side=tk.LEFT, 
        pady=20, 
        padx=50, 
        anchor="nw",
        fill="both",
        expand=True
    )
 # Right button frame styling
    right_button_frame = ctk.CTkFrame(
        main_frame,
        fg_color="#2c3e50",  # Och sariq rang
        corner_radius=15,
        border_width=2,
        border_color="#2c3e50",  # To'qroq sariq chegara
        width=400,
        height=800
    )
    right_button_frame.pack(
        side=tk.RIGHT, 
        pady=20, 
        padx=50, 
        anchor="nw",
        fill="both",
        expand=True
    )   # Tugmalarni yaratish
 
    # left buttons
    left_buttons = [
        (translations[language]["add_phone"], add_phone),
        (translations[language]["delete_phone"], delete_phone),
        (translations[language]["view_phones"], view_phones),
        ("📱 Sotilgan telefonlar", open_sales_file), 
        ("📊 Telefon tarixi", view_all_history),
        (translations[language]["phone_stats"], show_phone_stats),
        ("🖨️ Chop etish", view_print_screen),  # Add this new button
        ("🖨️ Printer bulimi", printer_file_ochish),  # Add this new button
        ("Qidiruv", search_phone_by_imei),
    ]
    right_buttons = [

        ("bush bo'lim", None)

    ]

# Left buttons styling
    for text, command in left_buttons:
        btn = ctk.CTkButton(
            left_button_frame,
            text=text,
            command=command,
            fg_color="#3498db",  # Asosiy ko'k rang
            hover_color="#2980b9",  # Hover uchun to'qroq ko'k
            text_color="white",
            font=("Arial", 16, "bold"),
            width=320,
            height=55,
            corner_radius=10,
            border_width=2,
            border_color="#2980b9"
        )
        btn.pack(pady=15, padx=20, anchor="center")
    # create right buttons
# Right buttons styling
    for text, command in right_buttons:
        btn = ctk.CTkButton(
            right_button_frame,
            text=text,
            command=command,
            fg_color="#3498db",  # Asosiy tugma rangi (to'qroq sariq)
            hover_color="#2980b9",  # Hover uchun rang
            text_color="white",  # Qora yozuv
            font=("Arial", 16, "bold"),
            width=320,
            height=55,
            corner_radius=10,
            border_width=2,
            border_color="#2980b9"
        )
        btn.pack(pady=15, padx=20, anchor="center")

    #     # Login oynasini yaratish va tekshirish
    # login_screen = LoginWindow()
    # if show_login_screen.login_action():
    #     # Agar login muvaffaqiyatsiz bo'lsa dastur yopiladi
    #     sys.exit()
        



    # ...existing code (menu, buttons, etc.)...

    # Ma'lumotlarni avtomatik yuklash
    load_data()
    # sotilgan telefonlar
    load_sold_phones() 

    # Asosiy tsikl
    root_app.mainloop()
    
    # ...existing code (button_frame and other elements)...

    load_sold_phones()  # Sotilgan telefonlarni yuklash

    # Ma'lumotlarni avtomatik yuklash
    load_data()

    # Asosiy tsikl
    root_app.mainloop()

    show_login_screen()
    pass


if __name__ == "__main__":       
    main_application()



