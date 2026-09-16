import qrcode


def render_terminal_qr(value):
    """Render an otpauth:// URL as a scannable QR code in the terminal."""
    qr = qrcode.QRCode(border=2)
    qr.add_data(value)
    qr.make(fit=True)
    return '\n'.join(
        ''.join('██' if cell else '  ' for cell in row)
        for row in qr.get_matrix()
    )
