import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import *

def generate_rounded_qr_with_logo(data, file_name, logo_path=None):
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=25,
        border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        color_mask=SolidFillColorMask(back_color=(255, 255, 255), front_color=(0, 0, 0))
    )
    img = img.convert('RGBA')
    if logo_path:
        logo = Image.open(logo_path).convert("RGBA")
        img_w, img_h = img.size
        logo_size = int(img_w * 0.2)
        logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
        pos = ((img_w - logo_size) // 2, (img_h - logo_size) // 2)
        img.paste(logo, pos, mask=logo)
    img.save(file_name)

def on_generate():
    data = entry.get()
    if not data:
        messagebox.showwarning("Advertencia", "Por favor ingresa el texto o URL.")
        return
    file_name = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png")],
        title="Guardar QR como..."
    )
    if not file_name:
        return
    try:
        generate_rounded_qr_with_logo(data, file_name, logo_path=None)
        messagebox.showinfo("Éxito", f"QR guardado como:\n{file_name}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# --- UI Moderna con ttkbootstrap ---
app = tb.Window(themename="superhero")
app.title("ModernQR Studio")  # Cambiado el título aquí
app.geometry("400x200")
app.resizable(False, False)

label = tb.Label(app, text="Texto o URL para el QR:", font=("Segoe UI", 12))
label.pack(pady=(30, 10))

entry = tb.Entry(app, font=("Segoe UI", 12), width=35)
entry.pack(pady=5)

btn = tb.Button(app, text="Generar QR", bootstyle=SUCCESS, command=on_generate)
btn.pack(pady=20)

app.mainloop()
