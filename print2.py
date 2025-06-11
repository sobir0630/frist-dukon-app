import customtkinter as ctk
from tkinter import messagebox, filedialog
import tkinter as tk
from PIL import Image, ImageDraw, ImageFont
import io
import os
from datetime import datetime
import tempfile
import platform
import subprocess

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class IMEIBarcodeGenerator:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("IMEI Shtrix Kod Generator")
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0")
        # self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))


        self.barcode_image = None
        self.setup_ui()

    def setup_ui(self):
        main_container = ctk.CTkFrame(self.root, corner_radius=15)
        main_container.pack(pady=20, padx=20, fill="both", expand=True)

        title_label = ctk.CTkLabel(
            main_container,
            text="\ud83d\udcf1 IMEI SHTRIX KOD GENERATOR \ud83d\udcca",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#00D4FF"
        )
        title_label.pack(pady=10)

        content_frame = ctk.CTkFrame(main_container, corner_radius=10)
        content_frame.pack(pady=10, padx=20, fill="both", expand=True)

        left_frame = ctk.CTkFrame(content_frame, corner_radius=10, width=400)
        left_frame.pack(side="left", fill="y", padx=10, pady=10)
        left_frame.pack_propagate(False)

        right_frame = ctk.CTkFrame(content_frame, corner_radius=10)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.setup_input_section(left_frame)
        self.setup_display_section(right_frame)

    def setup_input_section(self, parent):
        ctk.CTkLabel(parent, text="IMEI Raqamini Kiriting:").pack(pady=(20, 5))
        self.imei_entry = ctk.CTkEntry(parent, width=350, height=40, placeholder_text="15 ta raqam kritng")
        self.imei_entry.pack()

        ctk.CTkLabel(parent, text="Telefon Modeli:").pack(pady=(20, 5))
        self.model_entry = ctk.CTkEntry(parent, width=350, height=40, placeholder_text="Masalan: iPhone 15 Pro")
        self.model_entry.pack()

        ctk.CTkLabel(parent, text="Narxi (ixtiyoriy):").pack(pady=(20, 5))
        self.price_entry = ctk.CTkEntry(parent, width=350, height=40)
        self.price_entry.pack()

        self.verified_checkbox = ctk.CTkCheckBox(parent, text="UZ EMAidan o'tgan")
        self.verified_checkbox.pack(pady=10)

        ctk.CTkButton(parent, text="\ud83c\udf1f Shtrix Kod Yaratish", command=self.generate_barcode,
                      fg_color="#00C851", hover_color="#009933",
                      font=ctk.CTkFont(size=16, weight="bold"), width=350, height=45).pack(pady=20)

        self.save_btn = ctk.CTkButton(parent, text="\ud83d\udcc2 Saqlash", command=self.save_barcode,
                                      fg_color="#FFD700", hover_color="#E5C100",
                                      font=ctk.CTkFont(size=14, weight="bold"), width=350, height=40, state="disabled")
        self.save_btn.pack(pady=5)

        self.print_btn = ctk.CTkButton(parent, text="\ud83d\uddb6\ufe0f Chop etish", command=self.print_barcode,
                                       fg_color="#4285F4", hover_color="#3367D6",
                                       font=ctk.CTkFont(size=14, weight="bold"), width=350, height=40, state="disabled")
        self.print_btn.pack(pady=5)

        ctk.CTkButton(parent, text="\u274c Tozalash", command=self.clear_all,
                      fg_color="#FF4444", hover_color="#CC0000",
                      font=ctk.CTkFont(size=14, weight="bold"), width=350, height=40).pack(pady=10)

    def setup_display_section(self, parent):
        self.display_frame = ctk.CTkFrame(parent, corner_radius=15, fg_color="white")
        self.display_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.initial_label = ctk.CTkLabel(
            self.display_frame,
            text="\ud83d\udd0d IMEI raqamini kiriting va\n'SHTRIX KOD YARATISH' tugmasini bosing",
            font=ctk.CTkFont(size=16),
            text_color="#666666"
        )
        self.initial_label.pack(expand=True)

    def generate_barcode(self):
        imei = self.imei_entry.get().strip()
        model = self.model_entry.get().strip()
        price = self.price_entry.get().strip()
        is_verified = self.verified_checkbox.get() == 1

        if not imei.isdigit() or len(imei) != 15:
            messagebox.showerror("Xato", "IMEI 15 xonali raqam bo'lishi kerak")
            return

        self.barcode_image = self.create_barcode_image(imei, model, is_verified, price)
        self.display_barcode()
        self.save_btn.configure(state="normal")
        self.print_btn.configure(state="normal")

    def create_barcode_image(self, imei, phone_model="", is_verified=False, price=""):
        pattern = "11010000100" + ''.join(["11001100110" if c == '2' else "11011001100" for c in imei]) + "1100011101011"
        width = 500
        height = 300
        bar_width = 2

        img = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(img)

        try:
            font_path = "arial.ttf"
            title_font = ImageFont.truetype(font_path, 24)
            small_font = ImageFont.truetype(font_path, 18)
            imei_font = ImageFont.truetype(font_path, 20)
            price_font = ImageFont.truetype(font_path, 18)
        except:
            title_font = small_font = imei_font = price_font = ImageFont.load_default()

        y_cursor = 10
        date_str = datetime.now().strftime("%d.%m.%Y")
        draw.text((10, y_cursor), date_str, fill='gray', font=small_font)
        y_cursor += 30

        if phone_model:
            model_x = (width - draw.textlength(phone_model, font=title_font)) // 2
            draw.text((model_x, y_cursor), phone_model, fill='black', font=title_font)
            y_cursor += 35

        if is_verified:
            verified_text = "UZ IMAI dan o'tgan"
            verified_x = (width - draw.textlength(verified_text, font=small_font)) // 2
            draw.text((verified_x, y_cursor), verified_text, fill='green', font=small_font)
            y_cursor += 30

        x = 50
        for bit in pattern:
            if bit == '1':
                draw.rectangle([x, y_cursor, x + bar_width, y_cursor + 80], fill='black')
            x += bar_width
        y_cursor += 90

        imei_x = (width - draw.textlength(imei, font=imei_font)) // 2
        draw.text((imei_x, y_cursor), imei, fill='blue', font=imei_font)
        y_cursor += 30

        if price:
            price_text = f"Narxi: {price}"
            price_x = (width - draw.textlength(price_text, font=price_font)) // 2
            draw.text((price_x, y_cursor), price_text, fill='black', font=price_font)

        return img

    def display_barcode(self):
        for widget in self.display_frame.winfo_children():
            widget.destroy()
        display_image = self.barcode_image.resize((450, 200), Image.Resampling.LANCZOS)
        canvas = tk.Canvas(self.display_frame, width=460, height=210, bg='white')
        canvas.pack(pady=20)
        self.photo = tk.PhotoImage(data=self.pil_to_tkinter(display_image))
        canvas.create_image(230, 105, image=self.photo)

    def pil_to_tkinter(self, pil_image):
        bio = io.BytesIO()
        pil_image.save(bio, format='PNG')
        bio.seek(0)
        return bio.getvalue()

    def save_barcode(self):
        if not self.barcode_image:
            return
        imei = self.imei_entry.get().strip()
        default_name = f"barcode_{imei}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")],
            initialfile=default_name
        )
        if file_path:
            self.barcode_image.save(file_path, "PNG")
            messagebox.showinfo("Saqlandi", f"Fayl saqlandi: {file_path}")

    def print_barcode(self):
        if not self.barcode_image:
            return
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
                self.barcode_image.save(tmpfile.name, "PNG")
                if platform.system() == "Windows":
                    os.startfile(tmpfile.name, "print")
                elif platform.system() == "Darwin":  # macOS
                    subprocess.run(["lp", tmpfile.name])
                else:
                    subprocess.run(["lp", tmpfile.name])
        except Exception as e:
            messagebox.showerror("Xato", f"Chop etishda xatolik: {str(e)}")

    def clear_all(self):
        self.imei_entry.delete(0, 'end')
        self.model_entry.delete(0, 'end')
        self.price_entry.delete(0, 'end')
        self.verified_checkbox.deselect()
        for widget in self.display_frame.winfo_children():
            widget.destroy()
        self.initial_label = ctk.CTkLabel(
            self.display_frame,
            text="\ud83d\udd0d IMEI raqamini kiriting va\n'SHTRIX KOD YARATISH' tugmasini bosing",
            font=ctk.CTkFont(size=16),
            text_color="#666666"
        )
        self.initial_label.pack(expand=True)
        self.save_btn.configure(state="disabled")
        self.print_btn.configure(state="disabled")
        self.barcode_image = None

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = IMEIBarcodeGenerator()
    app.run()
