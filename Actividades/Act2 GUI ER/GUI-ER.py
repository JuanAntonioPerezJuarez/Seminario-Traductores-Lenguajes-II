import tkinter as tk
from tkinter import messagebox
import re

def validate_and_submit():
    phone = phone_entry.get()
    email = email_entry.get()
    curp = curp_entry.get()
    rfc = rfc_entry.get()
    ip = ip_entry.get()
    birthday = birthday_entry.get()

    errors = []

    # Validate phone number
    if not re.fullmatch(r"\d{10}", phone):
        errors.append("Teléfono debe tener 10 dígitos.")

    # Validate email
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        errors.append("Correo electrónico no válido.")

    # Validate CURP
    if not re.fullmatch(r"[A-Z]{4}\d{6}[HM][A-Z]{5}\d{2}", curp):
        errors.append("CURP no válida.")

    # Validate RFC
    if not re.fullmatch(r"[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}", rfc):
        errors.append("RFC no válido.")

    # Validate IPv4 address
    if not re.fullmatch(r"(\d{1,3}\.){3}\d{1,3}", ip) or not all(0 <= int(part) <= 255 for part in ip.split('.')):
        errors.append("Dirección IP v4 no válida.")

    # Validate birthday
    if not re.fullmatch(r"\d{2}/\d{2}/\d{2}", birthday):
        errors.append("Fecha de cumpleaños debe estar en formato DD/MM/AA.")

    # Show errors or success message
    if errors:
        messagebox.showerror("Errores de validación", "\n".join(errors))
    else:
        messagebox.showinfo("Éxito", "Todos los datos son válidos.")

# Create the main window
root = tk.Tk()
root.title("Formulario de datos personales")
root.geometry("400x400")

# Labels and Entry fields
fields = [
    ("Teléfono (10 dígitos):", "phone_entry"),
    ("Correo electrónico:", "email_entry"),
    ("CURP:", "curp_entry"),
    ("RFC:", "rfc_entry"),
    ("Dirección IP v4:", "ip_entry"),
    ("Fecha de cumpleaños (DD/MM/AA):", "birthday_entry"),
]

entries = {}
for i, (label_text, var_name) in enumerate(fields):
    label = tk.Label(root, text=label_text, anchor="w")
    label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
    entry = tk.Entry(root, width=30)
    entry.grid(row=i, column=1, padx=10, pady=5)
    entries[var_name] = entry

# Map entry variables
phone_entry = entries["phone_entry"]
email_entry = entries["email_entry"]
curp_entry = entries["curp_entry"]
rfc_entry = entries["rfc_entry"]
ip_entry = entries["ip_entry"]
birthday_entry = entries["birthday_entry"]

# Submit button
submit_button = tk.Button(root, text="Validar y Enviar", command=validate_and_submit)
submit_button.grid(row=len(fields), column=0, columnspan=2, pady=20)

# Run the application
root.mainloop()