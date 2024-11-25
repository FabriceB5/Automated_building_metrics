import tkinter as tk
from tkinter import filedialog, messagebox
from processors.ifc_processing import process_kubische_berechnung, process_bgf_berechnung
from processors.excel_export import export_to_excel

def upload_file():
    global ifc_file_path
    ifc_file_path = filedialog.askopenfilename(filetypes=[("IFC files", "*.ifc")])
    if ifc_file_path:
        messagebox.showinfo("Erfolg", f"Datei erfolgreich hochgeladen: {ifc_file_path}")
        btn_kubische_berechnung.config(state=tk.NORMAL)
        btn_bgf_berechnung.config(state=tk.NORMAL)

def kubische_berechnung():
    if ifc_file_path:
        result = process_kubische_berechnung(ifc_file_path)
        export_to_excel(result, "Kubische_Berechnung.xlsx")
        messagebox.showinfo("Erfolg", "Kubische Berechnung abgeschlossen und Excel exportiert!")

def bgf_berechnung():
    if ifc_file_path:
        result = process_bgf_berechnung(ifc_file_path)
        export_to_excel(result, "BGF_Berechnung.xlsx")
        messagebox.showinfo("Erfolg", "BGF-Berechnung abgeschlossen und Excel exportiert!")

# GUI-Setup
root = tk.Tk()
root.title("IFC Analyse Tool")

btn_upload = tk.Button(root, text="IFC-Datei hochladen", command=upload_file)
btn_upload.pack(pady=10)

btn_kubische_berechnung = tk.Button(root, text="Kubische Berechnung", state=tk.DISABLED, command=kubische_berechnung)
btn_kubische_berechnung.pack(pady=10)

btn_bgf_berechnung = tk.Button(root, text="BGF-Berechnung", state=tk.DISABLED, command=bgf_berechnung)
btn_bgf_berechnung.pack(pady=10)

root.mainloop()

