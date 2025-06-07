import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import json
import os
from datetime import datetime
import sys
import subprocess
from PIL import Image, ImageTk

# Global o'zgaruvchilar
root = None
tree = None
sold_phones = []
language = "uz"

# lug‘at
translations = {
    "uz": {
        "title": "Sotilgan telefonlar tarixi",
        "header": "📱 Sotilgan telefonlar tarixi",
        "phone_name": "Telefon nomi",
        "imei": "IMEI",
        "original_price": "Asl narx",
        "selling_price": "Sotish narx", 
        "profit": "Foyda",
        "date": "Sana",
        "customer": "Mijoz",
        "phone": "Telefon",
        "close": "Yopish",
        "enter_code": "Kodni kiriting:",
        "wrong_code": "Noto'g'ri kod!",
        "error": "Xatolik",
        "confirm": "Tasdiqlash",
        "enter": "Enter tugmasi bosib naxrni ko'ing:",
        "search": "Qidirsh"
    },
    "ru": {
        "title": "История продаж телефонов",
        "header": "📱 История продаж телефонов",
        "phone_name": "Название телефона",
        "imei": "IMEI",
        "original_price": "Исходная цена",
        "selling_price": "Цена продажи",
        "profit": "Прибыль",
        "date": "Дата",
        "customer": "Клиент",
        "phone": "Телефон",
        "close": "Закрыть",
        "enter_code": "Введите код:",
        "wrong_code": "Неверный код!",
        "error": "Ошибка",
        "confirm": "Подтверждение",
        "enter": "Нажмите Enter, чтобы увидеть цену:",
        "search": "Поиск"
    }
}

# Ranglar
colors = {
    "bg": "#ffffff",
    "fg": "#333333",
    "button_bg": "#4CAF50",
    "button_fg": "white",
    "entry_bg": "#f0f0f0",
    "entry_fg": "#333333"
}

def main():
    global root, tree
    
    root = tk.Tk()
    root.title("Sotilgan telefonlar tarixi")
    root.state('zoomed')
    root.configure(bg=colors["bg"])






        # Til tanlash tugmalari
    def change_language(lang):
        global language
        language = lang
        root.title(translations[language]["title"])
        header.config(text=translations[language]["header"])
        # Ustun sarlavhalarini yangilash
        tree.heading("nomi", text=translations[language]["phone_name"])
        tree.heading("modeli", text=translations[language]["imei"])
        tree.heading("asl_narx", text=translations[language]["original_price"])
        tree.heading("sotish_narx", text=translations[language]["selling_price"])
        tree.heading("foyda", text=translations[language]["profit"])
        tree.heading("sana", text=translations[language]["date"])
        tree.heading("mijoz", text=translations[language]["customer"])
        tree.heading("telefon", text=translations[language]["phone"])
        close_btn.configure(text=translations[language]["close"])

    
    lang_frame = tk.Frame(root, bg=colors["bg"])
    lang_frame.pack(anchor="ne", padx=20, pady=10)
    
    uz_btn = ctk.CTkButton(lang_frame, 
                          text="UZ",
                          command=lambda: change_language("uz"),
                          fg_color="#3486eb",
                          text_color="white",
                          width=80,
                          height=25,
                          corner_radius=10)  # Burchaklar radiusi
    uz_btn.pack(side=tk.LEFT, padx=5)
    
    ru_btn = ctk.CTkButton(lang_frame,
                          text="RU",
                          command=lambda: change_language("ru"),
                          fg_color="#34eb40",
                          text_color="white", 
                          width=80,
                          height=25,)
    ru_btn.pack(side=tk.LEFT, padx=5)

    
    
    # Sarlavha
    header = tk.Label(root, 
                     text="📱 Sotilgan telefonlar tarixi",
                     font=("Arial", 20, "bold"),
                     bg=colors["bg"],
                     fg=colors["fg"])
    header.pack(pady=20)
    
    # Jadval
    table_frame = tk.Frame(root, bg=colors["bg"])
    table_frame.pack(pady=10, padx=20, fill="both", expand=True)
    
    columns = ("id", "nomi", "modeli", "asl_narx", "sotish_narx", "foyda", "sana", "mijoz", "telefon")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")
    
    # Ustun sarlavhalari
    tree.heading("id", text="ID")
    tree.heading("nomi", text="Telefon nomi")
    tree.heading("modeli", text="IMEI")
    tree.heading("asl_narx", text="Asl narx")
    tree.heading("sotish_narx", text="Sotish narx")
    tree.heading("foyda", text="Foyda")
    tree.heading("sana", text="Sana")
    tree.heading("mijoz", text="Mijoz")
    tree.heading("telefon", text="Telefon")
    
    # Ustun kengliklari
    tree.column("id", width=50, anchor="center")
    tree.column("nomi", width=150, anchor="center")
    tree.column("modeli", width=150, anchor="center")
    tree.column("asl_narx", width=100, anchor="center")
    tree.column("sotish_narx", width=100, anchor="center")
    tree.column("foyda", width=100, anchor="center")
    tree.column("sana", width=100, anchor="center")
    tree.column("mijoz", width=150, anchor="center")
    tree.column("telefon", width=150, anchor="center")
    tree.bind('<ButtonRelease-1>', verify_price)
    
    # Skroll
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)
    
    # Ustunlar tagidan chiziq
    separator = ttk.Separator(root, orient='horizontal')
    separator.pack(fill='x', pady=10)
    # Ma'lumotlarni yuklash
    load_sales_data()
    
    # Statistika frame dan oldin qo'shish kerak:

    # Qidiruv frame
    search_frame = tk.Frame(root, bg=colors["bg"])
    search_frame.pack(fill="x", padx=20, pady=10)
    
    # IMEI qidiruv
    tk.Label(search_frame, 
             text="IMEI orqali qidirish:",
             font=("Arial", 12),
             bg=colors["bg"],
             fg=colors["fg"]).pack(side=tk.LEFT, padx=5)
    
    
    def search_by_imei():
        search_text = search_entry.get().strip().lower()
        if not search_text:
            for item in tree.get_children():
                tree.delete(item)

            load_sales_data()  # Agar bo'sh bo'lsa, barcha ma'lumotlarni ko'rsatish
            return
            
        try:
            with open("sotish_file.json", 'r', encoding='utf-8') as f:
                sales_data = json.load(f)
            
            # Avval jadvaldan barcha elementlarni o'chirish
            for item in tree.get_children():
                tree.delete(item)
            
            # Qidiruv natijalarini ko'rsatish
            found = False
            for i, sale in enumerate(sales_data, 1):
                if search_text in sale["modeli"].lower():
                    found = True
                    tree.insert("", "end", values=(
                        i,
                        sale["nomi"],
                        sale["modeli"],
                        "****",
                        "****",
                        "****",
                        sale["sotilgan_sana"],
                        sale["mijoz_ismi"],
                        sale["mijoz_telefon"]
                    ))
            
            if not found:
                messagebox.showinfo("Natija", "Bunday IMEI raqamli telefon topilmadi!")
                for item in tree.get_children():  # Avval tozalash
                    tree.delete(item)
                load_sales_data()  # Barcha ma'lumotlarni qayta yuklash
                
        except Exception as e:
            messagebox.showerror("Xatolik", f"Qidirishda xatolik: {str(e)}")
        # qidiruv
    search_entry = tk.Entry(search_frame, 
                        font=("Arial", 12),
                        bg=colors["entry_bg"],
                        fg=colors["entry_fg"],
                        width=30)  # Kenglikni oshirdik
    search_entry.pack(side=tk.LEFT, padx=5)
    
    # Enter bosilganda qidirish
    search_entry.bind('<Return>', lambda e: search_by_imei())






    # Statistika
    stats_frame = tk.Frame(root, bg=colors["bg"])
    stats_frame.pack(fill="x", padx=20, pady=10)
    
    # Yopish tugmasi
    close_btn = ctk.CTkButton(root,
                         text=translations[language]["close"],
                         command=root.destroy,
                         fg_color="#FF6B6B",  # Qizil rang
                         hover_color="#FF4B4B",  # Hover ranggi
                         text_color="white", 
                         width=120,  # Kattaroq tugma
                         height=40,
                         corner_radius=10,
                         font=("Arial", 14, "bold")
                        )
    close_btn.pack(pady=15, padx=25)


    
    root.mainloop()




def verify_price(event):
    """Narxni ko'rish uchun kodni tekshirish"""
    item = tree.identify_row(event.y)
    column = tree.identify_column(event.x)
    
    # Check if clicked on price columns
    if column in ('#4', '#5', '#6'):  # asl_narx, sotish_narx, foyda ustunlari
        dialog = tk.Toplevel(root)
        dialog.title("Tasdiqlash")
        dialog.geometry("300x150")
        dialog.configure(bg=colors["bg"])
        # Dialog oynasini markazlashtirish
        dialog.transient(root)   # Asosiy oynaga bog'lash
        dialog.grab_set()        # Modallik
        
        # Oynani markazga joylash
        x = root.winfo_x() + (root.winfo_width() - 300) // 2
        y = root.winfo_y() + (root.winfo_height() - 150) // 2
        dialog.geometry(f"300x150+{x}+{y}")

        
        tk.Label(dialog, 
                text=translations[language]["enter"],
                font=("Arial", 12),
                bg=colors["bg"]).pack(pady=10)
        
        code_entry = tk.Entry(dialog, show="*", font=("Arial", 12))
        code_entry.pack(pady=5)
        code_entry.focus()
        
        def check_code():
            if code_entry.get() == "0630":  # O'zingizning kodingizni qo'ying
                item_id = int(tree.item(item)["values"][0]) - 1
                with open("sotish_file.json", 'r', encoding='utf-8') as f:
                    sales_data = json.load(f)
                
                sale = sales_data[item_id]
                values = list(tree.item(item)["values"])
                
                # Show actual price based on column
                if column == '#4':
                    values[3] = sale["asl_narx"]
                elif column == '#5':
                    values[4] = sale["sotish_narx"]
                elif column == '#6':
                    values[5] = sale["foyda"]
                
                tree.item(item, values=values)
                dialog.destroy()
            else:
                messagebox.showerror("Xato", "Noto'g'ri kod!", parent=dialog)
                code_entry.delete(0, tk.END)
        
        code_entry.bind('<Return>', lambda e: check_code())
        tk.Button(dialog, 
                 command=check_code,
                 bg=colors[""],
                 fg="white").pack(pady=10)




def load_sales_data():

    """Sotilgan telefonlar ma'lumotlarini yuklash"""
    try:
        if os.path.exists("sotish_file.json"):
            with open("sotish_file.json", 'r', encoding='utf-8') as f:
                sales_data = json.load(f)
                
            for i, sale in enumerate(sales_data, 1):


                tree.insert("", "end", values=(
                    i,
                    sale["nomi"],
                    sale["modeli"],
                    "****",
                    "****",
                    "****",
                    sale["sotilgan_sana"],
                    sale["mijoz_ismi"],
                    sale["mijoz_telefon"]
                ))
    except Exception as e:
        messagebox.showerror("Xatolik", f"Ma'lumotlarni yuklashda xatolik: {str(e)}")



if __name__ == "__main__":
    main()