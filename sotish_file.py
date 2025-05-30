import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import sys
import subprocess

# Global o'zgaruvchilar
root = None
tree = None
sold_phones = []

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
    
    # Statistika
    stats_frame = tk.Frame(root, bg=colors["bg"])
    stats_frame.pack(fill="x", padx=20, pady=10)
    
    # Yopish tugmasi
    close_btn = tk.Button(root,
                         text="Yopish",
                         command=root.destroy,
                         bg="#eb346b",
                         fg="white",
                         font=("Arial", 15),
                         activebackground='#eb346b',
                         activeforeground="white",
                         padx=25)
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
        
        tk.Label(dialog, 
                text="Kodni kiriting:",
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
                    values[3] = sale["narx"]
                elif column == '#5':
                    values[4] = sale["sell_price"]
                elif column == '#6':
                    values[5] = sale["foyda"]
                
                tree.item(item, values=values)
                dialog.destroy()
            else:
                messagebox.showerror("Xato", "Noto'g'ri kod!", parent=dialog)
                code_entry.delete(0, tk.END)
        
        code_entry.bind('<Return>', lambda e: check_code())
        tk.Button(dialog, 
                 text="Tasdiqlash",
                 command=check_code,
                 bg=colors["button_bg"],
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
                    sale["asl_narx"],
                    sale["sotish_narx"],
                    sale["foyda"],
                    sale["sotilgan_sana"],
                    sale["mijoz_ismi"],
                    sale["mijoz_telefon"]
                ))
    except Exception as e:
        messagebox.showerror("Xatolik", f"Ma'lumotlarni yuklashda xatolik: {str(e)}")



if __name__ == "__main__":
    main()