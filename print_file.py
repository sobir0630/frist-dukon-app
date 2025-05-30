import tkinter as tk
import tkinter.ttk as ttk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from tkinter.font import Font
import os
import sys
import tempfile
import threading
import time
import subprocess
import platform
import queue

class PrinterApp:
    def __init__(self, root):
        self.progress_queue = queue.Queue()
        self.root = root
        self.root.title("Printer Dasturi")
        self.root.state('zoomed')
        self.root.configure(bg="#f5f5f5")
        self.root.minsize(700, 600)
        
        # Asosiy stillar
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Segoe UI', 10), background='#4285f4', foreground='white')
        self.style.configure('TLabel', font=('Segoe UI', 10), background='#f5f5f5')
        self.style.configure('Header.TLabel', font=('Segoe UI', 12, 'bold'), background='#4285f4', foreground='white')
        self.style.configure('TFrame', background='#f5f5f5')
        
        # Asosiy container
        self.main_frame = ttk.Frame(self.root, padding=(20, 10))
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Sarlavha
        self.header_frame = ttk.Frame(self.main_frame, style='Header.TFrame')
        self.header_frame.pack(fill=tk.X, pady=(0, 15))
        
        header_label = ttk.Label(self.header_frame, text="Printer Dasturi", font=('Segoe UI', 16, 'bold'), background='#4285f4', foreground='white')
        header_label.pack(fill=tk.X, ipady=10)
        
        # Standart matn bloki
        self.default_text_frame = ttk.Frame(self.main_frame, relief=tk.GROOVE, borderwidth=1)
        self.default_text_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.default_text = ttk.Label(self.default_text_frame, text="Bu yerda standart matn. Uni o'zgartiring yoki pastdagi maydonni to'ldiring.", padding=10, wraplength=750)
        self.default_text.pack(fill=tk.X)
        
        # Matn kiritish maydoni
        self.text_frame = ttk.Frame(self.main_frame)
        self.text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.text_label = ttk.Label(self.text_frame, text="Chop etish uchun matn:")
        self.text_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.text_area = scrolledtext.ScrolledText(self.text_frame, wrap=tk.WORD, font=('Segoe UI', 11))
        self.text_area.pack(fill=tk.BOTH, expand=True)
        self.text_area.insert(tk.END, self.default_text.cget("text"))
        
        # Formatlar paneli
        self.format_frame = ttk.LabelFrame(self.main_frame, text="Formatlash")
        self.format_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Font va o'lcham
        self.format_options_frame = ttk.Frame(self.format_frame)
        self.format_options_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(self.format_options_frame, text="Shrift:").grid(row=0, column=0, padx=(0, 5))
        self.font_var = tk.StringVar(value="Segoe UI")
        self.font_combo = ttk.Combobox(self.format_options_frame, textvariable=self.font_var, state="readonly", width=15)
        self.font_combo['values'] = ("Segoe UI", "Arial", "Times New Roman", "Courier New", "Verdana")
        self.font_combo.grid(row=0, column=1, padx=5)
        self.font_combo.bind("<<ComboboxSelected>>", self.update_text_format)
        
        ttk.Label(self.format_options_frame, text="Hajmi:").grid(row=0, column=2, padx=5)
        self.size_var = tk.StringVar(value="11")
        self.size_combo = ttk.Combobox(self.format_options_frame, textvariable=self.size_var, state="readonly", width=5)
        self.size_combo['values'] = ("8", "9", "10", "11", "12", "14", "16", "18", "20", "24")
        self.size_combo.grid(row=0, column=3, padx=5)
        self.size_combo.bind("<<ComboboxSelected>>", self.update_text_format)
        
        # Tugmalar: qalin, kursiv, tagiga chizish
        self.bold_var = tk.BooleanVar(value=False)
        self.bold_check = ttk.Checkbutton(self.format_options_frame, text="Qalin", variable=self.bold_var, command=self.update_text_format)
        self.bold_check.grid(row=0, column=4, padx=10)
        
        self.italic_var = tk.BooleanVar(value=False)
        self.italic_check = ttk.Checkbutton(self.format_options_frame, text="Kursiv", variable=self.italic_var, command=self.update_text_format)
        self.italic_check.grid(row=0, column=5, padx=10)
        
        self.underline_var = tk.BooleanVar(value=False)
        self.underline_check = ttk.Checkbutton(self.format_options_frame, text="Tagiga chizish", variable=self.underline_var, command=self.update_text_format)
        self.underline_check.grid(row=0, column=6, padx=10)
        
        # Printer sozlamalari
        self.settings_frame = ttk.LabelFrame(self.main_frame, text="Printer sozlamalari")
        self.settings_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.settings_inner_frame = ttk.Frame(self.settings_frame)
        self.settings_inner_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Printer tanlash
        ttk.Label(self.settings_inner_frame, text="Printer:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.printer_var = tk.StringVar()
        self.printer_combo = ttk.Combobox(self.settings_inner_frame, textvariable=self.printer_var, state="readonly", width=30)
        self.printer_combo.grid(row=0, column=1, sticky=tk.W, padx=(0, 10))
        
        self.refresh_btn = ttk.Button(self.settings_inner_frame, text="🔄 Yangilash", command=self.find_printers, width=10)
        self.refresh_btn.grid(row=0, column=2, padx=5)
        
        # Chop etish parametrlari
        self.param_frame = ttk.Frame(self.settings_frame)
        self.param_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Chap tomon - flags
        self.flags_frame = ttk.Frame(self.param_frame)
        self.flags_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.color_var = tk.BooleanVar(value=True)
        self.color_check = ttk.Checkbutton(self.flags_frame, text="Rangli chop etish", variable=self.color_var)
        self.color_check.pack(anchor=tk.W)
        
        self.duplex_var = tk.BooleanVar(value=False)
        self.duplex_check = ttk.Checkbutton(self.flags_frame, text="Ikki tomonlama chop etish", variable=self.duplex_var)
        self.duplex_check.pack(anchor=tk.W)
        
        # O'ng tomon - sonli parametrlar
        self.num_frame = ttk.Frame(self.param_frame)
        self.num_frame.pack(side=tk.RIGHT, fill=tk.X)
        
        ttk.Label(self.num_frame, text="Nusxalar soni:").grid(row=0, column=0, padx=(0, 5))
        self.copies_var = tk.StringVar(value="1")
        self.copies_spin = ttk.Spinbox(self.num_frame, from_=1, to=99, width=5, textvariable=self.copies_var)
        self.copies_spin.grid(row=0, column=1)
        
        # Tugmalar qismi
        self.buttons_frame = ttk.Frame(self.main_frame)
        self.buttons_frame.pack(fill=tk.X, pady=(0, 10))
        
        button_style = {'width': 15, 'padding': 5}
        
        self.print_btn = ttk.Button(self.buttons_frame, text="Chop etish", command=self.print_text, **button_style)
        self.print_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.preview_btn = ttk.Button(self.buttons_frame, text="Ko'rib chiqish", command=self.preview_text, **button_style)
        self.preview_btn.pack(side=tk.LEFT, padx=10)
        
        self.clear_btn = ttk.Button(self.buttons_frame, text="Tozalash", command=self.clear_text, **button_style)
        self.clear_btn.pack(side=tk.LEFT, padx=10)
        
        self.save_btn = ttk.Button(self.buttons_frame, text="Saqlash", command=self.save_text, **button_style)
        self.save_btn.pack(side=tk.LEFT, padx=10)
        
        self.open_btn = ttk.Button(self.buttons_frame, text="Ochish", command=self.open_text, **button_style)
        self.open_btn.pack(side=tk.LEFT, padx=10)
        self.view_print_screen = ttk.Button(self.buttons_frame, text="jadval tanlash", command=self.open_text, **button_style)
        self.view_print_screen.pack(side=tk.LEFT, padx=10)
        
        # Status qismi
        self.status_frame = ttk.Frame(self.main_frame)
        self.status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_var = tk.StringVar()
        self.status_label = ttk.Label(self.status_frame, textvariable=self.status_var, foreground="#4285f4")
        self.status_label.pack(anchor=tk.W)
        
        # Printerlarni izlash
        self.find_printers()
        
        # Status o'chirish uchun timer
        self.status_timer = None
        
        # Yuklash ko'rsatkichi uchun
        self.progress_queue = queue.Queue()
        self.start_progress_monitor()
    
    def update_text_format(self, event=None):
        """Matn formatini yangilash"""
        try:
            # Joriy font parametrlarini olish
            font_family = self.font_var.get()
            font_size = int(self.size_var.get())
            
            # Font stilini aniqlash
            font_style = ""
            if self.bold_var.get():
                font_style += " bold"
            if self.italic_var.get():
                font_style += " italic"
                
            # Yangi font yaratish
            new_font = Font(
                family=font_family,
                size=font_size,
                weight="bold" if self.bold_var.get() else "normal",
                slant="italic" if self.italic_var.get() else "roman",
                underline=self.underline_var.get()
            )
            
            # Matn maydoniga yangi shriftni qo'llash
            self.text_area.configure(font=new_font)
            
        except Exception as e:
            self.show_status(f"Shriftni yangilashda xatolik: {str(e)}", "error")

    def find_printers(self):
        """Tizimdan mavjud printerlarni topish"""
        self.status_var.set("Printerlar izlanmoqda...")
        
        def find_printers_thread():
            printers = self.get_system_printers()
            self.progress_queue.put(("finish", None))
            
            if printers:
                self.root.after(0, lambda: self.update_printers_list(printers))
            else:
                self.root.after(0, lambda: self.show_status("Printer topilmadi. Printeringiz ulanganligini tekshiring", "error"))
        
        try:
            self.progress_queue.put(("start", None))
        except queue.Full:
            self.show_status("Progress queue is full. Unable to add task.", "error")
        threading.Thread(target=find_printers_thread, daemon=True).start()
    
    def get_system_printers(self):
        """Operatsion tizimga qarab printerlarni olish"""
        printers = []
        system = platform.system()
        
        try:
            if system == "Windows":
                # Windows tizimida printerlarni olish
                import win32print
                printers = [printer[2] for printer in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL)]
            
            elif system == "Darwin":  # macOS
                # macOS tizimida printerlarni olish
                result = subprocess.run(["lpstat", "-p"], capture_output=True, text=True)
                if result.stdout:
                    for line in result.stdout.split('\n'):
                        if line.startswith("printer"):
                            printers.append(line.split()[1])
            
            elif system == "Linux":
                # Linux tizimida printerlarni olish
                result = subprocess.run(["lpstat", "-a"], capture_output=True, text=True)
                if result.stdout:
                    for line in result.stdout.split('\n'):
                        if line:
                            printers.append(line.split()[0])
        
        except Exception as e:
            self.show_status(f"Printerlarni olishda xatolik: {str(e)}", "error")
        
        return printers
    
    def update_printers_list(self, printers):
        """Printerlar ro'yxatini yangilash"""
        self.printer_combo['values'] = printers
        
        if printers:
            self.printer_combo.current(0)
            self.show_status(f"{len(printers)} ta printer topildi")
        else:
            self.printer_var.set("")
            self.show_status("Printerlar topilmadi", "error")
    
# Removed duplicate definition of PrinterApp class

    
    def print_text(self):
        """Matnni chop etish"""
        if not self.text_area.get("1.0", tk.END).strip():
            self.show_status("Chop etish uchun matn kiriting!", "error")
            return
        
        if not self.printer_var.get():
            self.show_status("Printer tanlanmagan!", "error")
            return
        
        self.status_var.set("Chop etishga tayyorlanmoqda...")
        
        def print_thread():
            try:
                self.progress_queue.put(("start", None))
                
                text_content = self.text_area.get("1.0", tk.END)
                printer_name = self.printer_var.get()
                copies = int(self.copies_var.get())
                color_mode = "color" if self.color_var.get() else "monochrome"
                duplex = self.duplex_var.get()
                
                # Vaqtinchalik fayl yaratish
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8")
                temp_file.write(text_content)
                temp_file.close()
                
                system = platform.system()
                
                if system == "Windows":
                    self._print_windows(temp_file.name, printer_name, copies, color_mode, duplex)
                elif system in ["Darwin", "Linux"]:
                    self._print_unix(temp_file.name, printer_name, copies, color_mode, duplex)
                else:
                    self.root.after(0, lambda: self.show_status(f"Noma'lum operatsion tizim: {system}", "error"))
                
                # Vaqtinchalik faylni o'chirish
                try:
                    os.unlink(temp_file.name)
                except:
                    pass
                
                self.progress_queue.put(("finish", None))
                self.root.after(0, lambda: self.show_status("Chop etish topshirig'i yuborildi"))
            
            except Exception as e:
                self.progress_queue.put(("finish", None))
                self.root.after(0, lambda: self.show_status(f"Chop etishda xato: {str(e)}", "error"))
        
        threading.Thread(target=print_thread, daemon=True).start()
    
    def _print_windows(self, filename, printer_name, copies, color_mode, duplex):
        """Windows'da chop etish"""
        try:
            import win32print
            import win32api
            
            # Printer tanlaymiz
            win32print.SetDefaultPrinter(printer_name)
            
            # Chop etish
            win32api.ShellExecute(0, "print", filename, f'/d:"{printer_name}"', ".", 0)
            
        except ImportError:
            # Win32print mavjud emas, oddiy usul bilan urinib ko'ramiz
            subprocess.run(["notepad", "/p", filename], check=True)
    
    def _print_unix(self, filename, printer_name, copies, color_mode, duplex):
        """Unix tizimlarida (macOS, Linux) chop etish"""
        cmd = ["lpr", "-P", printer_name, "-#", str(copies)]
        
        if color_mode == "monochrome":
            cmd.extend(["-o", "ColorModel=Gray"])
        
        if duplex:
            cmd.extend(["-o", "sides=two-sided-long-edge"])
        
        cmd.append(filename)
        
        subprocess.run(cmd, check=True)
    
    def preview_text(self):
        """Chop etishdan oldin ko'rib chiqish"""
        if not self.text_area.get("1.0", tk.END).strip():
            self.show_status("Ko'rib chiqish uchun matn kiriting!", "error")
            return
        
        # Ko'rib chiqish oynasi
        preview_window = tk.Toplevel(self.root)
        preview_window.title("Ko'rib chiqish")
        preview_window.geometry("700x500")
        preview_window.minsize(500, 400)
        
        # Header
        header_frame = ttk.Frame(preview_window, style='Header.TFrame')
        header_frame.pack(fill=tk.X)
        
        header_label = ttk.Label(header_frame, text="Chop etish uchun ko'rib chiqish", 
                              font=('Segoe UI', 14, 'bold'), background='#4285f4', foreground='white')
        header_label.pack(fill=tk.X, ipady=10)
        
        # Matn bloki
        preview_frame = ttk.Frame(preview_window, padding=20)
        preview_frame.pack(fill=tk.BOTH, expand=True)
        
        preview_text = scrolledtext.ScrolledText(preview_frame, font=self.text_area.cget("font"), wrap=tk.WORD)
        preview_text.pack(fill=tk.BOTH, expand=True)
        preview_text.insert(tk.END, self.text_area.get("1.0", tk.END))
        preview_text.configure(state="disabled")
        
        # Tagiga chizish (underline) ko'chirib o'tkazish
        if self.underline_var.get():
            preview_text.tag_configure("underline", underline=True)
            preview_text.tag_add("underline", "1.0", tk.END)
        
        # Tugmalar bloki
        buttons_frame = ttk.Frame(preview_window, padding=10)
        buttons_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        # print_btn = ttk.Button(buttons_frame, text="Chop etish", command=lambda: [preview_window.destroy(), self.print_text()])
        # print_btn.pack(side=tk.LEFT, padx=5)
        
        close_btn = ttk.Button(buttons_frame, text="Yopish", command=preview_window.destroy)
        close_btn.pack(side=tk.LEFT, padx=5)
        
        # Oynani modalga aylantirish
        preview_window.transient(self.root)
        preview_window.grab_set()
        self.root.wait_window(preview_window)
    
    def clear_text(self):
        """Matn maydonini tozalash"""
        self.text_area.delete("1.0", tk.END)
        self.show_status("Matn tozalandi")
    
    def save_text(self):
        """Matnni faylga saqlash"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Faylni saqlash"
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(self.text_area.get("1.0", tk.END))
            
            self.show_status(f"Fayl saqlandi: {os.path.basename(file_path)}")
        
        except Exception as e:
            self.show_status(f"Faylni saqlashda xato: {str(e)}", "error")
    
    def open_text(self):
        """Fayldan matn ochish"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Faylni ochish"
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, content)
            
            self.show_status(f"Fayl ochildi: {os.path.basename(file_path)}")
        
        except Exception as e:
            self.show_status(f"Faylni ochishda xato: {str(e)}", "error")
    
    def show_status(self, message, message_type="info"):
        """Status xabarini ko'rsatish"""
        if message_type == "error":
            self.status_label.configure(foreground="#d32f2f")
        else:
            self.status_label.configure(foreground="#4285f4")
        
        self.status_var.set(message)
        
        # Agar timer mavjud bo'lsa, uni bekor qilamiz
        if self.status_timer is not None:
            self.root.after_cancel(self.status_timer)
        
        # 5 soniyadan keyin xabarni tozalash
        self.status_timer = self.root.after(5000, lambda: self.status_var.set(""))
    
    def start_progress_monitor(self):
        """Yuklash ko'rsatkichi monitoringini boshlash"""
        self.progress_bar = None
        self.progress_step = 0
        
        def check_progress():
            try:
                while True:
                    cmd, data = self.progress_queue.get_nowait()
                    
                    if cmd == "start":
                        self.start_progress()
                    elif cmd == "finish":
                        self.stop_progress()
            except queue.Empty:
                pass
            
            self.root.after(100, check_progress)
        
        check_progress()
    
    def start_progress(self):
        """Yuklash ko'rsatkichini yaratish"""
        if self.progress_bar is None:
            self.progress_bar = ttk.Progressbar(self.status_frame, mode="indeterminate", length=200)
            self.progress_bar.pack(fill=tk.X, pady=(5, 0))
            self.progress_bar.start()
    
    def stop_progress(self):
        """Yuklash ko'rsatkichini to'xtatish va o'chirish"""
        if self.progress_bar is not None:
            self.progress_bar.stop()
            self.progress_bar.destroy()
            self.progress_bar = None
    
    def view_phone_list(self):
        """Telefonlar ro'yxatini ko'rsatish"""
        # Yangi oyna
        list_window = tk.Toplevel(self.root)
        list_window.title("Telefon tanlash")
        list_window.geometry("800x600")
        list_window.configure(bg="#f5f5f5")
        
        # Sarlavha
        header = ttk.Label(list_window, 
                          text="🖨️ Chop etish uchun telefon tanlang",
                          font=("Arial", 16, "bold"))
        header.pack(pady=(15, 10))

        # Jadval
        table_frame = ttk.Frame(list_window)
        table_frame.pack(pady=10, padx=20, fill="both", expand=True)

        columns = ("id", "phone", "model", "price", "date")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        
        tree.heading("id", text="ID")
        tree.heading("phone", text="Telefon nomi")
        tree.heading("model", text="IMEI")
        tree.heading("price", text="Narxi")
        tree.heading("date", text="Sana")

        # Ustunlar kengligi
        tree.column("id", width=50, anchor="center")
        tree.column("phone", width=150, anchor="center")
        tree.column("model", width=150, anchor="center")
        tree.column("price", width=100, anchor="center")
        tree.column("date", width=100, anchor="center")

        # Skroll
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(side="left", fill="both", expand=True)
    def view_phone_list(self):
        """Telefonlar ro'yxatini ko'rsatish"""
        # Yangi oyna
        list_window = tk.Toplevel(self.root)
        list_window.title("Telefon tanlash")
        list_window.geometry("800x600")
        list_window.configure(bg="#f5f5f5")
        
        # Sarlavha
        header = ttk.Label(list_window, 
                          text="🖨️ Chop etish uchun telefon tanlang",
                          font=("Arial", 16, "bold"))
        header.pack(pady=(15, 10))

        # Jadval
        table_frame = ttk.Frame(list_window)
        table_frame.pack(pady=10, padx=20, fill="both", expand=True)

        columns = ("id", "phone", "model", "price", "date")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        
        tree.heading("id", text="ID")
        tree.heading("phone", text="Telefon nomi")
        tree.heading("model", text="IMEI")
        tree.heading("price", text="Narxi")
        tree.heading("date", text="Sana")

        # Ustunlar kengligi
        tree.column("id", width=50, anchor="center")
        tree.column("phone", width=150, anchor="center")
        tree.column("model", width=150, anchor="center")
        tree.column("price", width=100, anchor="center")
        tree.column("date", width=100, anchor="center")

        # Skroll
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(side="left", fill="both", expand=True)

        def print_selected():
            selected = tree.selection()
            if not selected:
                messagebox.showerror("Xato", "Telefon tanlanmagan!")
                return
                
            item = tree.item(selected[0])
            phone_data = {
                "nomi": item['values'][1],
                "modeli": item['values'][2],
                "narx": item['values'][3],
                "sana": item['values'][4]
            }
            
            # Tanlangan ma'lumotni matn maydoniga qo'yish
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, f"""
Telefon ma'lumotlari:
-------------------
Nomi: {phone_data['nomi']}
IMEI: {phone_data['modeli']}
Narx: {phone_data['narx']}
Sana: {phone_data['sana']}
""")
            list_window.destroy()

        # Tugmalar
        btn_frame = ttk.Frame(list_window)
        btn_frame.pack(pady=15)

        print_btn = ttk.Button(btn_frame, 
                             text="Tanlash", 
                             command=print_selected)
        print_btn.pack(side=tk.LEFT, padx=5)

        close_btn = ttk.Button(btn_frame, 
                             text="Yopish",
                             command=list_window.destroy)
        close_btn.pack(side=tk.LEFT, padx=5)
    
def view_print_screen():
    
#    return print_file.view_print_screen()
    
    if not phones:
        messagebox.showerror(translations[language]["error"], "Telefonlar mavjud emas!")
        return

    print_window = tk.Toplevel(root_app)
    print_window.title("Chop etish bo'limi")
    print_window.geometry("800x600")
    print_window.configure(bg=colors["bg"])
    center_window(print_window)

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



def main():
    root = tk.Tk()
    app = PrinterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()