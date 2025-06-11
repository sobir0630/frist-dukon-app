# import tkinter as tk
# import tkinter.ttk as ttk
# from tkinter import ttk, scrolledtext, messagebox, filedialog
# from tkinter.font import Font
# import os
# import sys
# import tempfile
# import threading
# import time
# import subprocess
# import platform
# import queue
# import json
# from datetime import datetime

# class PrinterApp:
#     def __init__(self, root):
#         self.progress_queue = queue.Queue()
#         self.root = root
#         self.root.title("Printer Dasturi - Telefon Chop Etish")
#         self.root.state('zoomed')
#         self.root.configure(bg="#f5f5f5")
#         self.root.minsize(900, 700)
        
#         # Telefonlar ma'lumotlari
#         self.phones_data = []
#         self.selected_phone = None
#         self.json_file_path = "telefon_data.json"
        
#         # Asosiy stillar
#         self.setup_styles()
        
#         # Interfeys yaratish
#         self.create_interface()
        
#         # Printerlarni izlash
#         self.find_printers()
        
#         # Progress monitor
#         self.start_progress_monitor()
    
#     def setup_styles(self):
#         """Dizayn stillarini sozlash"""
#         self.style = ttk.Style()
#         self.style.theme_use('clam')
        
#         # Ranglar
#         self.colors = {
#             'primary': '#2196F3',
#             'secondary': '#4CAF50', 
#             'danger': '#f44336',
#             'warning': '#FF9800',
#             'bg': '#f5f5f5',
#             'white': '#ffffff',
#             'text': '#333333'
#         }
        
#         # Stillar
#         self.style.configure('TButton', 
#                            font=('Segoe UI', 10), 
#                            background=self.colors['primary'], 
#                            foreground='white',
#                            padding=8)
        
#         self.style.configure('Success.TButton',
#                            background=self.colors['secondary'])
        
#         self.style.configure('Danger.TButton',
#                            background=self.colors['danger'])
        
#         self.style.configure('TLabel', 
#                            font=('Segoe UI', 10), 
#                            background=self.colors['bg'])
        
#         self.style.configure('Header.TLabel', 
#                            font=('Segoe UI', 16, 'bold'), 
#                            background=self.colors['primary'], 
#                            foreground='white')
        
#         self.style.configure('TFrame', background=self.colors['bg'])
        
#         self.style.configure('Card.TFrame', 
#                            background=self.colors['white'],
#                            relief='solid',
#                            borderwidth=1)
    
#     def create_interface(self):
#         """Asosiy interfeys yaratish"""
#         # Asosiy container
#         self.main_frame = ttk.Frame(self.root, padding=(5, 2.5))
#         self.main_frame.pack(fill=tk.BOTH, expand=True)
        
#         # Sarlavha
#         self.create_header()
        
#         # Asosiy content
#         self.content_frame = ttk.Frame(self.main_frame)
#         self.content_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
#         # Chap tomon - Telefonlar ro'yxati
#         self.create_phone_list()
        
#         # O'ng tomon - Preview va sozlamalar
#         self.create_preview_panel()
        
#         # Pastki panel - Tugmalar va status
#         self.create_bottom_panel()
    
#     def create_header(self):
#         """Sarlavha yaratish"""
#         header_frame = ttk.Frame(self.main_frame, style='Card.TFrame')
#         header_frame.pack(fill=tk.X, pady=(0, 5))
        
#         header_label = ttk.Label(header_frame, 
#                                text="📱 Telefon Printer Dasturi", 
#                                style='Header.TLabel')
#         header_label.pack(fill=tk.X, ipady=5)
    
#     def create_phone_list(self):
#         """Telefonlar ro'yxati paneli"""
#         # Chap panel
#         left_frame = ttk.Frame(self.content_frame, style='Card.TFrame')
#         left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
#         # Sarlavha va tugmalar
#         list_header_frame = ttk.Frame(left_frame)
#         list_header_frame.pack(fill=tk.X, padx=15)
        
#         ttk.Label(list_header_frame, 
#                  text="📋 Telefonlar Ro'yxati", 
#                  font=('Segoe UI', 12, 'bold')).pack(side=tk.LEFT)
        
#         load_btn = ttk.Button(list_header_frame, 
#                             text="📁 JSON Yuklash", 
#                             command=self.load_json_file,
#                             width=15)
#         load_btn.pack(side=tk.RIGHT, padx=5)
        
#         # Qidiruv
#         search_frame = ttk.Frame(left_frame)
#         search_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        
#         ttk.Label(search_frame, text="🔍 Qidiruv:").pack(side=tk.LEFT)
#         self.search_var = tk.StringVar()
#         self.search_var.trace('w', self.filter_phones)
#         search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
#         search_entry.pack(side=tk.LEFT, padx=(5, 0), fill=tk.X, expand=True)
        
#         # Jadval
#         table_frame = ttk.Frame(left_frame)
#         table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
#         # Treeview
#         columns = ("id", "nomi")
#         self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        
#         # Sarlavhalar
#         self.tree.heading("id", text="ID")
#         self.tree.heading("nomi", text="Telefon Nomi")

        
#         # Ustunlar kengligi
#         self.tree.column("id", width=10, anchor="center")
#         self.tree.column("nomi", width=30, anchor="center")

        
#         # Scrollbar
#         tree_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
#         self.tree.configure(yscrollcommand=tree_scrollbar.set)
        
#         # Pack
#         tree_scrollbar.pack(side="right", fill="y")
#         self.tree.pack(side="left", fill="both", expand=True)
        
#         # Event binding
#         self.tree.bind("<<TreeviewSelect>>", self.on_phone_select)
#         self.tree.bind("<Double-1>", self.on_phone_double_click)
    
#     def create_preview_panel(self):
#         """Preview va sozlamalar paneli"""
#         # O'ng panel
#         right_frame = ttk.Frame(self.content_frame, style='Card.TFrame')
#         right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
#         # Preview sarlavha
#         preview_header = ttk.Frame(right_frame)
#         preview_header.pack(fill=tk.X, padx=15, pady=(15, 10))
        
#         ttk.Label(preview_header, 
#                  text="👁️ Chop Etish Ko'rinishi", 
#                  font=('Segoe UI', 12, 'bold')).pack(side=tk.LEFT)
        
#         # Hajm sozlash
#         size_frame = ttk.Frame(preview_header)
#         size_frame.pack(side=tk.RIGHT)
        

#         # Preview matn maydoni
#         self.preview_frame = ttk.Frame(right_frame)
#         self.preview_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 10))
        
#         self.preview_text = scrolledtext.ScrolledText(
#             self.preview_frame, 
#             wrap=tk.WORD, 
#             font=('Segoe UI', 11),
#             state='disabled',
#             bg='white',
#             relief='solid',
#             borderwidth=1
#         )
#         self.preview_text.pack(fill=tk.BOTH, expand=True)
        
#         # Formatlash sozlamalari
#         self.create_format_settings(right_frame)
    
#     def create_format_settings(self, parent):
#         """Formatlash sozlamalarini yaratish"""
#         format_frame = ttk.LabelFrame(parent, text="🎨 Formatlash Sozlamalari")
#         format_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
#         # Font sozlamalari
#         font_frame = ttk.Frame(format_frame)
#         font_frame.pack(fill=tk.X, padx=10, pady=10)
        
#         # Shrift
#         ttk.Label(font_frame, text="Shrift:").grid(row=0, column=0, padx=5, sticky=tk.W)
#         self.font_var = tk.StringVar(value="Segoe UI")
#         font_combo = ttk.Combobox(font_frame, textvariable=self.font_var, state="readonly", width=12)
#         font_combo['values'] = ("Segoe UI", "Arial", "Times New Roman", "Courier New", "Verdana")
#         font_combo.grid(row=0, column=1, padx=5)
#         font_combo.bind("<<ComboboxSelected>>", self.update_preview)
        
#         # Hajm
#         ttk.Label(font_frame, text="Hajm:").grid(row=0, column=2, padx=5, sticky=tk.W)
#         self.size_var = tk.StringVar(value="11")
#         size_combo = ttk.Combobox(font_frame, textvariable=self.size_var, state="readonly", width=5)
#         size_combo['values'] = ("8", "9", "10", "11", "12", "14", "16", "18", "20", "24")
#         size_combo.grid(row=0, column=3, padx=5)
#         size_combo.bind("<<ComboboxSelected>>", self.update_preview)
        
#         # Stil sozlamalari
#         style_frame = ttk.Frame(format_frame)
#         style_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
#         self.bold_var = tk.BooleanVar()
#         bold_check = ttk.Checkbutton(style_frame, text="Qalin", variable=self.bold_var, command=self.update_preview)
#         bold_check.pack(side=tk.LEFT, padx=10)
        
#         self.italic_var = tk.BooleanVar()
#         italic_check = ttk.Checkbutton(style_frame, text="Kursiv", variable=self.italic_var, command=self.update_preview)
#         italic_check.pack(side=tk.LEFT, padx=10)
        
#         self.underline_var = tk.BooleanVar()
#         underline_check = ttk.Checkbutton(style_frame, text="Chiziq", variable=self.underline_var, command=self.update_preview)
#         underline_check.pack(side=tk.LEFT, padx=10)
    
#     def create_bottom_panel(self):
#         """Pastki panel - printer sozlamalari va tugmalar"""
#         bottom_frame = ttk.Frame(self.main_frame, style='Card.TFrame')
#         bottom_frame.pack(fill=tk.X, pady=(0, 10))
        
#         # Printer sozlamalari
#         printer_frame = ttk.LabelFrame(bottom_frame, text="🖨️ Printer Sozlamalari")
#         printer_frame.pack(fill=tk.X, padx=15, pady=15)
        
#         settings_frame = ttk.Frame(printer_frame)
#         settings_frame.pack(fill=tk.X, padx=10, pady=10)
        
#         # Printer tanlash
#         ttk.Label(settings_frame, text="Printer:").grid(row=0, column=0, padx=5, sticky=tk.W)
#         self.printer_var = tk.StringVar()
#         self.printer_combo = ttk.Combobox(settings_frame, textvariable=self.printer_var, state="readonly", width=30)
#         self.printer_combo.grid(row=0, column=1, padx=5)
        
#         refresh_btn = ttk.Button(settings_frame, text="🔄", command=self.find_printers, width=5)
#         refresh_btn.grid(row=0, column=2, padx=5)
        
#         # Nusxalar soni
#         ttk.Label(settings_frame, text="Nusxalar:").grid(row=0, column=3, padx=(20, 5), sticky=tk.W)
#         self.copies_var = tk.StringVar(value="1")
#         copies_spin = ttk.Spinbox(settings_frame, from_=1, to=99, width=5, textvariable=self.copies_var)
#         copies_spin.grid(row=0, column=4, padx=5)
        
#         # Boshqa sozlamalar
#         options_frame = ttk.Frame(settings_frame)
#         options_frame.grid(row=1, column=0, columnspan=5, pady=(10, 0), sticky=tk.W)
        
#         self.color_var = tk.BooleanVar(value=True)
#         color_check = ttk.Checkbutton(options_frame, text="Rangli", variable=self.color_var)
#         color_check.pack(side=tk.LEFT, padx=10)
        
#         self.duplex_var = tk.BooleanVar()
#         duplex_check = ttk.Checkbutton(options_frame, text="Ikki tomonlama", variable=self.duplex_var)
#         duplex_check.pack(side=tk.LEFT, padx=10)
        
#         # Tugmalar
#         buttons_frame = ttk.Frame(bottom_frame)
#         buttons_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
#         # Chap tomon tugmalar
#         left_buttons = ttk.Frame(buttons_frame)
#         left_buttons.pack(side=tk.LEFT)
        
#         edit_btn = ttk.Button(left_buttons, text="✏️ Tahrirlash", command=self.edit_selected_phone, width=15)
#         edit_btn.pack(side=tk.LEFT, padx=5)
        
#         # O'ng tomon tugmalar
#         right_buttons = ttk.Frame(buttons_frame)
#         right_buttons.pack(side=tk.RIGHT)
        
#         self.print_btn = ttk.Button(right_buttons, text="🖨️ Chop Etish", command=self.print_selected, 
#                                   style='Success.TButton', width=15)
#         self.print_btn.pack(side=tk.RIGHT, padx=5)
#         self.print_btn.configure(state='disabled')
        
#         # Status
#         self.status_frame = ttk.Frame(bottom_frame)
#         self.status_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
#         self.status_var = tk.StringVar(value="JSON fayl yuklab telefon tanlang")
#         self.status_label = ttk.Label(self.status_frame, textvariable=self.status_var, foreground=self.colors['primary'])
#         self.status_label.pack(side=tk.LEFT)
    
#     def load_default_json(self):
#         """Dastur ishga tushganda avtomatik JSON yuklash"""
#         if os.path.exists(self.json_file_path):
#             try:
#                 with open(self.json_file_path, 'r', encoding='utf-8') as file:
#                     data = json.load(file)
                
#                 if isinstance(data, list):
#                     self.phones_data = data
#                 elif isinstance(data, dict) and 'phones' in data:
#                     self.phones_data = data['phones']
#                 else:
#                     raise ValueError("JSON fayl noto'g'ri formatda")
                
#                 self.populate_phone_list()
#                 self.show_status(f"{len(self.phones_data)} ta telefon yuklandi")
                
#             except Exception as e:
#                 messagebox.showerror("Xato", f"JSON faylni yuklashda xato:\n{str(e)}")
#                 self.show_status("JSON fayl yuklanmadi", "error")
#         else:
#             self.show_status(f"{self.json_file_path} fayli topilmadi", "warning")

#     def load_json_file(self):
#         """JSON fayl yuklash (qo'lda)"""
#         file_path = filedialog.askopenfilename(
#             title="Telefonlar JSON faylini tanlang",
#             filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
#             initialfile=self.json_file_path  # Oldingi fayl nomini ko'rsatish
#         )
        
#         if not file_path:
#             return
        
#         try:
#             with open(file_path, 'r', encoding='utf-8') as file:
#                 data = json.load(file)
            
#             if isinstance(data, list):
#                 self.phones_data = data
#             elif isinstance(data, dict) and 'phones' in data:
#                 self.phones_data = data['phones']
#             else:
#                 raise ValueError("JSON fayl noto'g'ri formatda")
            
#             # Yangi fayl nomini saqlash
#             self.json_file_path = file_path
#             self.populate_phone_list()
#             self.show_status(f"{len(self.phones_data)} ta telefon yuklandi")
            
#         except Exception as e:
#             messagebox.showerror("Xato", f"JSON faylni yuklashda xato:\n{str(e)}")
#             self.show_status("JSON fayl yuklanmadi", "error")
            
               
#     def populate_phone_list(self):
#         """Telefonlar ro'yxatini to'ldirish"""
#         # Oldingi ma'lumotlarni tozalash
#         for item in self.tree.get_children():
#             self.tree.delete(item)
        
#         # Yangi ma'lumotlarni qo'shish
#         for i, phone in enumerate(self.phones_data, 1):
#             try:
#                 self.tree.insert("", tk.END, values=(
#                     i,
#                     phone.get('nomi', 'N/A'),

#                 ))
#             except Exception as e:
#                 print(f"Ma'lumot qo'shishda xato: {e}")
    
#     def filter_phones(self, *args):
#         """Telefonlarni qidirish bo'yicha filtrlash"""
#         if not self.phones_data:
#             return
        
#         search_term = self.search_var.get().lower()
        
#         # Oldingi ma'lumotlarni tozalash
#         for item in self.tree.get_children():
#             self.tree.delete(item)
        
#         # Filtrlangan ma'lumotlarni qo'shish
#         filtered_count = 0
#         for i, phone in enumerate(self.phones_data, 1):
#             if (search_term in phone.get('nomi', '').lower()):
                
#                 self.tree.insert("", tk.END, values=(
#                     i,
#                     phone.get('nomi', 'N/A'),
#                 ))
#                 filtered_count += 1
        
#         if search_term:
#             self.show_status(f"{filtered_count} ta telefon topildi")
    
#     def on_phone_select(self, event):
#         """Telefon tanlanganida"""
#         selection = self.tree.selection()
#         if not selection:
#             return
        
#         item = self.tree.item(selection[0])
#         phone_id = item['values'][0] - 1  # Index 0 dan boshlanadi
        
#         if 0 <= phone_id < len(self.phones_data):
#             self.selected_phone = self.phones_data[phone_id]
#             self.update_preview()
#             self.print_btn.configure(state='normal')
#             self.show_status(f"Telefon tanlandi: {self.selected_phone.get('nomi', 'N/A')}")
    
#     def on_phone_double_click(self, event):
#         """Telefonga ikki marta bosganda tahrirlash"""
#         self.edit_selected_phone()
    
#     def update_preview(self, *args):
#         """Preview matnini yangilash"""
#         if not self.selected_phone:
#             self.preview_text.configure(state='normal')
#             self.preview_text.delete('1.0', tk.END)
#             self.preview_text.insert(tk.END, "Telefon tanlanmagan...")
#             self.preview_text.configure(state='disabled')
#             return
        
#         # Matn yaratish
#         text_content = self.format_phone_info(self.selected_phone)
        
#         # Font sozlash
#         font_family = self.font_var.get()
#         font_size = int(self.size_var.get())
#         font_weight = "bold" if self.bold_var.get() else "normal"
#         font_slant = "italic" if self.italic_var.get() else "roman"
        
#         preview_font = Font(
#             family=font_family,
#             size=font_size,
#             weight=font_weight,
#             slant=font_slant,
#             underline=self.underline_var.get()
#         )
        
#         # Preview yangilash
#         self.preview_text.configure(state='normal', font=preview_font)
#         self.preview_text.delete('1.0', tk.END)
#         self.preview_text.insert(tk.END, text_content)
#         self.preview_text.configure(state='disabled')
    
#     def update_preview_size(self, value):
#         """Preview hajmini yangilash"""
#         zoom_percent = int(float(value) * 100)
#         self.zoom_label.configure(text=f"{zoom_percent}%")
        
#         if hasattr(self, 'preview_text'):
#             current_font = self.preview_text.cget('font')
#             if current_font:
#                 # Font hajmini kattalashtirish
#                 base_size = int(self.size_var.get())
#                 new_size = int(base_size * float(value))
                
#                 font_family = self.font_var.get()
#                 font_weight = "bold" if self.bold_var.get() else "normal"
#                 font_slant = "italic" if self.italic_var.get() else "roman"
                
#                 scaled_font = Font(
#                     family=font_family,
#                     size=new_size,
#                     weight=font_weight,
#                     slant=font_slant,
#                     underline=self.underline_var.get()
#                 )
                
#                 self.preview_text.configure(font=scaled_font)
    
      


#     def format_phone_info(self, phone):
#         """Telefon ma'lumotlarini formatlash"""
#         current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
#         text = f"""
#             ╔══════════════════════════════════════════════════════════════╗
#             ║                    TELEFON MA'LUMOTLARI                      ║
#             ╠══════════════════════════════════════════════════════════════╣
#             ║                                                              ║
#             ║  📱 Telefon Nomi:  {phone.get('nomi', 'N/A'):<40} ║
#             ║                                                              ║
#             ║  🔢 IMEI Raqam:    {phone.get('imei', 'N/A'):<40} ║
#             ║                                                              ║
#             ║  💰 Narx:          {phone.get('narx', 'N/A'):<40} ║
#             ║                                                              ║
#             ║  📅 Sana:          {phone.get('sana', 'N/A'):<40} ║
#             ║                                                              ║
#             ║  📝 Izoh:          {phone.get('izoh', 'Izoh yoq'):<40} ║
#             ║                                                              ║
#             ║  🏪 Magazin:       {phone.get('magazin', 'N/A'):<40} ║
#             ║                                                              ║
#             ║  👤 Sotuvchi:      {phone.get('sotuvchi', 'N/A'):<40} ║
#             ║                                                              ║
#             ╠══════════════════════════════════════════════════════════════╣
#             ║  Chop etilgan:     {current_time:<40} ║
#             ╚══════════════════════════════════════════════════════════════╝

#             Diqqat: Bu hujjat rasmiy hisobot hisoblanadi.
#             Barcha ma'lumotlar to'g'riligini tekshiring.

#             --------------------------------
#             Imzo: _______________  Sana: _______________

#         """
#         return text.strip()
    
#     def edit_selected_phone(self):
#         """Tanlangan telefonni tahrirlash"""
#         if not self.selected_phone:
#             messagebox.showwarning("Ogohlantirish", "Avval telefon tanlang!")
#             return
        
#         # Tahrirlash oynasi
#         edit_window = tk.Toplevel(self.root)
#         edit_window.title("Telefon Ma'lumotlarini Tahrirlash")
#         edit_window.geometry("500x600")
#         edit_window.configure(bg=self.colors['bg'])
#         edit_window.transient(self.root)
#         edit_window.grab_set()
        
#         # Sarlavha
#         header = ttk.Label(edit_window, text="✏️ Telefon Ma'lumotlarini Tahrirlash", 
#                           font=('Segoe UI', 14, 'bold'))
#         header.pack(pady=20)
        
#         # Ma'lumotlar kiritish
#         main_frame = ttk.Frame(edit_window, padding=20)
#         main_frame.pack(fill=tk.BOTH, expand=True)
        
#         # O'zgaruvchilar
#         vars_dict = {}
#         fields = [
#             ('nomi', 'Telefon Nomi:', 'text'),
#             ('imei', 'IMEI Raqam:', 'text'),
#             ('narx', 'Narx:', 'text'),
#             ('sana', 'Sana:', 'text'),
#             ('izoh', 'Izoh:', 'text'),
#             ('magazin', 'Magazin:', 'text'),
#             ('sotuvchi', 'Sotuvchi:', 'text')
#         ]
        
#         for i, (key, label, field_type) in enumerate(fields):
#             ttk.Label(main_frame, text=label, font=('Segoe UI', 10, 'bold')).grid(
#                 row=i, column=0, sticky=tk.W, pady=5, padx=(0, 10))
            
#             vars_dict[key] = tk.StringVar(value=self.selected_phone.get(key, ''))
            
#             if key == 'izoh':
#                 # Izoh uchun Text widget
#                 text_widget = tk.Text(main_frame, height=4, width=40, font=('Segoe UI', 10))
#                 text_widget.grid(row=i, column=1, sticky=tk.W+tk.E, pady=5)
#                 text_widget.insert('1.0', self.selected_phone.get(key, ''))
#                 vars_dict[key] = text_widget
#             else:
#                 entry = ttk.Entry(main_frame, textvariable=vars_dict[key], width=40, font=('Segoe UI', 10))
#                 entry.grid(row=i, column=1, sticky=tk.W+tk.E, pady=5)
        
#         # Tugmalar
#         buttons_frame = ttk.Frame(edit_window)
#         buttons_frame.pack(fill=tk.X, pady=20)
        
#         def save_changes():
#             try:
#                 # Ma'lumotlarni yangilash
#                 phone_index = self.phones_data.index(self.selected_phone)
#                 for key, var in vars_dict.items():
#                     if key == 'izoh':
#                         self.phones_data[phone_index][key] = var.get('1.0', tk.END).strip()
#                     else:
#                         self.phones_data[phone_index][key] = var.get()
                
#                 # Jadval va preview yangilash
#                 self.populate_phone_list()
#                 self.selected_phone = self.phones_data[phone_index]
#                 self.update_preview()
                
#                 edit_window.destroy()
#                 self.show_status("Ma'lumotlar yangilandi")
                
#             except Exception as e:
#                 messagebox.showerror("Xato", f"Ma'lumotlarni saqlashda xato:\n{str(e)}")
        
#         save_btn = ttk.Button(buttons_frame, text="💾 Saqlash", command=save_changes, 
#                             style='Success.TButton')
#         save_btn.pack(side=tk.RIGHT, padx=5)
        
#         cancel_btn = ttk.Button(buttons_frame, text="❌ Bekor qilish", command=edit_window.destroy)
#         cancel_btn.pack(side=tk.RIGHT, padx=5)
    
#     def find_printers(self):
#         """Mavjud printerlarni topish"""
#         try:
#             if platform.system() == "Windows":
#                 import win32print
#                 printers = [printer[2] for printer in win32print.EnumPrinters(2)]
#             else:
#                 # Linux/Mac uchun
#                 printers = [line.split()[0] for line in subprocess.check_output(["lpstat", "-a"]).decode().splitlines()]
            
#             self.printer_combo['values'] = printers
#             if printers:
#                 self.printer_var.set(printers[0])
#                 self.show_status(f"{len(printers)} ta printer topildi")
#             else:
#                 self.show_status("Printer topilmadi", "error")
        
#         except Exception as e:
#             self.show_status(f"Printerlarni topishda xato: {str(e)}", "error")
#             self.printer_combo['values'] = []
    
#     def print_selected(self):
#         """Tanlangan telefonni chop etish"""
#         if not self.selected_phone:
#             messagebox.showwarning("Ogohlantirish", "Avval telefon tanlang!")
#             return
        
#         if not self.printer_var.get():
#             messagebox.showwarning("Ogohlantirish", "Printer tanlanmagan!")
#             return
        
#         try:
#             # Vaqtinchalik fayl yaratish
#             temp_file = tempfile.NamedTemporaryFile(mode='w+', suffix='.txt', delete=False, encoding='utf-8')
#             temp_file.write(self.format_phone_info(self.selected_phone))
#             temp_file.close()
            
#             # Printer buyrug'i
#             printer_name = self.printer_var.get()
#             copies = self.copies_var.get()
            
#             if platform.system() == "Windows":
#                 # Windows uchun
#                 command = f'notepad /P "{temp_file.name}"'
#             else:
#                 # Linux/Mac uchun
#                 command = f'lpr -P "{printer_name}" -# {copies} "{temp_file.name}"'
            
#             # Chop etish jarayonini alohida threadda boshlash
#             print_thread = threading.Thread(
#                 target=self.run_print_command,
#                 args=(command, temp_file.name),
#                 daemon=True
#             )
#             print_thread.start()
            
#             self.show_status(f"Chop etish boshlanmoqda... (Printer: {printer_name})")
        
#         except Exception as e:
#             messagebox.showerror("Xato", f"Chop etishda xato:\n{str(e)}")
#             self.show_status("Chop etishda xato", "error")
    
#     def run_print_command(self, command, temp_file_path):
#         """Chop etish buyrug'ini bajarish"""
#         try:
#             subprocess.run(command, shell=True, check=True)
#             self.progress_queue.put(("success", "Telefon ma'lumotlari muvaffaqiyatli chop etildi"))
        
#         except subprocess.CalledProcessError as e:
#             self.progress_queue.put(("error", f"Chop etishda xato: {str(e)}"))
        
#         finally:
#             try:
#                 os.unlink(temp_file_path)
#             except:
#                 pass
    
#     def start_progress_monitor(self):
#         """Progress yangiliklarini kuzatish"""
#         try:
#             while True:
#                 status, message = self.progress_queue.get_nowait()
#                 if status == "success":
#                     self.show_status(message, "success")
#                 else:
#                     self.show_status(message, "error")
#         except queue.Empty:
#             pass
        
#         self.root.after(100, self.start_progress_monitor)
    
#     def show_status(self, message, status_type="info"):
#         """Status xabarini ko'rsatish"""
#         colors = {
#             "info": self.colors['primary'],
#             "success": self.colors['secondary'],
#             "error": self.colors['danger'],
#             "warning": self.colors['warning']
#         }
        
#         self.status_var.set(message)
#         self.status_label.configure(foreground=colors.get(status_type, self.colors['text']))
    
#     def run(self):
#         """Dasturni ishga tushirish"""
#         self.root.mainloop()

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = PrinterApp(root)
#     app.run()









import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext, messagebox
from tkinter.font import Font
import os
import subprocess
import platform
import queue
import threading
import tempfile
from datetime import datetime

class PrinterApp:
    def __init__(self, root):
        self.progress_queue = queue.Queue()
        self.root = root
        self.root.title("Telefon Printer Dasturi")
        self.root.state('zoomed')
        self.root.configure(bg="#f5f5f5")
        self.root.minsize(900, 700)
        
        # Telefonlar ma'lumotlari (to'g'ridan-to'g'ri kodda)
        self.phones_data = "telefon_data.json"
        self.selected_phone = None
        
        # Asosiy stillar
        self.setup_styles()
        
        # Interfeys yaratish
        self.create_interface()
        
        # Printerlarni izlash
        self.find_printers()
        
        # Telefonlar ro'yxatini to'ldirish
        self.populate_phone_list()
        
        # Progress monitor
        self.start_progress_monitor()
    
    def setup_styles(self):
        """Dizayn stillarini sozlash"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Ranglar
        self.colors = {
            'primary': '#2196F3',
            'secondary': '#4CAF50', 
            'danger': '#f44336',
            'warning': '#FF9800',
            'bg': '#f5f5f5',
            'white': '#ffffff',
            'text': '#333333'
        }
        
        # Stillar
        self.style.configure('TButton', 
                           font=('Segoe UI', 10), 
                           background=self.colors['primary'], 
                           foreground='white',
                           padding=8)
        
        self.style.configure('Success.TButton',
                           background=self.colors['secondary'])
        
        self.style.configure('Danger.TButton',
                           background=self.colors['danger'])
        
        self.style.configure('TLabel', 
                           font=('Segoe UI', 10), 
                           background=self.colors['bg'])
        
        self.style.configure('Header.TLabel', 
                           font=('Segoe UI', 16, 'bold'), 
                           background=self.colors['primary'], 
                           foreground='white')
        
        self.style.configure('TFrame', background=self.colors['bg'])
        
        self.style.configure('Card.TFrame', 
                           background=self.colors['white'],
                           relief='solid',
                           borderwidth=1)
    
    def create_interface(self):
        """Asosiy interfeys yaratish"""
        # Asosiy container
        self.main_frame = ttk.Frame(self.root, padding=(5, 2.5))
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Sarlavha
        self.create_header()
        
        # Asosiy content
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        # Chap tomon - Telefonlar ro'yxati
        self.create_phone_list()
        
        # O'ng tomon - Preview va sozlamalar
        self.create_preview_panel()
        
        # Pastki panel - Tugmalar va status
        self.create_bottom_panel()
    
    def create_header(self):
        """Sarlavha yaratish"""
        header_frame = ttk.Frame(self.main_frame, style='Card.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 5))
        
        header_label = ttk.Label(header_frame, 
                               text="📱 Telefon Printer Dasturi", 
                               style='Header.TLabel')
        header_label.pack(fill=tk.X, ipady=5)
    
    def create_phone_list(self):
        """Telefonlar ro'yxati paneli"""
        # Chap panel
        left_frame = ttk.Frame(self.content_frame, style='Card.TFrame')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Sarlavha va tugmalar
        list_header_frame = ttk.Frame(left_frame)
        list_header_frame.pack(fill=tk.X, padx=15)
        
        ttk.Label(list_header_frame, 
                 text="📋 Telefonlar Ro'yxati", 
                 font=('Segoe UI', 12, 'bold')).pack(side=tk.LEFT)
        
        # Qidiruv
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        ttk.Label(search_frame, text="🔍 Qidiruv:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_phones)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=(5, 0), fill=tk.X, expand=True)
        
        # Jadval
        table_frame = ttk.Frame(left_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        # Treeview
        columns = ("id", "nomi")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        
        # Sarlavhalar
        self.tree.heading("id", text="ID")
        self.tree.heading("nomi", text="Telefon Nomi")

        # Ustunlar kengligi
        self.tree.column("id", width=10, anchor="center")
        self.tree.column("nomi", width=30, anchor="center")

        # Scrollbar
        tree_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scrollbar.set)
        
        # Pack
        tree_scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)
        
        # Event binding
        self.tree.bind("<<TreeviewSelect>>", self.on_phone_select)
        self.tree.bind("<Double-1>", self.on_phone_double_click)
    
    def create_preview_panel(self):
        """Preview va sozlamalar paneli"""
        # O'ng panel
        right_frame = ttk.Frame(self.content_frame, style='Card.TFrame')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Preview sarlavha
        preview_header = ttk.Frame(right_frame)
        preview_header.pack(fill=tk.X, padx=15, pady=(15, 10))
        
        ttk.Label(preview_header, 
                 text="👁️ Chop Etish Ko'rinishi", 
                 font=('Segoe UI', 12, 'bold')).pack(side=tk.LEFT)
        
        # Preview matn maydoni
        self.preview_frame = ttk.Frame(right_frame)
        self.preview_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 10))
        
        self.preview_text = scrolledtext.ScrolledText(
            self.preview_frame, 
            wrap=tk.WORD, 
            font=('Segoe UI', 11),
            state='disabled',
            bg='white',
            relief='solid',
            borderwidth=1
        )
        self.preview_text.pack(fill=tk.BOTH, expand=True)
        
        # Formatlash sozlamalari
        self.create_format_settings(right_frame)
    
    def create_format_settings(self, parent):
        """Formatlash sozlamalarini yaratish"""
        format_frame = ttk.LabelFrame(parent, text="🎨 Formatlash Sozlamalari")
        format_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        # Font sozlamalari
        font_frame = ttk.Frame(format_frame)
        font_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Shrift
        ttk.Label(font_frame, text="Shrift:").grid(row=0, column=0, padx=5, sticky=tk.W)
        self.font_var = tk.StringVar(value="Segoe UI")
        font_combo = ttk.Combobox(font_frame, textvariable=self.font_var, state="readonly", width=12)
        font_combo['values'] = ("Segoe UI", "Arial", "Times New Roman", "Courier New", "Verdana")
        font_combo.grid(row=0, column=1, padx=5)
        font_combo.bind("<<ComboboxSelected>>", self.update_preview)
        
        # Hajm
        ttk.Label(font_frame, text="Hajm:").grid(row=0, column=2, padx=5, sticky=tk.W)
        self.size_var = tk.StringVar(value="11")
        size_combo = ttk.Combobox(font_frame, textvariable=self.size_var, state="readonly", width=5)
        size_combo['values'] = ("8", "9", "10", "11", "12", "14", "16", "18", "20", "24")
        size_combo.grid(row=0, column=3, padx=5)
        size_combo.bind("<<ComboboxSelected>>", self.update_preview)
        
        # Stil sozlamalari
        style_frame = ttk.Frame(format_frame)
        style_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.bold_var = tk.BooleanVar()
        bold_check = ttk.Checkbutton(style_frame, text="Qalin", variable=self.bold_var, command=self.update_preview)
        bold_check.pack(side=tk.LEFT, padx=10)
        
        self.italic_var = tk.BooleanVar()
        italic_check = ttk.Checkbutton(style_frame, text="Kursiv", variable=self.italic_var, command=self.update_preview)
        italic_check.pack(side=tk.LEFT, padx=10)
        
        self.underline_var = tk.BooleanVar()
        underline_check = ttk.Checkbutton(style_frame, text="Chiziq", variable=self.underline_var, command=self.update_preview)
        underline_check.pack(side=tk.LEFT, padx=10)
    
    def create_bottom_panel(self):
        """Pastki panel - printer sozlamalari va tugmalar"""
        bottom_frame = ttk.Frame(self.main_frame, style='Card.TFrame')
        bottom_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Printer sozlamalari
        printer_frame = ttk.LabelFrame(bottom_frame, text="🖨️ Printer Sozlamalari")
        printer_frame.pack(fill=tk.X, padx=15, pady=15)
        
        settings_frame = ttk.Frame(printer_frame)
        settings_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Printer tanlash
        ttk.Label(settings_frame, text="Printer:").grid(row=0, column=0, padx=5, sticky=tk.W)
        self.printer_var = tk.StringVar()
        self.printer_combo = ttk.Combobox(settings_frame, textvariable=self.printer_var, state="readonly", width=30)
        self.printer_combo.grid(row=0, column=1, padx=5)
        
        refresh_btn = ttk.Button(settings_frame, text="🔄", command=self.find_printers, width=5)
        refresh_btn.grid(row=0, column=2, padx=5)
        
        # Nusxalar soni
        ttk.Label(settings_frame, text="Nusxalar:").grid(row=0, column=3, padx=(20, 5), sticky=tk.W)
        self.copies_var = tk.StringVar(value="1")
        copies_spin = ttk.Spinbox(settings_frame, from_=1, to=99, width=5, textvariable=self.copies_var)
        copies_spin.grid(row=0, column=4, padx=5)
        
        # Boshqa sozlamalar
        options_frame = ttk.Frame(settings_frame)
        options_frame.grid(row=1, column=0, columnspan=5, pady=(10, 0), sticky=tk.W)
        
        self.color_var = tk.BooleanVar(value=True)
        color_check = ttk.Checkbutton(options_frame, text="Rangli", variable=self.color_var)
        color_check.pack(side=tk.LEFT, padx=10)
        
        self.duplex_var = tk.BooleanVar()
        duplex_check = ttk.Checkbutton(options_frame, text="Ikki tomonlama", variable=self.duplex_var)
        duplex_check.pack(side=tk.LEFT, padx=10)
        
        # Tugmalar
        buttons_frame = ttk.Frame(bottom_frame)
        buttons_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        # Chap tomon tugmalar
        left_buttons = ttk.Frame(buttons_frame)
        left_buttons.pack(side=tk.LEFT)
        
        edit_btn = ttk.Button(left_buttons, text="✏️ Tahrirlash", command=self.edit_selected_phone, width=15)
        edit_btn.pack(side=tk.LEFT, padx=5)
        
        # O'ng tomon tugmalar
        right_buttons = ttk.Frame(buttons_frame)
        right_buttons.pack(side=tk.RIGHT)
        
        self.print_btn = ttk.Button(right_buttons, text="🖨️ Chop Etish", command=self.print_selected, 
                                  style='Success.TButton', width=15)
        self.print_btn.pack(side=tk.RIGHT, padx=5)
        self.print_btn.configure(state='disabled')
        
        # Status
        self.status_frame = ttk.Frame(bottom_frame)
        self.status_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        self.status_var = tk.StringVar(value="Tizimga xush kelibsiz! Telefon tanlang")
        self.status_label = ttk.Label(self.status_frame, textvariable=self.status_var, foreground=self.colors['primary'])
        self.status_label.pack(side=tk.LEFT)
    
    def populate_phone_list(self):
        """Telefonlar ro'yxatini to'ldirish"""
        # Oldingi ma'lumotlarni tozalash
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Yangi ma'lumotlarni qo'shish
        for i, phone in enumerate(self.phones_data, 1):
            try:
                self.tree.insert("", tk.END, values=(
                    i,
                    phone.get('nomi', 'N/A'),
                    phone.get('nomi', 'N/A'),
                ))
            except Exception as e:
                print(f"Ma'lumot qo'shishda xato: {e}")
    
    def filter_phones(self, *args):
        """Telefonlarni qidirish bo'yicha filtrlash"""
        search_term = self.search_var.get().lower()
        
        # Oldingi ma'lumotlarni tozalash
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Filtrlangan ma'lumotlarni qo'shish
        filtered_count = 0
        for i, phone in enumerate(self.phones_data, 1):
            if search_term in phone.get('nomi', '').lower():
                self.tree.insert("", tk.END, values=(
                    i,
                    phone.get('nomi', 'N/A'),
                ))
                filtered_count += 1
        
        if search_term:
            self.show_status(f"{filtered_count} ta telefon topildi")
    
    def on_phone_select(self, event):
        """Telefon tanlanganida"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        phone_id = item['values'][0] - 1  # Index 0 dan boshlanadi
        
        if 0 <= phone_id < len(self.phones_data):
            self.selected_phone = self.phones_data[phone_id]
            self.update_preview()
            self.print_btn.configure(state='normal')
            self.show_status(f"Telefon tanlandi: {self.selected_phone.get('nomi', 'N/A')}")
    
    def on_phone_double_click(self, event):
        """Telefonga ikki marta bosganda tahrirlash"""
        self.edit_selected_phone()
    
    def update_preview(self, *args):
        """Preview matnini yangilash"""
        if not self.selected_phone:
            self.preview_text.configure(state='normal')
            self.preview_text.delete('1.0', tk.END)
            self.preview_text.insert(tk.END, "Telefon tanlanmagan...")
            self.preview_text.configure(state='disabled')
            return
        
        # Matn yaratish
        text_content = self.format_phone_info(self.selected_phone)
        
        # Font sozlash
        font_family = self.font_var.get()
        font_size = int(self.size_var.get())
        font_weight = "bold" if self.bold_var.get() else "normal"
        font_slant = "italic" if self.italic_var.get() else "roman"
        
        preview_font = Font(
            family=font_family,
            size=font_size,
            weight=font_weight,
            slant=font_slant,
            underline=self.underline_var.get()
        )
        
        # Preview yangilash
        self.preview_text.configure(state='normal', font=preview_font)
        self.preview_text.delete('1.0', tk.END)
        self.preview_text.insert(tk.END, text_content)
        self.preview_text.configure(state='disabled')
    
    def format_phone_info(self, phone):
        """Telefon ma'lumotlarini formatlash"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        text = f"""
            ╔══════════════════════════════════════════════════════════════╗
            ║                    TELEFON MA'LUMOTLARI                      ║
            ╠══════════════════════════════════════════════════════════════╣
            ║                                                              ║
            ║  📱 Telefon Nomi:  {phone.get('nomi', 'N/A'):<40} ║
            ║                                                              ║
            ║  🔢 IMEI Raqam:    {phone.get('imei', 'N/A'):<40} ║
            ║                                                              ║
            ║  💰 Narx:          {phone.get('narx', 'N/A'):<40} ║
            ║                                                              ║
            ║  📅 Sana:          {phone.get('sana', 'N/A'):<40} ║
            ║                                                              ║
            ╠══════════════════════════════════════════════════════════════╣
            ║  Chop etilgan:     {current_time:<40} ║
            ╚══════════════════════════════════════════════════════════════╝

            Diqqat: Bu hujjat rasmiy hisobot hisoblanadi.
            Barcha ma'lumotlar to'g'riligini tekshiring.

            --------------------------------
            Imzo: _______________  Sana: _______________

        """
        return text.strip()
    
    def edit_selected_phone(self):
        """Tanlangan telefonni tahrirlash"""
        if not self.selected_phone:
            messagebox.showwarning("Ogohlantirish", "Avval telefon tanlang!")
            return
        
        # Tahrirlash oynasi
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Telefon Ma'lumotlarini Tahrirlash")
        edit_window.geometry("500x500")
        edit_window.configure(bg=self.colors['bg'])
        edit_window.transient(self.root)
        edit_window.grab_set()
        
        # Sarlavha
        header = ttk.Label(edit_window, text="✏️ Telefon Ma'lumotlarini Tahrirlash", 
                          font=('Segoe UI', 14, 'bold'))
        header.pack(pady=20)
        
        # Ma'lumotlar kiritish
        main_frame = ttk.Frame(edit_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # O'zgaruvchilar
        vars_dict = {}
        fields = [
            ('nomi', 'Telefon Nomi:', 'text'),
            ('imei', 'IMEI Raqam:', 'text'),
            ('narx', 'Narx:', 'text'),
            ('sana', 'Sana:', 'text')
        ]
        
        for i, (key, label, field_type) in enumerate(fields):
            ttk.Label(main_frame, text=label, font=('Segoe UI', 10, 'bold')).grid(
                row=i, column=0, sticky=tk.W, pady=5, padx=(0, 10))
            
            vars_dict[key] = tk.StringVar(value=self.selected_phone.get(key, ''))
            
            entry = ttk.Entry(main_frame, textvariable=vars_dict[key], width=40, font=('Segoe UI', 10))
            entry.grid(row=i, column=1, sticky=tk.W+tk.E, pady=5)
        
        # Tugmalar
        buttons_frame = ttk.Frame(edit_window)
        buttons_frame.pack(fill=tk.X, pady=20)
        
        def save_changes():
            try:
                # Ma'lumotlarni yangilash
                phone_index = self.phones_data.index(self.selected_phone)
                for key, var in vars_dict.items():
                    self.phones_data[phone_index][key] = var.get()
                
                # Jadval va preview yangilash
                self.populate_phone_list()
                self.selected_phone = self.phones_data[phone_index]
                self.update_preview()
                
                edit_window.destroy()
                self.show_status("Ma'lumotlar yangilandi")
                
            except Exception as e:
                messagebox.showerror("Xato", f"Ma'lumotlarni saqlashda xato:\n{str(e)}")
        
        save_btn = ttk.Button(buttons_frame, text="💾 Saqlash", command=save_changes, 
                            style='Success.TButton')
        save_btn.pack(side=tk.RIGHT, padx=5)
        
        cancel_btn = ttk.Button(buttons_frame, text="❌ Bekor qilish", command=edit_window.destroy)
        cancel_btn.pack(side=tk.RIGHT, padx=5)
    
    def find_printers(self):
        """Mavjud printerlarni topish"""
        try:
            if platform.system() == "Windows":
                import win32print
                printers = [printer[2] for printer in win32print.EnumPrinters(2)]
            else:
                # Linux/Mac uchun
                printers = [line.split()[0] for line in subprocess.check_output(["lpstat", "-a"]).decode().splitlines()]
            
            self.printer_combo['values'] = printers
            if printers:
                self.printer_var.set(printers[0])
                self.show_status(f"{len(printers)} ta printer topildi")
            else:
                self.show_status("Printer topilmadi", "error")
        
        except Exception as e:
            self.show_status(f"Printerlarni topishda xato: {str(e)}", "error")
            self.printer_combo['values'] = []
    
    def print_selected(self):
        """Tanlangan telefonni chop etish"""
        if not self.selected_phone:
            messagebox.showwarning("Ogohlantirish", "Avval telefon tanlang!")
            return
        
        if not self.printer_var.get():
            messagebox.showwarning("Ogohlantirish", "Printer tanlanmagan!")
            return
        
        try:
            # Vaqtinchalik fayl yaratish
            temp_file = tempfile.NamedTemporaryFile(mode='w+', suffix='.txt', delete=False, encoding='utf-8')
            temp_file.write(self.format_phone_info(self.selected_phone))
            temp_file.close()
            
            # Printer buyrug'i
            printer_name = self.printer_var.get()
            copies = self.copies_var.get()
            
            if platform.system() == "Windows":
                # Windows uchun
                command = f'notepad /P "{temp_file.name}"'
            else:
                # Linux/Mac uchun
                command = f'lpr -P "{printer_name}" -# {copies} "{temp_file.name}"'
            
            # Chop etish jarayonini alohida threadda boshlash
            print_thread = threading.Thread(
                target=self.run_print_command,
                args=(command, temp_file.name),
                daemon=True
            )
            print_thread.start()
            
            self.show_status(f"Chop etish boshlanmoqda... (Printer: {printer_name})")
        
        except Exception as e:
            messagebox.showerror("Xato", f"Chop etishda xato:\n{str(e)}")
            self.show_status("Chop etishda xato", "error")
    
    def run_print_command(self, command, temp_file_path):
        """Chop etish buyrug'ini bajarish"""
        try:
            subprocess.run(command, shell=True, check=True)
            self.progress_queue.put(("success", "Telefon ma'lumotlari muvaffaqiyatli chop etildi"))
        
        except subprocess.CalledProcessError as e:
            self.progress_queue.put(("error", f"Chop etishda xato: {str(e)}"))
        
        finally:
            try:
                os.unlink(temp_file_path)
            except:
                pass
    
    def start_progress_monitor(self):
        """Progress yangiliklarini kuzatish"""
        try:
            while True:
                status, message = self.progress_queue.get_nowait()
                if status == "success":
                    self.show_status(message, "success")
                else:
                    self.show_status(message, "error")
        except queue.Empty:
            pass
        
        self.root.after(100, self.start_progress_monitor)
    
    def show_status(self, message, status_type="info"):
        """Status xabarini ko'rsatish"""
        colors = {
            "info": self.colors['primary'],
            "success": self.colors['secondary'],
            "error": self.colors['danger'],
            "warning": self.colors['warning']
        }
        
        self.status_var.set(message)
        self.status_label.configure(foreground=colors.get(status_type, self.colors['text']))
    
    def run(self):
        """Dasturni ishga tushirish"""
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = PrinterApp(root)
    app.run()