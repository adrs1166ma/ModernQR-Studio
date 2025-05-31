import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
from PIL import Image

def generate_rounded_qr_with_logo(data, file_name, logo_path=None):
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=25,  # Aumentado de 10 a 25
        border=2,
    )

    qr.add_data(data)
    qr.make(fit=True)

    # Crear imagen QR con módulos redondeados
    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),  # Redondear shapes
        color_mask=SolidFillColorMask(back_color=(255, 255, 255), front_color=(0, 0, 0))
    )

    img = img.convert('RGBA')

    if logo_path:
        logo = Image.open(logo_path).convert("RGBA")

        # Redimensionar logo de manera proporcional
        img_w, img_h = img.size
        logo_size = int(img_w * 0.2)  # 20% del QR
        logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

        # Posicionar logo en el centro
        pos = ((img_w - logo_size) // 2, (img_h - logo_size) // 2)
        img.paste(logo, pos, mask=logo)

    img.save(file_name)
    print('QR code with rounded shapes and logo saved as', file_name)

# Uso:
generate_rounded_qr_with_logo('https://chat.whatsapp.com/JQV7aQ7wuJoLndAQKV1Hh1', 'qr_cybersu.png', logo_path='logo.png')
