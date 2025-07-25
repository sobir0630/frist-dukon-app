import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import json
import os
import sys
import hashlib
import subprocess

# CustomTkinter sozlamalari
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class PasswordManager:
    def __init__(self):
        self.PASSWORDS_FILE = "app_config.json"
        self.CODES_FILE = "internal_codes.json"
        self.DEFAULT_LOGIN_PASSWORD = "9959"
        self.DEFAULT_INTERNAL_PASSWORD = "IDEAL_MOBILE+998995999959"
        self.USERNAME = "IDEAL MOBILE"
        
    def hash_password(self, password):
        """Parolni hash qilish"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def load_config(self):
        """Dastur konfiguratsiyasini yuklash"""
        if os.path.exists(self.PASSWORDS_FILE):
            try:
                with open(self.PASSWORDS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data
            except Exception:
                return self.create_default_config()
        else:
            return self.create_default_config()
    
    def create_default_config(self):
        """Standart konfiguratsiya yaratish"""
        config = {
            "login_password": self.hash_password(self.DEFAULT_LOGIN_PASSWORD),
            "internal_password": self.hash_password(self.DEFAULT_INTERNAL_PASSWORD),
            "username": self.USERNAME
        }
        self.save_config(config)
        return config
    
    def save_config(self, config):
        """Konfiguratsiyani saqlash"""
        try:
            with open(self.PASSWORDS_FILE, "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Xatolik", f"Konfiguratsiyani saqlashda xatolik: {str(e)}")
    
    def load_internal_codes(self):
        """Ichki kodlarni yuklash"""
        if os.path.exists(self.CODES_FILE):
            try:
                with open(self.CODES_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return self.create_default_codes()
        else:
            return self.create_default_codes()
    
    def create_default_codes(self):
        """Standart ichki kodlar yaratish"""
        codes = {
            "IDEAL MOBILE": "ichki123"
        }
        self.save_internal_codes(codes)
        return codes
    
    def save_internal_codes(self, codes):
        """Ichki kodlarni saqlash"""
        try:
            with open(self.CODES_FILE, "w", encoding="utf-8") as f:
                json.dump(codes, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Xatolik", f"Kodlarni saqlashda xatolik: {str(e)}")
    
    def verify_login_password(self, password):
        """Kirish parolini tekshirish"""
        config = self.load_config()
        return self.hash_password(password) == config["login_password"]
    
    def verify_internal_password(self, password):
        """Ichki parolni tekshirish"""
        config = self.load_config()
        return self.hash_password(password) == config["internal_password"]
    
    def change_login_password(self, current_password, new_password):
        """Kirish parolini o'zgartirish"""
        if self.verify_login_password(current_password):
            config = self.load_config()
            config["login_password"] = self.hash_password(new_password)
            self.save_config(config)
            return True
        return False

class LoginWindow:
    def __init__(self):
        self.password_manager = PasswordManager()
        self.setup_login_window()
    
    def setup_login_window(self):
        """Login oynasini sozlash"""
        self.login_window = ctk.CTk()
        self.login_window.title("🔐 Tizimga Kirish")
        self.login_window.geometry("500x600")
        self.login_window.resizable(False, False)
        
        # Oynani markazlashtirish
        self.center_window()
        
        # Oynani yopishni cheklash
        self.login_window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Enter tugmasi uchun
        self.login_window.bind('<Return>', lambda event: self.login_action())
        
        self.create_login_interface()
    
    def center_window(self):
        """Oynani ekran markazida joylash"""
        self.login_window.update_idletasks()
        width = 500
        height = 600
        x = (self.login_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.login_window.winfo_screenheight() // 2) - (height // 2)
        self.login_window.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_login_interface(self):
        """Login interfeysi yaratish"""
        # Asosiy frame
        main_frame = ctk.CTkFrame(self.login_window, corner_radius=20)
        main_frame.pack(expand=True, fill="both", padx=30, pady=30)
        
        # Sarlavha
        title_label = ctk.CTkLabel(
            main_frame, 
            text="🔐 TIZIMGA KIRISH",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#00D4FF"
        )
        title_label.pack(pady=(40, 30))
        
        # Username qismi
        username_label = ctk.CTkLabel(
            main_frame,
            text="👤 Foydalanuvchi:",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FFFFFF"
        )
        username_label.pack(pady=(20, 5))
        
        self.username_entry = ctk.CTkEntry(
            main_frame,
            width=350,
            height=45,
            placeholder_text="Usernameni kiriting...",
            font=ctk.CTkFont(size=14),
            corner_radius=15,
            border_width=2
        )
        self.username_entry.pack(pady=(0, 20))
        
        # Password qismi
        password_label = ctk.CTkLabel(
            main_frame,
            text="🔑 Parol:",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FFFFFF"
        )
        password_label.pack(pady=(0, 5))
        
        self.password_entry = ctk.CTkEntry(
            main_frame,
            width=350,
            height=45,
            placeholder_text="Parolni kiriting...",
            show="*",
            font=ctk.CTkFont(size=14),
            corner_radius=15,
            border_width=2
        )
        self.password_entry.pack(pady=(0, 30))
        
        # Login tugmasi
        login_button = ctk.CTkButton(
            main_frame,
            text="🚀 KIRISH",
            command=self.login_action,
            width=250,
            height=50,
            font=ctk.CTkFont(size=18, weight="bold"),
            corner_radius=25,
            fg_color=("#1f538d", "#14375e"),
            hover_color=("#144870", "#1e5578")
        )
        login_button.pack(pady=(0, 20))
        
        # Parol o'zgartirish tugmasi
        change_password_button = ctk.CTkButton(
            main_frame,
            text="🔧 Parolni O'zgartirish",
            command=self.show_change_password_dialog,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14),
            corner_radius=20,
            fg_color="transparent",
            border_width=2,
            text_color=("#1f538d", "#1e5578"),
            border_color=("#1f538d", "#1e5578"),
            hover_color=("#1f538d", "#1e5578")
        )
        change_password_button.pack(pady=(0, 30))
        
        # Ma'lumot matnlari
        info_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        info_frame.pack(pady=(0, 20))
        
        info_text = "💡 Standart ma'lumotlar:\n👤 Username: IDEAL MOBILE\n🔑 Kirish paroli: 9959\n🔐 Ichki parol: IDEAL_MOBILE+998995999959"
        info_label = ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=ctk.CTkFont(size=12),
            text_color="#888888",
            justify="center"
        )
        info_label.pack()
    
    def login_action(self):
        """Login jarayoni"""
        username_input = self.username_entry.get().strip()
        password_input = self.password_entry.get().strip()
        
        if not username_input or not password_input:
            messagebox.showerror("Xatolik", "Iltimos, barcha maydonlarni to'ldiring!")
            return
        
        config = self.password_manager.load_config()
        
        if (username_input == config["username"] and 
            self.password_manager.verify_login_password(password_input)):
            
            self.login_window.destroy()
            self.open_main_app()
        else:
            messagebox.showerror("Xatolik", "Login yoki parol noto'g'ri! ❌")
            self.password_entry.delete(0, 'end')
    
    def open_main_app(self):
        """Asosiy dasturni ochish"""
        try:
            # dukon.py faylini ochish
            if os.path.exists("dukon.py"):
                subprocess.run([sys.executable, "dukon.py"])
            else:
                # Agar dukon.py yo'q bo'lsa, asosiy oynani ochish
                self.show_main_window()
        except Exception as e:
            messagebox.showerror("Xatolik", f"Dasturni ochishda xatolik: {str(e)}")
            self.show_main_window()
    
    def show_main_window(self):
        """Asosiy oynani ko'rsatish"""
        app_window = ctk.CTk()
        app_window.title("📱 IDEAL MOBILE - Asosiy Oyna")
        app_window.geometry("600x500")
        app_window.resizable(False, False)
        
        # Oynani markazlashtirish
        app_window.update_idletasks()
        width = 600
        height = 500
        x = (app_window.winfo_screenwidth() // 2) - (width // 2)
        y = (app_window.winfo_screenheight() // 2) - (height // 2)
        app_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Asosiy frame
        main_frame = ctk.CTkFrame(app_window, corner_radius=20)
        main_frame.pack(expand=True, fill="both", padx=30, pady=30)
        
        # Sarlavha
        title_label = ctk.CTkLabel(
            main_frame,
            text="📱 IDEAL MOBILE",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#00D4FF"
        )
        title_label.pack(pady=(40, 30))
        
        # Xush kelibsiz matni
        welcome_label = ctk.CTkLabel(
            main_frame,
            text="✅ Tizimga muvaffaqiyatli kirildi!",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#4CAF50"
        )
        welcome_label.pack(pady=(0, 30))
        
        # Kodlar frame
        codes_frame = ctk.CTkFrame(main_frame, corner_radius=15)
        codes_frame.pack(pady=(0, 20), padx=20, fill="x")
        
        codes_title = ctk.CTkLabel(
            codes_frame,
            text="🔍 Ichki Kodlar",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        codes_title.pack(pady=(20, 10))
        
        def show_internal_codes():
            """Ichki kodlarni ko'rsatish"""
            # Ichki parolni so'rash
            internal_dialog = ctk.CTkToplevel(app_window)
            internal_dialog.title("🔐 Ichki Parol")
            internal_dialog.geometry("400x250")
            internal_dialog.resizable(False, False)
            internal_dialog.transient(app_window)
            internal_dialog.grab_set()
            
            # Markazlashtirish
            internal_dialog.update_idletasks()
            x = (internal_dialog.winfo_screenwidth() // 2) - (200)
            y = (internal_dialog.winfo_screenheight() // 2) - (125)
            internal_dialog.geometry(f"400x250+{x}+{y}")
            
            dialog_frame = ctk.CTkFrame(internal_dialog, corner_radius=15)
            dialog_frame.pack(expand=True, fill="both", padx=20, pady=20)
            
            title = ctk.CTkLabel(
                dialog_frame,
                text="🔐 ICHKI PAROL KIRITING",
                font=ctk.CTkFont(size=16, weight="bold")
            )
            title.pack(pady=(30, 20))
            
            internal_entry = ctk.CTkEntry(
                dialog_frame,
                width=250,
                height=40,
                placeholder_text="Ichki parolni kiriting...",
                show="*",
                corner_radius=10
            )
            internal_entry.pack(pady=(0, 20))
            
            def verify_internal():
                internal_pwd = internal_entry.get().strip()
                if self.password_manager.verify_internal_password(internal_pwd):
                    internal_dialog.destroy()
                    self.show_codes_window(app_window)
                else:
                    messagebox.showerror("Xatolik", "Ichki parol noto'g'ri!")
                    internal_entry.delete(0, 'end')
            
            verify_btn = ctk.CTkButton(
                dialog_frame,
                text="✅ Tasdiqlash",
                command=verify_internal,
                width=150,
                height=35,
                corner_radius=10
            )
            verify_btn.pack()
            
            internal_dialog.bind('<Return>', lambda event: verify_internal())
            internal_entry.focus()
        
        codes_button = ctk.CTkButton(
            codes_frame,
            text="🔍 Kodlarni Ko'rish",
            command=show_internal_codes,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=15
        )
        codes_button.pack(pady=(0, 20))
        
        # Chiqish tugmasi
        exit_button = ctk.CTkButton(
            main_frame,
            text="🚪 Chiqish",
            command=app_window.destroy,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=15,
            fg_color="#d32f2f",
            hover_color="#b71c1c"
        )
        exit_button.pack(pady=(30, 50))
        
        app_window.mainloop()
    
    def show_codes_window(self, parent):
        """Kodlar oynasini ko'rsatish"""
        codes_window = ctk.CTkToplevel(parent)
        codes_window.title("🔍 Ichki Kodlar")
        codes_window.geometry("500x400")
        codes_window.resizable(False, False)
        codes_window.transient(parent)
        codes_window.grab_set()
        
        # Markazlashtirish
        codes_window.update_idletasks()
        x = (codes_window.winfo_screenwidth() // 2) - (250)
        y = (codes_window.winfo_screenheight() // 2) - (200)
        codes_window.geometry(f"500x400+{x}+{y}")
        
        main_frame = ctk.CTkFrame(codes_window, corner_radius=15)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Sarlavha
        title = ctk.CTkLabel(
            main_frame,
            text="🔍 ICHKI KODLAR",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#00D4FF"
        )
        title.pack(pady=(30, 20))
        
        # Kodlarni yuklash va ko'rsatish
        codes = self.password_manager.load_internal_codes()
        
        codes_frame = ctk.CTkScrollableFrame(main_frame, height=200)
        codes_frame.pack(pady=(0, 20), padx=20, fill="both", expand=True)
        
        for username, code in codes.items():
            code_item = ctk.CTkFrame(codes_frame)
            code_item.pack(fill="x", pady=5)
            
            ctk.CTkLabel(
                code_item,
                text=f"👤 {username}: {code}",
                font=ctk.CTkFont(size=14),
                anchor="w"
            ).pack(pady=10, padx=20, fill="x")
        
        # Yopish tugmasi
        close_button = ctk.CTkButton(
            main_frame,
            text="❌ Yopish",
            command=codes_window.destroy,
            width=120,
            height=40,
            corner_radius=10,
            fg_color="#666666"
        )
        close_button.pack(pady=(0, 20))
    
    def show_change_password_dialog(self):
        """Parol o'zgartirish oynasini ko'rsatish"""
        change_window = ctk.CTkToplevel(self.login_window)
        change_window.title("🔧 Parolni O'zgartirish")
        change_window.geometry("450x400")
        change_window.resizable(False, False)
        change_window.transient(self.login_window)
        change_window.grab_set()
        
        # Oynani markazlashtirish
        change_window.update_idletasks()
        x = (change_window.winfo_screenwidth() // 2) - (225)
        y = (change_window.winfo_screenheight() // 2) - (200)
        change_window.geometry(f"450x400+{x}+{y}")
        
        # Frame
        main_frame = ctk.CTkFrame(change_window, corner_radius=15)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Sarlavha
        title = ctk.CTkLabel(
            main_frame,
            text="🔧 PAROLNI O'ZGARTIRISH",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#00D4FF"
        )
        title.pack(pady=(20, 30))
        
        # Ichki parol (kodda saqlangan parol)
        current_label = ctk.CTkLabel(
            main_frame,
            text="🔐 Ichki parol (kodda saqlangan):",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        current_label.pack(pady=(0, 5))
        
        current_entry = ctk.CTkEntry(
            main_frame,
            width=300,
            height=40,
            placeholder_text="Ichki parolni kiriting...",
            show="*",
            corner_radius=10
        )
        current_entry.pack(pady=(0, 20))
        
        # Yangi parol
        new_label = ctk.CTkLabel(
            main_frame,
            text="🆕 Yangi parol:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        new_label.pack(pady=(0, 5))
        
        new_entry = ctk.CTkEntry(
            main_frame,
            width=300,
            height=40,
            placeholder_text="Yangi parolni kiriting...",
            show="*",
            corner_radius=10
        )
        new_entry.pack(pady=(0, 30))
        
        # Tugmalar frame
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(pady=(0, 20))
        
        def change_password():
            current_pwd = current_entry.get().strip()
            new_pwd = new_entry.get().strip()
            
            if not current_pwd or not new_pwd:
                messagebox.showerror("Xatolik", "Barcha maydonlarni to'ldiring!")
                return
            
            if len(new_pwd) < 4:
                messagebox.showerror("Xatolik", "Yangi parol kamida 4 ta belgi bo'lishi kerak!")
                return
            
            # ICHKI PAROLNI TEKSHIRISH (kodda saqlangan parol)
            if self.password_manager.verify_internal_password(current_pwd):
                config = self.password_manager.load_config()
                config["login_password"] = self.password_manager.hash_password(new_pwd)
                self.password_manager.save_config(config)
                messagebox.showinfo("Muvaffaqiyat", "Kirish paroli muvaffaqiyatli o'zgartirildi! 🎉")
                change_window.destroy()
            else:
                messagebox.showerror("Xatolik", "Ichki parol noto'g'ri!")
                current_entry.delete(0, 'end')
        
        # O'zgartirish tugmasi
        change_btn = ctk.CTkButton(
            buttons_frame,
            text="✅ O'zgartirish",
            command=change_password,
            width=120,
            height=35,
            corner_radius=10,
            fg_color="#1f538d"
        )
        change_btn.pack(side="left", padx=(0, 10))
        
        # Bekor qilish tugmasi
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="❌ Bekor qilish",
            command=change_window.destroy,
            width=120,
            height=35,
            corner_radius=10,
            fg_color="#666666"
        )
        cancel_btn.pack(side="left")
        
        # Enter tugmasi
        change_window.bind('<Return>', lambda event: change_password())
        current_entry.focus()
    
    def on_closing(self):
        """Oynani yopish"""
        if messagebox.askokcancel("Chiqish", "Dasturdan chiqishni xohlaysizmi? 🤔"):
            self.login_window.destroy()
            sys.exit()

    def run(self):
        """Dasturni ishga tushirish"""
        self.login_window.mainloop()

# Dasturni ishga tushirish
if __name__ == "__main__":
    app = LoginWindow()
    app.run()