import tkinter as tk
from tkinter import filedialog, messagebox
from processors.ifc_processing import process_kubische_berechnung, process_bgf_berechnung
from processors.excel_export import export_to_excel

# Funktion zur Auswahl der IFC-Datei
def upload_file():
    global ifc_file_path
    ifc_file_path = filedialog.askopenfilename(filetypes=[("IFC files", "*.ifc")])
    if ifc_file_path:
        messagebox.showinfo("Erfolg", f"Datei erfolgreich hochgeladen: {ifc_file_path}")
        btn_kubische_berechnung.config(state=tk.NORMAL)
        btn_bgf_berechnung.config(state=tk.NORMAL)

# Funktion für Kubische Berechnung
def kubische_berechnung():
    if ifc_file_path:
        result = process_kubische_berechnung(ifc_file_path)
        export_to_excel(result, "Kubische_Berechnung.xlsx")
        messagebox.showinfo("Erfolg", "Kubische Berechnung abgeschlossen und Excel exportiert!")

# Funktion für BGF-Berechnung
def bgf_berechnung():
    if ifc_file_path:
        result = process_bgf_berechnung(ifc_file_path)
        export_to_excel(result, "BGF_Berechnung.xlsx")
        messagebox.showinfo("Erfolg", "BGF-Berechnung abgeschlossen und Excel exportiert!")

# Hauptfenster erstellen
root = tk.Tk()
root.title("Automated Building Metrics")

# Fenstergröße einstellen
root.geometry("600x400")  # Breite x Höhe
root.configure(bg="#2c2c2c")  # Hintergrundfarbe Schwarz

# Titel hinzufügen
title_label = tk.Label(
    root,
    text="Automated Building Metrics",
    font=("Helvetica", 24, "bold"),
    bg="#2c2c2c",  # Hintergrund Schwarz
    fg="#ffa500"   # Schriftfarbe Orange
)
title_label.pack(pady=20)

# Upload-Button
btn_upload = tk.Button(
    root,
    text="IFC-Datei hochladen",
    command=upload_file,
    bg="#ffa500",  # Hintergrund Orange
    fg="black",    # Schriftfarbe Schwarz
    font=("Helvetica", 14, "bold"),
    relief="raised"
)
btn_upload.pack(pady=10)

# Buttons für die Berechnungen
btn_kubische_berechnung = tk.Button(
    root,
    text="Kubische Berechnung",
    state=tk.DISABLED,
    command=kubische_berechnung,
    bg="#ffa500",  # Hintergrund Orange
    fg="black",    # Schriftfarbe Schwarz
    font=("Helvetica", 14, "bold"),
    relief="raised"
)
btn_kubische_berechnung.pack(pady=10)

btn_bgf_berechnung = tk.Button(
    root,
    text="BGF-Berechnung",
    state=tk.DISABLED,
    command=bgf_berechnung,
    bg="#ffa500",  # Hintergrund Orange
    fg="black",    # Schriftfarbe Schwarz
    font=("Helvetica", 14, "bold"),
    relief="raised"
)
btn_bgf_berechnung.pack(pady=10)

# Event-Loop starten
root.mainloop()