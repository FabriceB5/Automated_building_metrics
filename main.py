import tkinter as tk
from tkinter import filedialog, messagebox
from ifc_processing import process_bgf_berechnung_detailliert
from ifc_processing import process_kubische_berechnung
from ifc_processing import debug_ifc_structure
from excel_export import export_to_excel_detailliert

def upload_file():
    global ifc_file_path
    ifc_file_path = filedialog.askopenfilename(filetypes=[("IFC files", "*.ifc")])
    if ifc_file_path:
        messagebox.showinfo("Erfolg", f"Datei erfolgreich hochgeladen: {ifc_file_path}")
        btn_bgf_berechnung.config(state=tk.NORMAL)
        btn_kubische_berechnung.config(state=tk.NORMAL)

def bgf_berechnung():
    if ifc_file_path:
        try:
            # Debugging der IFC-Struktur
            debug_ifc_structure(ifc_file_path)

            raum_liste, geschoss_auflistung = process_bgf_berechnung_detailliert(ifc_file_path)
            export_to_excel_detailliert(raum_liste, geschoss_auflistung, "BGF_Berechnung.xlsx")
            messagebox.showinfo("Erfolg", "BGF-Berechnung abgeschlossen und Excel exportiert!")
        except Exception as e:
            messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {e}")

def kubische_berechnung():
    if ifc_file_path:
        try:
            raum_liste, geschoss_auflistung = process_kubische_berechnung(ifc_file_path)
            export_to_excel_detailliert(raum_liste, geschoss_auflistung, "Kubische_Berechnung.xlsx")
            messagebox.showinfo("Erfolg", "Kubische Berechnung abgeschlossen und Excel exportiert!")
        except Exception as e:
            messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {e}")

root = tk.Tk()
root.title("Automated Building Metrics")
root.geometry("600x400")
root.configure(bg="#2c2c2c")

title_label = tk.Label(
    root,
    text="Automated Building Metrics",
    font=("Helvetica", 24, "bold"),
    bg="#2c2c2c",
    fg="#ffa500"
)
title_label.pack(pady=20)

btn_upload = tk.Button(
    root,
    text="IFC-Datei hochladen",
    command=upload_file, bg="#ffa500",
    fg="black",
    font=("Helvetica", 14, "bold")
)
btn_upload.pack(pady=10)

btn_bgf_berechnung = tk.Button(
    root,
    text="BGF-Berechnung",
    state=tk.DISABLED,
    command=bgf_berechnung,
    bg="#ffa500",
    fg="black",
    font=("Helvetica", 14, "bold")
)
btn_bgf_berechnung.pack(pady=10)

btn_kubische_berechnung = tk.Button(
    root,
    text="Kubische Berechnung",
    state=tk.DISABLED,
    command=kubische_berechnung,
    bg="#ffa500",
    fg="black",
    font=("Helvetica", 14, "bold")
)
btn_kubische_berechnung.pack(pady=10)

root.mainloop()