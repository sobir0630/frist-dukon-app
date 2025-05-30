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
import win32print
import win32ui
from PIL import Image, ImageDraw
import subprocess
import os
import sys
import subprocess
from tkinter import messagebox


# Global ma'lumotlar
phones = []  # Har bir telefon: {"nomi": ..., "modeli": ..., "sana": ..., "narx": ...}
language = "uz"  # Dastur standarti – o'zbek tili
dark_mode = True
data_file = "telefon_data.json"  # Ma'lumotlarni saqlash uchun fayl

# Tarjimalar (O'zbek va Rus)
translations = {
    "uz": {
        "title": "Telefon Do'koni Dasturi",
        "phone_menu": "Telefon tovarlar",
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
        "phone_image": "Telefon rasmi",
        "about": "Dastur haqida",
        "total_price": "Jami narx:",
        "about_text": "Telefon Do'koni Dasturi\nVersiya 2.0\n\nDastur telefon do'konidagi tovarlarni boshqarish uchun yaratilgan.\n\n©2025 Barcha huquqlar himoyalangan."
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
        "phone_image": "Изображение телефона",
        "about": "О программе",
        "total_price": "Общая сумма:",
        "about_text": "Программа магазина телефонов\nВерсия 2.0\n\nПрограмма создана для управления товарами в магазине телефонов.\n\n©2025 Все права защищены."
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
    }
    
}

# Joriy mavzu
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
def change_theme(theme_name):
    global current_theme, colors
    current_theme = theme_name
    colors = themes[current_theme]["dark" if dark_mode else "light"]
    # Mavzuni qo'llash kodlari (root_app configuratsiyasi)
    if 'root_app' in globals():
        root_app.configure(bg=colors["bg"])
        # Boshqa UI elementlarini yangilash...


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



# Excel formatiga eksport qilish funksiyasi (qo'shildi)
def export_to_excel():
    try:
        # Bu joyda Excel faylni yaratish logikasi bo'lishi kerak
        # Misol: pandas, xlsxwriter, openpyxl kabilardan foydalanish
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx")],
            title=translations[language]["export_excel"]
        )

        if file_path:
            # Excel faylni yaratish va saqlash (bu yerda faqat namoyish uchun)
            # Bu joyda haqiqiy Excel fayl yaratish kodlari bo'lishi kerak
            time.sleep(1)  # Ma'lumotlar eksport qilinayotgani taqlid
            messagebox.showinfo(translations[language]["success"], translations[language]["export_success"])
    except Exception as e:
        messagebox.showerror(translations[language]["error"], str(e))


# def login_action():
#     username_input = username_entry.get()
#     password_input = password_entry.get()

#     # Foydalanuvchi ma’lumotlari
#     CORRECT_USERNAME = "Sobir"
#     CORRECT_PASSWORD = "0630"    

#     if username_input == CORRECT_USERNAME and password_input == CORRECT_PASSWORD:
#         login_window.destroy()  # Login oynasini yopish
#         main_application()  # Asosiy menu ochish
#     else:
#         messagebox.showerror("Xatolik", "Login yoki parol noto‘g‘ri!")


# # Login oynasini yaratish
# login_window = tk.Tk()
# login_window.title("Login")
# login_window.geometry("300x200")

# # Foydalanuvchi login oynasidan chiqmasligi uchun X tugmasini bloklash
# def on_closing():
#     if messagebox.askokcancel("Chiqish", "Dasturdan chiqishni xohlaysizmi?"):
#         login_window.destroy()
#         sys.exit()  # Dasturdan butunlay chiqish
#         sys.exit()  # Dasturdan butunlay chiqish
        

# # X tugmasi bosilganda on_closing funksiyasini chaqirish
# login_window.protocol("WM_DELETE_WINDOW", on_closing)


# tk.Label(login_window, text="Username:").pack()
# username_entry = tk.Entry(login_window)
# username_entry.pack()

# tk.Label(login_window, text="Password:").pack()
# password_entry = tk.Entry(login_window, show="*")  # Parolni yashirish
# password_entry.pack()

# login_btn = tk.Button(login_window, text="Login", command=login_action)
# login_btn.pack(pady=10)

# login_window.mainloop()


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


# Telefon qo'shish funksiyasi
def add_phone():
    add_window = tk.Toplevel(root_app)
    add_window.title(translations[language]["add_phone"])
    add_window.geometry("500x480")
    add_window.configure(bg=colors["bg"])
    add_window.resizable(False, False)
    add_window.transient(root_app)
    add_window.grab_set()

    # Formani o'rta joylashtirish
    center_window(add_window)

    # Formani yaratish
    form_frame = tk.Frame(add_window, bg=colors["bg"], bd=1, relief=tk.GROOVE)
    form_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Sarlavha
    header = tk.Label(form_frame, text=translations[language]["add_phone"],
                      font=("Arial", 14, "bold"), bg=colors["bg"], fg=colors["fg"])
    header.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")

    # Formadagi maydonlar
    tk.Label(form_frame, text=translations[language]["enter_name"],
             bg=colors["bg"], fg=colors["fg"], font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=8, padx=10)
    name_entry = tk.Entry(form_frame, bg=colors["entry_bg"], fg=colors["entry_fg"],
                          font=("Arial", 10), width=25)
    name_entry.grid(row=1, column=1, pady=8, padx=10, sticky="ew")

    tk.Label(form_frame, text=translations[language]["enter_model"],
             bg=colors["bg"], fg=colors["fg"], font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=8, padx=10)
    model_entry = tk.Entry(form_frame, bg=colors["entry_bg"], fg=colors["entry_fg"],
                           font=("Arial", 10), width=25)
    model_entry.grid(row=2, column=1, pady=8, padx=10, sticky="ew")





    tk.Label(form_frame, text=translations[language]["enter_date"],
             bg=colors["bg"], fg=colors["fg"], font=("Arial", 10)).grid(row=3, column=0, sticky="w", pady=8, padx=10)
    date_frame = tk.Frame(form_frame, bg=colors["bg"])
    date_frame.grid(row=3, column=1, pady=8, padx=10, sticky="ew")

    date_entry = tk.Entry(date_frame, bg=colors["entry_bg"], fg=colors["entry_fg"],
                          font=("Arial", 10), width=15)
    date_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

    # Bugungi sanani olish tugmasi
    def set_today_date():
        today = datetime.now().strftime("%d/%m/%Y")
        date_entry.delete(0, tk.END)
        date_entry.insert(0, today)

    today_btn = tk.Button(date_frame, text=translations[language]["today"],
                          bg=colors["button_bg"], fg=colors["button_fg"],
                          font=("Arial", 8), command=set_today_date)
    today_btn.pack(side=tk.RIGHT, padx=(5, 0))

    tk.Label(form_frame, text=translations[language]["enter_price"],
             bg=colors["bg"], fg=colors["fg"], font=("Arial", 10)).grid(row=4, column=0, sticky="w", pady=8, padx=10)
    price_entry = tk.Entry(form_frame, bg=colors["entry_bg"], fg=colors["entry_fg"],
                           font=("Arial", 10), width=25)
    price_entry.grid(row=4, column=1, pady=8, padx=10, sticky="ew")

    # Telefon rasmini tanlash
    tk.Label(form_frame, text=translations[language]["phone_image"],
             bg=colors["bg"], fg=colors["fg"], font=("Arial", 10)).grid(row=5, column=0, sticky="w", pady=8, padx=10)

    # Telefon turini tanlash uchun combo box
    phone_types = ["iPhone", "Samsung", "Xiaomi", "Boshqa"]
    selected_type = tk.StringVar()
    selected_type.set(phone_types[0])

    type_combo = ttk.Combobox(form_frame, textvariable=selected_type, values=phone_types, state="readonly")
    type_combo.grid(row=5, column=1, pady=8, padx=10, sticky="ew")

    # Qo'shish tugmasi
    def save_phone():
        name = name_entry.get().strip()
        model = model_entry.get().strip()
        date = date_entry.get().strip()
        price = price_entry.get().strip()
        # imai = imai_entry.get().strip()  # IMAI raqami qo'shildi
        phone_type = selected_type.get()

        # Bo'sh maydonlarni tekshirish
        if not (name and model and date and price):  # To'g'ri shart
            messagebox.showerror(translations[language]["error"], translations[language]["fill_all"])
            return

        # Animatsiya bilan qo'shish
        progress_window = tk.Toplevel(add_window)
        progress_window.title(translations[language]["add_phone"])
        progress_window.geometry("300x100")
        progress_window.configure(bg=colors["bg"])
        progress_window.resizable(False, False)
        progress_window.transient(add_window)
        progress_window.grab_set()
        center_window(progress_window)

        tk.Label(progress_window, text=f"{name} ({model}) {translations[language]['added']}",
                 bg=colors["bg"], fg=colors["fg"]).pack(pady=(20, 10))

        progress = ttk.Progressbar(progress_window, mode="determinate", length=200)
        progress.pack(pady=10, padx=20)

        def simulate_adding():
            for i in range(101):
                progress["value"] = i
                progress_window.update()
                time.sleep(0.01)

            phone = {"nomi": name, "modeli": model, "sana": date, "narx": price}  # To'g'ri kalit nomlari
            phones.append(phone)
            save_data()  # Ma'lumotlarni avtomatik saqlash
            progress_window.destroy()
            add_window.destroy()

        threading.Thread(target=simulate_adding).start()

    btn_frame = tk.Frame(form_frame, bg=colors["bg"])
    btn_frame.grid(row=6, column=0, columnspan=2, pady=20)

    btn_save = tk.Button(btn_frame, text=translations[language]["add_phone"],
                         bg=colors["button_bg"], fg=colors["button_fg"],
                         font=("Arial", 10, "bold"), command=save_phone, width=15, height=2)
    btn_save.pack(side=tk.LEFT, padx=5)

    btn_cancel = tk.Button(btn_frame, text=translations[language]["close"],
                           bg="#FF6B6B", fg="white",
                           font=("Arial", 10), command=add_window.destroy, width=10, height=2)
    btn_cancel.pack(side=tk.LEFT, padx=5)

    # Enter bosilganda saqlash
    add_window.bind('<Return>', lambda event: save_phone())


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
            del phones[index]
            save_data()
            load_tree_data(search_var.get())
            messagebox.showinfo(translations[language]["success"],
                                f"{phone_name} {translations[language]['deleted']}")

    # Tugmalar
    btn_frame = tk.Frame(delete_window, bg=colors["bg"])
    btn_frame.pack(pady=15, fill="x", padx=20)

    delete_btn = tk.Button(btn_frame, text=translations[language]["delete_phone"],
                           command=confirm_delete, bg="#FF6B6B", fg="white",
                           font=("Arial", 10, "bold"))
    delete_btn.pack(side=tk.LEFT, padx=5)

    close_btn = tk.Button(btn_frame, text=translations[language]["close"],
                          command=delete_window.destroy, bg=colors["button_bg"],
                          fg=colors["button_fg"], font=("Arial", 10))
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

        def save_changes():
            phone["nomi"] = name_entry.get().strip()
            phone["modeli"] = model_entry.get().strip()
            phone["narx"] = price_entry.get().strip()
            phone["sana"] = date_entry.get().strip()

            save_data()
            load_tree_data(search_var.get())
            form_window.destroy()

        save_btn = tk.Button(form_window, text=translations[language]["update"],
                             bg=colors["button_bg"], fg=colors["button_fg"],
                             command=save_changes)
        save_btn.pack(pady=10)

    # Tahrirlash tugmasi
    edit_btn = tk.Button(edit_window, text=translations[language]["edit"],
                         command=open_edit_form, bg=colors["button_bg"],
                         fg=colors["button_fg"], font=("Arial", 10, "bold"))
    edit_btn.pack(pady=15)

    # Yopish tugmasi
    close_btn = tk.Button(edit_window, text=translations[language]["close"],
                          command=edit_window.destroy, bg="#FF6B6B",
                          fg="white", font=("Arial", 10))
    close_btn.pack(pady=5)
    
def view_phones():
    # global tree # add this line

    if not phones:
        messagebox.showerror(translations[language]["error"], translations[language]["no_phones"])
        return

    view_window = tk.Toplevel(root_app)
    view_window.title(translations[language]["view_phones"])
    view_window.geometry("1900x900")
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
    style.configure("Treeview",
                    background=colors["entry_bg"],
                    foreground=colors["entry_fg"],
                    fieldbackground=colors["entry_bg"],
                    font=('Arial', 10))
    style.configure("Treeview.Heading", font=('Arial', 11, 'bold'))

    columns = ("id", "phone", "model", "price", "date")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
    tree.heading("id", text="ID")
    tree.heading("phone", text=translations[language]["phone_name_label"])
    tree.heading("model", text=translations[language]["model_label"])
    tree.heading("price", text=translations[language]["price_label"])
    tree.heading("date", text=translations[language]["date_label"])

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
    def load_tree_data(search_text=""):
        tree.delete(*tree.get_children())
        sorted_phones = sort_phones(phones.copy())

        for i, phone in enumerate(sorted_phones):
            if search_text.lower() in phone["nomi"].lower() or search_text.lower() in phone["modeli"].lower():
                tree.insert("", tk.END, values=(i + 1, phone["nomi"], phone["modeli"], phone["narx"], phone["sana"]))

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

    



    # Tugmalar
    btn_frame = tk.Frame(view_window, bg=colors["bg"])
    btn_frame.pack(pady=15, fill="x", padx=20)

    # Sotish tugmasini tree bilan birga uzatish
    sell_btn = tk.Button(btn_frame, 
                        text="Sotish", 
                        command=lambda: sell_phone(tree),  # tree ni parametr sifatida uzatish
                        bg=colors["button_bg"], 
                        fg=colors["button_fg"], 
                        font=("Arial", 20, "bold"))
    sell_btn.pack(side=tk.LEFT, padx=5)

    tk.Button(btn_frame,
          text="Sotish bo'limi",
          command=open_sales_file,
          bg=colors["button_bg"],
          fg=colors["button_fg"],
          font=("Arial", 12)).pack(side=tk.LEFT, padx=5)

    btn_frame = tk.Frame(view_window, bg=colors["bg"])
    btn_frame.pack(pady=15, fill="x", padx=20)

    sell_btn = tk.Button(btn_frame, text="Sotish", command=sell_phone,
                         bg=colors["button_bg"], fg=colors["button_fg"], font=("Arial", 20, "bold"))
    sell_btn.pack(side=tk.LEFT, padx=5)

    sold_btn = tk.Button(btn_frame, text="Sotilganlar", command=view_sold_phones,
                         bg=colors["button_bg"], fg=colors["button_fg"], font=("Arial", 10, "bold"))
    sold_btn.pack(side=tk.LEFT, padx=5)

    close_btn = tk.Button(btn_frame, text=translations[language]["close"],
                          command=view_window.destroy, bg="#FF6B6B",
                          fg="white", font=("Arial", 10))
    close_btn.pack(side=tk.LEFT, padx=5)



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

def view_sold_phones():
    """Sotilgan telefonlarni ko'rish funksiyasi"""
    if not sold_phones:
        messagebox.showerror(translations[language]["error"], "Sotilgan telefonlar mavjud emas!")
        return

    sold_window = tk.Toplevel(root_app)
    sold_window.title("Sotilgan telefonlar")
    sold_window.state('zoomed')
    sold_window.configure(bg=colors["bg"])
    center_window(sold_window)

    # Sarlavha
    header = tk.Label(sold_window, text="📱 Sotilgan telefonlar ro'yxati",
                      font=("Arial", 16, "bold"), bg=colors["bg"], fg=colors["fg"])
    header.pack(pady=(15, 10))

    # Jadval
    table_frame = tk.Frame(sold_window, bg=colors["bg"])
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

    # Saralash tugmalari va statistika paneli
    stats_frame = tk.Frame(sold_window, bg=colors["bg"])
    stats_frame.pack(fill="x", padx=20, pady=10)
    
    stats_label = tk.Label(stats_frame, text="", bg=colors["bg"], fg=colors["fg"], font=("Arial", 12))
    stats_label.pack(pady=5)

    # Saralash funksiyasi
    def filter_by_days(days):
        """Sotilgan telefonlarni kunlar bo'yicha filtrlash va savdoni hisoblash"""
        tree.delete(*tree.get_children())
        total_sales = 0  # Savdo summasi
        if days is None:  # Hammasini ko'rsatish
            for i, phone in enumerate(sold_phones):
                tree.insert("", tk.END, values=(i + 1, phone["nomi"], phone["modeli"], phone["narx"], phone["sana"]))
                try:
                    total_sales += float(phone["narx"].replace("$", "").strip())
                except:
                    pass
            stats_label.config(text=f"Jami sotilgan telefonlar: {len(sold_phones)} dona | Umumiy savdo: ${total_sales:.2f}")
        else:
            filtered_phones = []
            cutoff_date = datetime.now() - timedelta(days=days - 1) if days > 1 else datetime.now()
            for i, phone in enumerate(sold_phones):
                phone_date = datetime.strptime(phone["sana"], "%d/%m/%Y")
                if phone_date.date() >= cutoff_date.date():
                    filtered_phones.append(phone)
                    tree.insert("", tk.END, values=(i + 1, phone["nomi"], phone["modeli"], phone["narx"], phone["sana"]))
                    try:
                        total_sales += float(phone["narx"].replace("$", "").strip())
                    except:
                        pass
            stats_label.config(text=f"Jami sotilgan telefonlar: {len(filtered_phones)} dona | Oxirgi {days} kun ichida sotilgan telefonlar: {len(filtered_phones)} dona | Savdo: ${total_sales:.2f}")

    # Saralash tugmalari
    sort_frame = tk.Frame(sold_window, bg=colors["bg"])
    sort_frame.pack(fill="x", padx=20, pady=10)

    sort_buttons = [
        ("Bugungi", 1),
        ("Hammasi", None)  # None - barcha sotilgan telefonlarni ko'rsatish
    ]
    
    for text, days in sort_buttons:
        btn = tk.Button(sort_frame,
                       text=text,
                       command=lambda d=days: filter_by_days(d),
                       bg=colors["button_bg"],
                       fg=colors["button_fg"],
                       font=("Arial", 10))
        btn.pack(side=tk.LEFT, padx=5)

    # Skroll
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    # Ma'lumotlarni yuklash 
    total_price = 0
    for i, phone in enumerate(sold_phones):
        tree.insert("", tk.END, values=(i + 1, phone["nomi"], phone["modeli"], phone["narx"], phone["sana"]))
        try:
            price = float(phone["narx"].replace("$", "").strip())
            total_price += price
        except:
            pass

    # Statistika
    stats_frame = tk.Frame(sold_window, bg=colors["bg"])
    stats_frame.pack(pady=10, fill="x", padx=20)

    tk.Label(stats_frame, text=f"Jami sotilgan telefonlar: {len(sold_phones)} dona",
             bg=colors["bg"], fg=colors["fg"], font=("Arial", 12)).pack(side=tk.LEFT, padx=10)
             
    tk.Label(stats_frame, text=f"Umumiy savdo: ${total_price:.2f}",
             bg=colors["bg"], fg=colors["fg"], font=("Arial", 12)).pack(side=tk.RIGHT, padx=10)

    # Yopish tugmasi
    close_button = tk.Button(sold_window, text="Yopish", command=sold_window.destroy,
                            bg="#FF6B6B", fg="white", font=("Arial", 12))
    close_button.pack(pady=15)
    
    # Dastlabki statistikani ko'rsatish
    filter_by_days(None)

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


def sell_phone(tree=None):
    """Tanlangan telefonni sotish funksiyasi"""
    global sold_phones
    if tree is None:
        messagebox.showerror("Xatolik", "Telefonlar jadvali topilmadi!")
        return

    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Xatolik", "Iltimos, telefon tanlang!")
        return

    index = int(tree.item(selected_item)['values'][0]) - 1
    phone = phones[index]
    original_price = float(phone['narx'].replace('$', '').strip())

    # Sotish oynasi
    sell_window = tk.Toplevel(root_app)
    sell_window.title("Telefonni sotish")
    sell_window.geometry("500x600")
    sell_window.configure(bg=colors["bg"])
    center_window(sell_window)

    # Telefon ma'lumotlari
    info_frame = tk.LabelFrame(sell_window, text="Telefon ma'lumotlari",
                             bg=colors["bg"], fg=colors["fg"], font=("Arial", 12))
    info_frame.pack(pady=(20, 10), padx=20, fill="x")

    details_text = f"Telefon: {phone['nomi']}\nIMEI: {phone['modeli']}\nAsl narxi: ${original_price:.2f}"
    tk.Label(info_frame, text=details_text, bg=colors["bg"], fg=colors["fg"],
            font=("Arial", 12), justify=tk.LEFT).pack(padx=10, pady=10)

    # Narx ma'lumotlari
    price_frame = tk.LabelFrame(sell_window, text="Narx ma'lumotlari",
                              bg=colors["bg"], fg=colors["fg"], font=("Arial", 12))
    price_frame.pack(pady=10, padx=20, fill="x")

    # Foyda/zarar ko'rsatkichi
    profit_label = tk.Label(price_frame, text="Foyda/Zarar: $0.00",
                          bg=colors["bg"], fg=colors["fg"], font=("Arial", 12, "bold"))
    profit_label.pack(pady=5)

    # Sotish narxi
    tk.Label(price_frame, text="Sotish narxi ($):", bg=colors["bg"],
            fg=colors["fg"], font=("Arial", 12)).pack(pady=5)
    price_entry = tk.Entry(price_frame, font=("Arial", 12))
    price_entry.insert(0, str(original_price))
    price_entry.pack(pady=5)

    def update_profit(*args):
        try:
            selling_price = float(price_entry.get())
            profit = selling_price - original_price
            color = "#4CAF50" if profit >= 0 else "#FF6B6B"  # Yashil yoki qizil
            profit_label.config(
                text=f"Foyda/Zarar: ${profit:.2f}",
                fg=color
            )
        except ValueError:
            profit_label.config(text="Foyda/Zarar: Noto'g'ri narx", fg="#FF6B6B")

    # Narx o'zgarganda foyda/zaralni yangilash
    price_entry.bind('<KeyRelease>', update_profit)

    # Mijoz ma'lumotlari
    customer_frame = tk.LabelFrame(sell_window, text="Mijoz ma'lumotlari",
                                 bg=colors["bg"], fg=colors["fg"], font=("Arial", 12))
    customer_frame.pack(pady=10, padx=20, fill="x")

    tk.Label(customer_frame, text="Mijoz ismi:", bg=colors["bg"],
            fg=colors["fg"], font=("Arial", 12)).pack(pady=5)
    customer_name = tk.Entry(customer_frame, font=("Arial", 12))
    customer_name.pack(pady=5)

    tk.Label(customer_frame, text="Telefon raqami:", bg=colors["bg"],
            fg=colors["fg"], font=("Arial", 12)).pack(pady=5)
    customer_phone = tk.Entry(customer_frame, font=("Arial", 12))
    customer_phone.pack(pady=5)

    tk.Label(customer_frame, text="Sanani kritng:", bg=colors["bg"],
            fg=colors["fg"], font=("Arial", 12)).pack(pady=5)
    customer_data = tk.Entry(customer_frame, font=("Arial", 12))
    customer_data.pack(pady=5)



    # def confirm_sell():
    #     try:
    #         sell_price = float(price_entry.get())
    #         customer_info = {
    #             "name": customer_name.get().strip(),
    #             "phone": customer_phone.get().strip()
    #         }

    #         today_data = customer_data.get().strip 

    #         if not customer_info["name"] or not customer_info["phone"]:
    #             messagebox.showerror("Xatolik", "Mijoz ma'lumotlarini to'ldiring!")
    #             return

    #         profit = sell_price - original_price
    #         confirm_text = (
    #             # ...existing confirmation text...
    #         )

    #         from datetime import date
    #         sale_record = {
    #             "nomi": customer_info.get('phone'),
    #             "modeli": phone['modeli'],
    #             "today_data": today_data,
    #             "narx": original_price,
    #             "sell_price": sell_price,
    #             "mijoz": customer_info,
    #             "foyda": profit
    #         }

    #         if messagebox.askyesno("Tasdiqlash", confirm_text):
    #             try:
    #                 # Save to sotish_file.json
    #                 sales_data = []
    #                 if os.path.exists("sotish_file.json"):
    #                     with open("sotish_file.json", 'r', encoding='utf-8') as f:
    #                         sales_data = json.load(f)
                    
    #                 sales_data.append(sale_record)
                    
    #                 with open("sotish_file.json", 'w', encoding='utf-8') as f:
    #                     json.dump(sales_data, f, ensure_ascii=False, indent=4)

    #                 # Save to regular sold_phones.json
    #                 phones.pop(index)
    #                 phone.update(sale_record)
    #                 sold_phones.append(phone)
    #                 save_data()
    #                 save_sold_phones()

    #                 messagebox.showinfo("Muvaffaqiyatli", 
    #                     f"{phone['nomi']} muvaffaqiyatli sotildi!")

    #                 sell_window.destroy()

    #             except Exception as e:
    #                 messagebox.showerror("Xatolik", f"Saqlashda xatolik: {str(e)}")

    #     except ValueError:
    #         messagebox.showerror("Xatolik", "Noto'g'ri narx kiritildi!")

        # Tugmalar
        # btn_frame = tk.Frame(sell_window, bg=colors["bg"])
        # btn_frame.pack(pady=15)

        # tk.Button(btn_frame, text="Sotish", command=confirm_sell,
        #         bg=colors["button_bg"], fg=colors["button_fg"],
        #         font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)

        # tk.Button(btn_frame, text="Bekor qilish", command=sell_window.destroy,
        #         bg="#FF6B6B", fg="white", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)

        # # Enter bosilganda sotish
        # sell_window.bind('<Return>', lambda e: confirm_sell())


def confirm_sell():
    try:
        # Narxni float ga o'tkazish va $ belgisini olib tashlash
        sell_price = float(price_entry.get().replace('$', '').strip())
        
        # Mijoz ma'lumotlarini olish
        customer_info = {
            "name": customer_name.get().strip(),
            "phone": customer_phone.get().strip()
        }
        
        if not customer_info["name"] or not customer_info["phone"]:
            messagebox.showerror("Xatolik", "Mijoz ma'lumotlarini to'ldiring!")
            return

        profit = sell_price - original_price
        
        # Sotish ma'lumotlarini yaratish
        sale_record = {
            "nomi": phone["nomi"],
            "modeli": phone["modeli"],
            "asl_narx": f"${original_price:.2f}",
            "sotish_narx": f"${sell_price:.2f}",
            "foyda": f"${profit:.2f}",
            "sotilgan_sana": datetime.now().strftime("%d/%m/%Y"),
            "mijoz_ismi": customer_info["name"],
            "mijoz_telefon": customer_info["phone"]
        }

        confirm_text = (
            f"Sotish ma'lumotlari:\n\n"
            f"Telefon: {phone['nomi']}\n"
            f"IMEI: {phone['modeli']}\n"
            f"Asl narx: ${original_price:.2f}\n"
            f"Sotish narx: ${sell_price:.2f}\n"
            f"Foyda: ${profit:.2f}\n\n"
            f"Mijoz: {customer_info['name']}\n"
            f"Telefon: {customer_info['phone']}\n\n"
            f"Sotishni tasdiqlaysizmi?"
        )

        if messagebox.askyesno("Tasdiqlash", confirm_text):
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

                # Asosiy ma'lumotlarni yangilash
                phones.pop(index)
                sold_phones.append(sale_record)
                save_data()
                save_sold_phones()
                
                messagebox.showinfo("Muvaffaqiyatli", f"{phone['nomi']} muvaffaqiyatli sotildi!")
                sell_window.destroy()

            except Exception as e:
                messagebox.showerror("Xatolik", f"Saqlashda xatolik: {str(e)}")
                print(f"Error details: {e}")  # Console ga xatolik haqida ma'lumot

    except ValueError:
        messagebox.showerror("Xatolik", "Noto'g'ri narx kiritildi!\nFaqat raqamlarni kiriting.")

        # Buttons after confirm_sell is defined
    btn_frame = tk.Frame(sell_window, bg=colors["bg"])
    btn_frame.pack(pady=15)

    tk.Button(btn_frame, text="Sotish", 
              command=confirm_sell,  # Now confirm_sell exists
              bg=colors["button_bg"], 
              fg=colors["button_fg"]).pack(side=tk.LEFT, padx=5)

    








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

# telefonlar tarixi va jami ma’lumotlari
def view_all_history():
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
    
    # qidiruv
    search_frame = tk.Frame(history_window, bg=colors["bg"])
    search_frame.pack(fill="x", padx=20, pady=10)

    tk.Label(search_frame, text=translations[language]["search"],
             bg=colors["bg"], fg=colors["fg"]).pack(side=tk.LEFT, padx=(0, 5))

    search_var = tk.StringVar()
    search_entry = tk.Entry(search_frame, textvariable=search_var,
                            bg=colors["entry_bg"], fg=colors["entry_fg"], width=40)
    search_entry.pack(side=tk.LEFT, padx=5, fill="x", expand=True)

    # Qidiruvni yangilash
    def search_history(event=None):
        search_text = search_var.get().lower()
        tree.delete(*tree.get_children())

        for i, phone in enumerate(all_phones, 1):
            if (search_text in phone["nomi"].lower() or
                search_text in phone["modeli"].lower() or
                search_text in phone["narx"].lower() or
                search_text in phone["holat"].lower() or
                search_text in phone["sana"].lower()):
                tree.insert("", tk.END, values=(
                    i,
                    phone["nomi"],
                    phone["modeli"],
                    phone["narx"],
                    phone["holat"],
                    phone["sana"]
                ), tags=(phone["holat"],))

    search_var.trace("w", lambda name, index, mode: search_history())
    search_entry.bind("<Return>", search_history)

    # Jadval
    table_frame = tk.Frame(history_window, bg=colors["bg"])
    table_frame.pack(pady=10, padx=20, fill="both", expand=True)

    # Jadval ustunlari
    columns = ("id", "phone", "model", "price", "status", "date")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
    
    tree.heading("id", text="ID")
    tree.heading("phone", text="Telefon nomi")
    tree.heading("model", text="IMEI")
    tree.heading("price", text="Narxi")
    tree.heading("status", text="Holati")
    tree.heading("date", text="Sana")

    tree.column("id", anchor="center", width=50)
    tree.column("phone", anchor="center", width=150)
    tree.column("model", anchor="center", width=150)
    tree.column("price", anchor="center", width=100)
    tree.column("status", anchor="center", width=100)
    tree.column("date", anchor="center", width=100)

    # Skroll
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    # Ma'lumotlarni yuklash
    all_phones = []
    
    # Mavjud telefonlar
    for phone in phones:
        phone_data = {
            "nomi": phone["nomi"],
            "modeli": phone["modeli"],
            "narx": phone["narx"],
            "holat": "Mavjud",
            "sana": phone["sana"]
        }
        all_phones.append(phone_data)
    
    # Sotilgan telefonlar
    for phone in sold_phones:
        phone_data = {
            "nomi": phone["nomi"],
            "modeli": phone["modeli"],
            "narx": phone["narx"],
            "holat": "Sotilgan",
            "sana": phone["sana"]
        }
        all_phones.append(phone_data)

    # Jadvalga ma'lumotlarni kiritish
    for i, phone in enumerate(all_phones, 1):
        status_color = "#90EE90" if phone["holat"] == "Mavjud" else "#FFB6C1"  # Yashil yoki qizil
        tree.insert("", tk.END, values=(
            i,
            phone["nomi"],
            phone["modeli"],
            phone["narx"],
            phone["holat"],
            phone["sana"]
        ), tags=(phone["holat"],))

    # Holatga qarab rang berish
    tree.tag_configure("Mavjud", background="#90EE90")  # Yashil
    tree.tag_configure("Sotilgan", background="#FFB6C1")  # Qizil

    # Statistika paneli
    stats_frame = tk.Frame(history_window, bg=colors["bg"])
    stats_frame.pack(pady=10, fill="x", padx=20)

    # Statistika ma'lumotlari
    total_phones = len(phones)
    sold_count = len(sold_phones)
    all_count = total_phones + sold_count

    stats_text = f"Jami telefonlar: {all_count} dona | "
    stats_text += f"Mavjud telefonlar: {total_phones} dona | "
    stats_text += f"Sotilgan telefonlar: {sold_count} dona"

    stats_label = tk.Label(stats_frame, text=stats_text,
                          bg=colors["bg"], fg=colors["fg"],
                          font=("Arial", 12))
    stats_label.pack(pady=5)

    # Yopish tugmasi
    close_btn = tk.Button(history_window, text="Yopish",
                          command=history_window.destroy,
                          bg="#FF6B6B", fg="white",
                          font=("Arial", 10))
    close_btn.pack(pady=15)


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
        font_size = 14  # Increased font size
        title_font = win32ui.CreateFont({
            "name": font_name,
            "height": font_size + 4,  # Larger size for title
            "weight": 700
        })
        font_bold = win32ui.CreateFont({
            "name": font_name,
            "height": font_size,
            "weight": 700
        })
        font_normal = win32ui.CreateFont({
            "name": font_name,
            "height": font_size,
            "weight": 400
        })
        
        # Page settings
        margin_left = 100
        margin_top = 100
        line_height = font_size + 12
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
        copyright_text = "© 2025 Barcha huquqlar himoyalangan"
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
                        sell_btn = tk.Button(info_frame, text="Sotish", command=lambda idx=i: sell_this_phone(idx),
                                          bg="#4CAF50", fg="white", font=("Arial", 10), padx=10)
                        sell_btn.pack(anchor="e", pady=(5, 0))
                        break
    
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
    phone_menu.add_separator()
    phone_menu.add_command(label=translations[language]["export_excel"], command=export_to_excel)

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
    left_button_frame = tk.Frame(main_frame, bg=colors["bg"])
    left_button_frame.pack(side=tk.LEFT, pady=20, padx=50, anchor="nw")

    right_button_frame = tk.Frame(main_frame, bg=colors["bg"])
    right_button_frame.pack(side=tk.RIGHT, pady=20, padx=50, anchor="nw")
    # Tugmalarni yaratish
 
    # left buttons
    left_buttons = [
        (translations[language]["add_phone"], add_phone),
        (translations[language]["delete_phone"], delete_phone),
        (translations[language]["view_phones"], view_phones),
        ("📱 Sotilgan telefonlar", view_sold_phones), 
        # ("🖨️ Chop etish", view_print_screen),  # Add this new button
        ("📊 Telefon tarixi", view_all_history),
        (translations[language]["phone_stats"], show_phone_stats)
    ]
    right_buttons = [
        ("🖨️ Chop etish", view_print_screen),  # Add this new button
        ("🖨️ Printer bulimi", printer_file_ochish),  # Add this new button
        ("Qidiruv", search_phone_by_imei),
        ("Sotish bo'limi", open_sales_file)

    ]

    # create left buttons
    for text, command in left_buttons:
        btn = tk.Button(left_button_frame, text=text, command=command,
                        bg=colors["button_bg"], fg=colors["button_fg"],
                        font=("Arial", 22, "bold"), width=30, height=2)
        btn.pack(pady=20, anchor="w")
    # create right buttons
    for text, command in right_buttons:
        btn = tk.Button(right_button_frame, text=text, command=command,
                        bg=colors["button_bg"], fg=colors["button_fg"],
                        font=("Arial", 22, "bold"), width=30, height=2)
        btn.pack(pady=20, anchor="e")





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



