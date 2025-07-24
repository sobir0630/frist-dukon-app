import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import re
from datetime import datetime

phones = []


# CustomTkinter sozlamalari
ctk.set_appearance_mode("light")  # "light" yoki "dark"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"


def search_phone_by_imei():
    """IMEI raqamning oxirgi 4 ta raqami orqali telefonni qidirish - CustomTkinter versiyasi"""

    # Asosiy oyna
    search_window = ctk.CTkToplevel()
    search_window.title("📱 Telefon Qidirish - IMEI")
    search_window.geometry("700x600")
    search_window.resizable(True, True)

    # Oynani markazlashtirish
    search_window.update_idletasks()
    x = (search_window.winfo_screenwidth() // 2) - (700 // 2)
    y = (search_window.winfo_screenheight() // 2) - (600 // 2)
    search_window.geometry(f"700x600+{x}+{y}")

    # Asosiy frame
    main_frame = ctk.CTkFrame(search_window, corner_radius=0, fg_color="transparent")
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Sarlavha
    title_frame = ctk.CTkFrame(main_frame, height=80, corner_radius=15)
    title_frame.pack(fill="x", pady=(0, 20))
    title_frame.pack_propagate(False)

    title_label = ctk.CTkLabel(
        title_frame,
        text="📱 IMEI bo'yicha telefon qidirish",
        font=ctk.CTkFont(size=24, weight="bold")
    )
    title_label.pack(expand=True)

    # Qidiruv paneli
    search_frame = ctk.CTkFrame(main_frame, height=100, corner_radius=15)
    search_frame.pack(fill="x", pady=(0, 20))
    search_frame.pack_propagate(False)

    # Qidiruv elementi
    search_container = ctk.CTkFrame(search_frame, fg_color="transparent")
    search_container.pack(expand=True, padx=20, pady=20)

    search_label = ctk.CTkLabel(
        search_container,
        text="IMEI oxirgi 4 raqami:",
        font=ctk.CTkFont(size=16, weight="bold")
    )
    search_label.pack(pady=(0, 10))

    # Qidiruv input va tugma
    input_frame = ctk.CTkFrame(search_container, fg_color="transparent")
    input_frame.pack()

    search_entry = ctk.CTkEntry(
        input_frame,
        placeholder_text="Masalan: 1234",
        width=250,
        height=20,
        font=ctk.CTkFont(size=16),
        corner_radius=5
    )
    search_entry.pack(side="left", padx=(0, 15))
    search_entry.focus()

    # Qidiruv tugmasi
    search_btn = ctk.CTkButton(
        input_frame,
        text="🔍 Qidirish",
        width=120,
        height=80,
        font=ctk.CTkFont(size=14, weight="bold"),
        corner_radius=5,
        command=lambda: perform_search()
    )
    search_btn.pack(side="left")

    # Natijalar paneli
    results_frame = ctk.CTkFrame(main_frame, corner_radius=15)
    results_frame.pack(fill="both", expand=True, pady=(0, 20))

    # Scrollable frame
    scrollable_frame = ctk.CTkScrollableFrame(
        results_frame,
        corner_radius=10,
        scrollbar_button_color=("gray70", "gray30"),
        scrollbar_button_hover_color=("gray60", "gray40")
    )
    scrollable_frame.pack(fill="both", expand=True, padx=15, pady=15)

    # Dastlabki xabar
    initial_message = ctk.CTkLabel(
        scrollable_frame,
        text="💡 IMEI raqamining oxirgi 4 ta raqamini kiriting va qidiring",
        font=ctk.CTkFont(size=16),
        text_color=("gray50", "gray60")
    )
    initial_message.pack(pady=50)

    def clear_results():
        """Natijalar panelini tozalash"""
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

    def create_phone_card(phone_data, status, index):
        """Telefon kartasini yaratish"""
        # Asosiy karta
        card_frame = ctk.CTkFrame(scrollable_frame, corner_radius=12, height=230)
        card_frame.pack(fill="x", pady=8, padx=5)
        card_frame.pack_propagate(False)

        # Karta ichidagi asosiy container
        card_container = ctk.CTkFrame(card_frame, fg_color="transparent")
        card_container.pack(fill="both", expand=True, padx=15, pady=15)

        # Yuqori qism - nomi va holati
        top_frame = ctk.CTkFrame(card_container, fg_color="transparent", height=40)
        top_frame.pack(fill="x", pady=(0, 10))
        top_frame.pack_propagate(False)

        # Telefon nomi
        name_label = ctk.CTkLabel(
            top_frame,
            text=f"📱 {phone_data['nomi']}",
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w"
        )
        name_label.pack(side="left", fill="x", expand=True)

        # Status badge
        if status == "active":
            status_text = "✅ Mavjud"
            status_color = ("green", "green")
        elif status == "sold":
            status_text = "💰 Sotilgan"
            status_color = ("orange", "orange")
        elif status == "deleted":
            status_text = "❌ Uchirilgan"
            status_color = ("red", "red")

        status_badge = ctk.CTkLabel(
            top_frame,
            text=status_text,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=status_color,
            corner_radius=15,
            width=80,
            height=30
        )
        status_badge.pack(side="right")

        # O'rta qism - ma'lumotlar
        info_frame = ctk.CTkFrame(card_container, fg_color="transparent")
        info_frame.pack(fill="x", pady=(0, 10))

        # IMEI
        imei_label = ctk.CTkLabel(
            info_frame,
            text=f"🔢 IMEI: {phone_data['modeli']}",
            font=ctk.CTkFont(size=14),
            anchor="w"
        )
        imei_label.pack(fill="x", pady=2)

        # Narx
        if status == "active":
            price_text = f"💰 Narx: {phone_data.get('narx', 'Nomalum')}"
        else:
            # Avval asl_narx, keyin narx, ikkalasi ham bo‘lmasa "Noma'lum"
            asl_narx = phone_data.get('asl_narx') or phone_data.get('narx', "Noma'lum")
            price_text = f"💰 Asl narx: {asl_narx}"
            if 'sotish_narx' in phone_data:
                price_text += f" → Sotish: {phone_data['sotish_narx']}"

        price_label = ctk.CTkLabel(
            info_frame,
            text=price_text,
            font=ctk.CTkFont(size=34),
            anchor="w"
        )
        price_label.pack(fill="x", pady=5)

        # Sana
        date_text = "📅 Qo'shilgan: " if status == "active" else "📅 Sotilgan: "
        date_field = phone_data.get('sana', phone_data.get('sotilgan_sana', 'Noma\'lum'))

        date_label = ctk.CTkLabel(
            info_frame,
            text=f"{date_text}{date_field}",
            font=ctk.CTkFont(size=14),
            anchor="w"
        )
        date_label.pack(fill="x", pady=2)

        # Mijoz ma'lumotlari (sotilganlar uchun)
        if status == "sold" and 'mijoz_ismi' in phone_data:
            customer_label = ctk.CTkLabel(
                info_frame,
                text=f"👤 Mijoz: {phone_data['mijoz_ismi']} - {phone_data.get('mijoz_telefon', '')}",
                font=ctk.CTkFont(size=14),
                anchor="w"
            )
            customer_label.pack(fill="x", pady=2)

        # Pastki qism - tugmalar
        if status == "active":
            action_frame = ctk.CTkFrame(card_container, fg_color="transparent", height=40)
            action_frame.pack(fill="x")
            action_frame.pack_propagate(False)

            # Sotish tugmasi
            sell_btn = ctk.CTkButton(
                action_frame,
                text="💰 Sotish",
                width=100,
                height=35,
                font=ctk.CTkFont(size=14, weight="bold"),
                fg_color=("green", "green"),
                hover_color=("darkgreen", "darkgreen"),
                corner_radius=8,
                command=lambda: sell_phone_action(phone_data)
            )
            sell_btn.pack(side="right")

            # Tahrirlash tugmasi
            edit_btn = ctk.CTkButton(
                action_frame,
                text="✏️ Tahrirlash",
                width=100,
                height=35,
                font=ctk.CTkFont(size=14, weight="bold"),
                fg_color=("blue", "blue"),
                hover_color=("darkblue", "darkblue"),
                corner_radius=8,
                command=lambda: edit_phone_action(phone_data)
            )
            edit_btn.pack(side="right", padx=(0, 10))

    def sell_phone_action(phone_data):
        """Telefonni sotish action"""
        
        # Mijoz ma'lumotlarini olish dialogini chaqirish va yopilishini kutish
        dialog = CustomerDialog(search_window, phone_data)
        search_window.wait_window(dialog.dialog)
                
        if dialog.result:
            try:
                # 1. telefon_data.json dan telefonni topish
                with open("telefon_data.json", "r", encoding="utf-8") as f:
                    phones = json.load(f)
                # model yoki index bo‘yicha topamiz
                for phone in phones:
                    if phone.get("index") == phone_data.get("index"):
                        # 2. sotilgan formatga o‘tkazish
                        sale_record = {
                            "nomi": phone.get("nomi"),
                            "modeli": phone.get("modeli"),
                            "asl_narx": phone.get("narx"),
                            "sotish_narx": f"${dialog.result.get('sell_price'):.2f}",
                            "foyda": f"${dialog.result.get('profit'):.2f}",
                            "sotilgan_sana": datetime.now().strftime("%d/%m/%Y %H:%M"),
                            "mijoz_ismi": dialog.result.get("customer_name"),
                            "mijoz_telefon": dialog.result.get("customer_phone")
                        }
                        break
                else:
                    # Telefon topilmasa
                    raise Exception("Telefon topilmadi!")

                # 3. sotish_file.json ga qo‘shish
                try:
                    with open("sotish_file.json", "r", encoding="utf-8") as f:
                        sold_phones = json.load(f)
                except (FileNotFoundError, json.JSONDecodeError):
                    sold_phones = []
                sold_phones.append(sale_record)
                with open("sotish_file.json", "w", encoding="utf-8") as f:
                    json.dump(sold_phones, f, ensure_ascii=False, indent=4)

                # 4. telefon_data.json dan o‘chirish
                phones = [p for p in phones if p.get("index") != phone_data.get("index")]
                with open("telefon_data.json", "w", encoding="utf-8") as f:
                    json.dump(phones, f, ensure_ascii=False, indent=4)
            
            # Muvaffaqiyat dialog oynasini yaratish
                success_dialog = ctk.CTkToplevel(search_window)
                success_dialog.title("Muvaffaqiyat")
                success_dialog.geometry("400x200")
                success_dialog.transient(search_window)
                success_dialog.grab_set()

                # Dialog oynasini markazlashtirish
                success_dialog.update_idletasks()
                x = search_window.winfo_x() + (search_window.winfo_width() // 2) - 200
                y = search_window.winfo_y() + (search_window.winfo_height() // 2) - 100
                success_dialog.geometry(f"400x200+{x}+{y}")

                success_label = ctk.CTkLabel(
                    success_dialog,
                    text=f"✅ {phone_data['nomi']} muvaffaqiyatli sotildi!\n\n💰 Foyda: ${dialog.result['profit']:.2f}",
                    font=ctk.CTkFont(size=16, weight="bold")
                )
                success_label.pack(expand=True)

                ok_btn = ctk.CTkButton(
                    success_dialog,
                    text="OK",
                    command=success_dialog.destroy
                )
                ok_btn.pack(pady=10)

                # Qidiruv natijalarini yangilash
                perform_search()

            except Exception as e:
                import traceback
                traceback.print_exc()
                messagebox.showerror("Xatolik", f"Sotishda xatolik yuz berdi: {str(e)}")
                    


    def edit_phone_action(phone_data):
        """Telefonni tahrirlash action"""
        global phones


        edit_window = ctk.CTkToplevel()
        edit_window.state("zoomed")
        edit_window.title("Telefonni tahrirlash")
        edit_window.grab_set()

        # Nomi
        ctk.CTkLabel(edit_window, text="Telefon nomi:").pack(pady=(10, 2))
        name_entry = ctk.CTkEntry(edit_window)
        name_entry.insert(0, phone_data.get("nomi", ""))
        name_entry.pack()

        # Modeli
        ctk.CTkLabel(edit_window, text="Modeli:").pack(pady=(10, 2))
        model_entry = ctk.CTkEntry(edit_window)
        model_entry.insert(0, phone_data.get("modeli", ""))
        model_entry.pack()

        # Narxi
        ctk.CTkLabel(edit_window, text="Turi:").pack(pady=(10, 2))
        tip_entry = ctk.CTkEntry(edit_window)
        tip_entry.insert(0, phone_data.get("turi", ""))
        tip_entry.pack()

        # Qo‘shilgan sana
        ctk.CTkLabel(edit_window, text="Narxi:").pack(pady=(10, 2))
        price_entry = ctk.CTkEntry(edit_window)
        price_entry.insert(0, phone_data.get("narx", ""))
        price_entry.pack()
        
        # sanasi
        ctk.CTkLabel(edit_window, text="Narxi:").pack(pady=(10, 2))
        today_entry = ctk.CTkEntry(edit_window)
        today_entry.insert(0, phone_data.get("sana", ""))
        today_entry.pack()

        # holati
        ctk.CTkLabel(edit_window, text="Holati:").pack(pady=(10, 2))
        status_entry = ctk.CTkEntry(edit_window)
        status_entry.insert(0, phone_data.get("holat", ""))
        status_entry.pack()
        
        # qushilgan sana
        ctk.CTkLabel(edit_window, text="Qushilgan sana:").pack(pady=(10, 2))
        choked_entry = ctk.CTkEntry(edit_window)
        choked_entry.insert(0, phone_data.get("qoshilgan_sana", ""))
        choked_entry.pack()

        def save_changes():
            updated_data = {
                "index": phone_data.get("index"),
                "nomi": name_entry.get(),
                "modeli": model_entry.get(),
                "turi": tip_entry.get(),
                "narx": price_entry.get(),
                "sana": today_entry.get(),
                "holat": status_entry.get(),
                "qoshilgan_sana": choked_entry.get()
            }
            try:
                # Barcha telefonlarni o'qish
                with open("telefon_data.json", "r", encoding="utf-8") as file:
                    phones = json.load(file)
                # Yangilash
                for i, phone in enumerate(phones):
                    if phone.get("index") == updated_data["index"]:
                        phones[i] = updated_data
                        break
                # Qayta yozish
                with open("telefon_data.json", "w", encoding="utf-8") as file:
                    json.dump(phones, file, ensure_ascii=False, indent=4)
                print("✅ Ma'lumotlar telefon_data.json fayliga saqlandi.")
            except Exception as e:
                print("❌ Xatolik yuz berdi:", e)
            edit_window.destroy()
        
        # enter bosib saqlash
        edit_window.bind('<Return>', lambda event: save_changes())
        # Saqlash tugmasi
        ctk.CTkButton(edit_window, text="Saqlash", command=save_changes).pack(pady=5)

                    

    def perform_search():
        """Qidirish funksiyasi"""
        search_text = search_entry.get().strip()

        if not search_text:
            clear_results()
            no_input_label = ctk.CTkLabel(
                scrollable_frame,
                text="⚠️ Iltimos, IMEI raqamining oxirgi 4 ta raqamini kiriting",
                font=ctk.CTkFont(size=16),
                text_color=("orange", "orange")
            )
            no_input_label.pack(pady=50)
            return

        # Faqat raqamlarni qoldirish
        search_text = ''.join(filter(str.isdigit, search_text))

        if len(search_text) != 4:
            if len(search_text) > 4:
                search_text = search_text[-4:]
                search_entry.delete(0, tk.END)
                search_entry.insert(0, search_text)
            else:
                clear_results()
                invalid_label = ctk.CTkLabel(
                    scrollable_frame,
                    text="⚠️ IMEI raqami 4 ta raqamdan iborat bo'lishi kerak",
                    font=ctk.CTkFont(size=16),
                    text_color=("orange", "orange")
                )
                invalid_label.pack(pady=50)
                return

        clear_results()

        # Qidiruv jarayoni
        loading_label = ctk.CTkLabel(
            scrollable_frame,
            text="🔍 Qidirilmoqda...",
            font=ctk.CTkFont(size=16),
            text_color=("blue", "blue")
        )
        loading_label.pack(pady=50)

        # Update oynasi
        search_window.update()

        # Qidiruv natijalarini simulation qilish
        # Bu yerda siz o'zingizning phones va sold_phones ro'yxatlaringizni ishlatishingiz kerak
        found_phones = []
        # Telefonlar ro'yxatini fayldan o'qish
        try:
            with open("telefon_data.json", "r", encoding="utf-8") as f:
                sample_phones = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            sample_phones = []
        try:
            with open("sotish_file.json", "r", encoding="utf-8") as f2:
                sample_sold_phones = json.load(f2)
        except (FileNotFoundError, json.JSONDecodeError):
            sample_sold_phones = []
        try:
            with open("deleted_phones.json", "r", encoding="utf-8") as f2:
                deleted_phones = json.load(f2)
        except (FileNotFoundError, json.JSONDecodeError):
            deleted_phones = []

        # Faol telefonlar ichidan qidirish
        for phone in sample_phones:
            if phone["modeli"][-4:] == search_text:
                found_phones.append((phone, "active"))

        # Sotilgan telefonlar ichidan qidirish
        for phone in sample_sold_phones:
            if phone["modeli"][-4:] == search_text:
                found_phones.append((phone, "sold"))
        # uchirilgan telefonlar icidan qidirish
        
        for phone in deleted_phones:
            if phone["modeli"][-4:] == search_text:
                found_phones.append((phone, "deleted"))

        # Loading ni olib tashlash
        loading_label.destroy()

        if not found_phones:
            no_results_label = ctk.CTkLabel(
                scrollable_frame,
                text=f"❌ '{search_text}' IMEI bilan telefon topilmadi",
                font=ctk.CTkFont(size=16),
                text_color=("red", "red")
            )
            no_results_label.pack(pady=50)
            return

        # Natijalar sarlavhasi
        results_header = ctk.CTkLabel(
            scrollable_frame,
            text=f"📋 {len(found_phones)} ta natija topildi:",
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w"
        )
        results_header.pack(fill="x", pady=(10, 20))

        # Natijalarni ko'rsatish
        for i, (phone, status) in enumerate(found_phones):
            create_phone_card(phone, status, i)
            
            
            
            
            
            

    # Enter tugmasi uchun
    search_entry.bind("<Return>", lambda event: perform_search())

    # Pastki tugmalar
    bottom_frame = ctk.CTkFrame(main_frame, height=60, corner_radius=15)
    bottom_frame.pack(fill="x")
    bottom_frame.pack_propagate(False)

    button_container = ctk.CTkFrame(bottom_frame, fg_color="transparent")
    button_container.pack(expand=True, padx=20, pady=15)

    def reset_search():
        try:
            search_entry.delete(0, tk.END)
        except Exception as e:
            print("search_entry xatosi:", e)

        try:
            clear_results()
        except Exception as e:
            print("clear_results xatosi:", e)

        try:
            initial_message.pack(pady=50)
        except Exception as e:
            print("initial_message xatosi:", e)

    # Tugma
    clear_btn = ctk.CTkButton(
        button_container,
        text="🧹 Tozalash",
        width=120,
        height=35,
        font=ctk.CTkFont(size=14, weight="bold"),
        fg_color=("gray", "gray"),
        hover_color=("darkgray", "darkgray"),
        command=reset_search  # <-- lambda emas, to‘g‘ridan-to‘g‘ri funksiya
    )
    clear_btn.pack(side="left")



    # Yopish tugmasi
    close_btn = ctk.CTkButton(
        button_container,
        text="❌ Yopish",
        width=120,
        height=35,
        font=ctk.CTkFont(size=14, weight="bold"),
        fg_color=("red", "red"),
        hover_color=("darkred", "darkred"),
        command=search_window.destroy
    )
    close_btn.pack(side="right")


class CustomerDialog:
    """Mijoz ma'lumotlarini olish uchun dialog"""

    def __init__(self, parent, phone_data):
        self.result = None
        self.phone_data = phone_data

        # Dialog oynasi
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Mijoz Ma'lumotlari")
        self.dialog.geometry("500x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Markazlashtirish
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - 250
        y = parent.winfo_y() + (parent.winfo_height() // 2) - 200
        self.dialog.geometry(f"500x500+{x}+{y}")

        self.setup_ui()

    def setup_ui(self):
        # Asosiy frame
        main_frame = ctk.CTkFrame(self.dialog, corner_radius=0, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Sarlavha
        title_label = ctk.CTkLabel(
            main_frame,
            text=f"📱 {self.phone_data['nomi']} - Sotish",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(0, 20))

        # Form
        form_frame = ctk.CTkFrame(main_frame, corner_radius=15)
        form_frame.pack(fill="both", expand=True, pady=(0, 20))

        form_container = ctk.CTkFrame(form_frame, fg_color="transparent")
        form_container.pack(fill="both", expand=True, padx=100, pady=10)

        # Mijoz ismi
        ctk.CTkLabel(form_container, text="👤 Mijoz ismi:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w",
                                                                                                          pady=(0, 5))
        self.name_entry = ctk.CTkEntry(form_container, placeholder_text="Mijoz ismini kiriting", height=40)
        self.name_entry.pack(fill="x", pady=(0, 15))
        self.name_entry.focus()

        # Mijoz telefoni
        ctk.CTkLabel(form_container, text="📞 Mijoz telefoni:", font=ctk.CTkFont(size=14, weight="bold")).pack(
            anchor="w", pady=(0, 5))
        self.phone_entry = ctk.CTkEntry(form_container, placeholder_text="+998901234567", height=40)
        self.phone_entry.pack(fill="x", pady=(0, 15))

        # Sotish narxi
        ctk.CTkLabel(form_container, text="💰 Sotish narxi:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w",
                                                                                                            pady=(0, 5))
        self.price_entry = ctk.CTkEntry(form_container, placeholder_text="1000", height=40)
        self.price_entry.pack(fill="x", pady=(0, 10))

        # Asl narx ko'rsatish
        original_price = re.sub(r"[^\d.]", "", str(self.phone_data['narx']))
        price_info = ctk.CTkLabel(
            form_container,
            text=f"📊 Asl narx: {self.phone_data['narx']}",
            font=ctk.CTkFont(size=12),
            text_color=("gray", "gray")
        )
        price_info.pack(anchor="w", pady=(0, 15))

        # Tugmalar
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent", height=50)
        button_frame.pack(fill="x")
        button_frame.pack_propagate(False)

        # Bekor qilish
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="❌ Bekor qilish",
            width=120,
            height=40,
            fg_color=("gray", "gray"),
            hover_color=("darkgray", "darkgray"),
            command=self.cancel
        )
        cancel_btn.pack(side="left")

        # Tasdiqlash
        confirm_btn = ctk.CTkButton(
            button_frame,
            text="✅ Tasdiqlash",
            width=120,
            height=40,
            fg_color=("green", "green"),
            hover_color=("darkgreen", "darkgreen"),
            command=self.confirm
        )
        confirm_btn.pack(side="right")

    def cancel(self):
        self.dialog.destroy()

    def confirm(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        price_str = self.price_entry.get().strip()

        if not name:
            messagebox.showerror("Xatolik", "Mijoz ismini kiriting!", parent=self.dialog)
            return

        if not phone:
            messagebox.showerror("Xatolik", "Mijoz telefon raqamini kiriting!", parent=self.dialog)
            return

        if not price_str:
            messagebox.showerror("Xatolik", "Sotish narxini kiriting!", parent=self.dialog)
            return

        try:
            # 1. Narxdagi belgilarni tozalash
            clean_price_str = price_str.replace("$", "").replace(",", "").strip()
            sell_price = float(clean_price_str)
            original_price = float(re.sub(r"[^\d.]", "", str(self.phone_data['narx'])))
            profit = sell_price - original_price

            self.result = {
                'customer_name': name,
                'customer_phone': phone,
                'sell_price': sell_price,
                'profit': profit
            }

            self.dialog.destroy()

        except ValueError:
            messagebox.showerror("Xatolik", "Noto'g'ri narx kiritildi!", parent=self.dialog)
    

# Test uchun
if __name__ == "__main__":
    root = ctk.CTk()
    root.withdraw()  # asosiy oynani yashirish
    search_phone_by_imei()
    root.mainloop()


