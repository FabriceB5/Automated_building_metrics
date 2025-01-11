# Importiere das Tkinter-Modul für die GUI-Erstellung und zusätzliche Komponenten
import tkinter as tk
from tkinter import filedialog, messagebox

# Importiere spezifische Funktionen aus Modulen für die IFC-Verarbeitung und Excel-Export
from ifc_processing import process_bgf_berechnung
from ifc_processing import process_kubische_berechnung
from ifc_processing import debug_ifc_structure
from excel_export import export_to_excel

# Globale Variable für den IFC-Dateipfad
ifc_file_path = None

# Funktion zum Hochladen einer IFC-Datei
def upload_file():
    """
    Öffnet einen Datei-Dialog zum Auswählen einer IFC-Datei.
    Wenn eine Datei erfolgreich ausgewählt wurde, wird der Pfad global gespeichert 
    und die Berechnungsschaltflächen aktiviert.
    """
    global ifc_file_path
    ifc_file_path = filedialog.askopenfilename(filetypes=[("IFC files", "*.ifc")])
    if ifc_file_path:  # Wenn der Benutzer eine Datei auswählt
        messagebox.showinfo("Erfolg", f"Datei erfolgreich hochgeladen: {ifc_file_path}")
        # Berechnungsschaltflächen aktivieren
        btn_bgf_berechnung.config(state=tk.NORMAL)
        btn_kubische_berechnung.config(state=tk.NORMAL)

# Funktion zur Berechnung der Bruttogeschossfläche (BGF)
def bgf_berechnung():
    """
    Führt die BGF-Berechnung basierend auf der hochgeladenen IFC-Datei durch.
    Exportiert die Ergebnisse in eine Excel-Datei.
    """
    if ifc_file_path:  # Überprüfen, ob eine Datei hochgeladen wurde
        try:
            # Debugging der IFC-Struktur zur Analyse der Datei
            debug_ifc_structure(ifc_file_path)

            # Verarbeitung der BGF-Berechnung und Excel-Export
            raum_liste, geschoss_auflistung = process_bgf_berechnung(ifc_file_path)
            export_to_excel(raum_liste, geschoss_auflistung, "BGF_Berechnung.xlsx")
            messagebox.showinfo("Erfolg", "BGF-Berechnung abgeschlossen und Excel exportiert")
        except Exception as e:
            messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {e}")

# Funktion zur Berechnung von kubischen Parametern
def kubische_berechnung():
    """
    Führt die kubische Berechnung basierend auf der hochgeladenen IFC-Datei durch.
    Exportiert die Ergebnisse in eine Excel-Datei.
    """
    if ifc_file_path:  # Überprüfen, ob eine Datei hochgeladen wurde
        try:
            # Verarbeitung der kubischen Berechnung und Excel-Export
            raum_liste, geschoss_auflistung = process_kubische_berechnung(ifc_file_path)
            export_to_excel(raum_liste, geschoss_auflistung, "Kubische_Berechnung.xlsx")
            messagebox.showinfo("Erfolg", "Kubische Berechnung abgeschlossen und Excel exportiert")
        except Exception as e:
            messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {e}")

# Hauptfenster der Anwendung erstellen
root = tk.Tk()
root.title("Automated Building Metrics")
root.geometry("800x800")
root.configure(bg="#2c2c2c")

# Überschrift der Anwendung
taskbar = tk.Frame(root, bg="black", height=50)
taskbar.pack(side=tk.TOP, fill=tk.X)
title_label = tk.Label(
    taskbar,
    text="Automated Building Metrics",
    font=("Helvetica", 24, "bold"),
    bg="black",
    fg="#ffffff"
)
title_label.pack(pady=10)

# Hauptbereich
main_frame = tk.Frame(root, bg="#2c2c2c")
main_frame.pack(fill=tk.BOTH, expand=True)

# Linker Bereich für Buttons
left_frame = tk.Frame(main_frame, bg="#2c2c2c", width=200)
left_frame.pack(side=tk.LEFT, fill=tk.Y)

# Trennlinie
separator = tk.Frame(main_frame, bg="#666666", width=2)
separator.pack(side=tk.LEFT, fill=tk.Y)

# Rechter Bereich für Informationen
right_frame = tk.Frame(main_frame, bg="#333333")
right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

info_label = tk.Label(
    right_frame,
    text="Bitte laden Sie eine IFC-Datei hoch, um mit der Berechnung zu beginnen.",
    bg="#333333",
    fg="#ffffff",
    font=("Helvetica", 14),
    wraplength=400,
    justify="center"
)
info_label.pack(expand=True)

# Buttons im linken Bereich
btn_upload = tk.Button(
    left_frame,
    text="IFC-Datei hochladen",
    command=upload_file,
    bg="#2c2c2c",  # Gleiche Hintergrundfarbe wie das Fenster
    fg="white",  # Schriftfarbe weiß
    font=("Helvetica", 14, "bold"),
    highlightbackground="white",  # Rahmenfarbe
    highlightthickness=2,  # Rahmendicke
    bd=0  # Deaktiviert den Standardrahmen
)
btn_upload.pack(pady=20, padx=10, fill=tk.X)

btn_bgf_berechnung = tk.Button(
    left_frame,
    text="BGF-Berechnung",
    state=tk.DISABLED,
    command=bgf_berechnung,
    bg="#2c2c2c",  # Gleiche Hintergrundfarbe wie das Fenster
    fg="white",  # Schriftfarbe weiß
    font=("Helvetica", 14, "bold"),
    highlightbackground="white",  # Rahmenfarbe
    highlightthickness=2,  # Rahmendicke
    bd=0  # Deaktiviert den Standardrahmen
)
btn_bgf_berechnung.pack(pady=10, padx=10, fill=tk.X)

btn_kubische_berechnung = tk.Button(
    left_frame,
    text="Kubische Berechnung",
    state=tk.DISABLED,
    command=kubische_berechnung,
    bg="#2c2c2c",  # Gleiche Hintergrundfarbe wie das Fenster
    fg="white",  # Schriftfarbe weiß
    font=("Helvetica", 14, "bold"),
    highlightbackground="white",  # Rahmenfarbe
    highlightthickness=2,  # Rahmendicke
    bd=0  # Deaktiviert den Standardrahmen
)
btn_kubische_berechnung.pack(pady=10, padx=10, fill=tk.X)



root.mainloop()