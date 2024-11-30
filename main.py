# Importiere das Tkinter-Modul für die GUI-Erstellung und zusätzliche Komponenten
import tkinter as tk
from tkinter import filedialog, messagebox

# Importiere spezifische Funktionen aus Modulen für die IFC-Verarbeitung und Excel-Export
from ifc_processing import process_bgf_berechnung
from ifc_processing import process_kubische_berechnung
from ifc_processing import debug_ifc_structure
from excel_export import export_to_excel

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

# Funktion zur Berechnung der Bruttogrundfläche (BGF)
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
            # Erfolgsmeldung anzeigen
            messagebox.showinfo("Erfolg", "BGF-Berechnung abgeschlossen und Excel exportiert!")
        except Exception as e:
            # Fehler melden, falls etwas schiefläuft
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
            # Erfolgsmeldung anzeigen
            messagebox.showinfo("Erfolg", "Kubische Berechnung abgeschlossen und Excel exportiert!")
        except Exception as e:
            # Fehler melden, falls etwas schiefläuft
            messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {e}")

# Hauptfenster der Anwendung erstellen
root = tk.Tk()
root.title("Automated Building Metrics")  # Titel des Fensters
root.geometry("600x400")  # Fenstergröße
root.configure(bg="#2c2c2c")  # Hintergrundfarbe des Fensters

# Überschrift der Anwendung
title_label = tk.Label(
    root,
    text="Automated Building Metrics",
    font=("Helvetica", 24, "bold"),  # Schriftart und Größe
    bg="#2c2c2c",  # Hintergrundfarbe
    fg="#ffa500"  # Schriftfarbe
)
title_label.pack(pady=20)  # Abstand nach oben und unten

# Schaltfläche zum Hochladen der IFC-Datei
btn_upload = tk.Button(
    root,
    text="IFC-Datei hochladen",  # Beschriftung der Schaltfläche
    command=upload_file,  # Verknüpfte Funktion
    bg="#ffa500",  # Hintergrundfarbe
    fg="black",  # Schriftfarbe
    font=("Helvetica", 14, "bold")  # Schriftart und Größe
)
btn_upload.pack(pady=10)  # Abstand nach oben und unten

# Schaltfläche für die BGF-Berechnung
btn_bgf_berechnung = tk.Button(
    root,
    text="BGF-Berechnung",  # Beschriftung der Schaltfläche
    state=tk.DISABLED,  # Initial deaktiviert
    command=bgf_berechnung,  # Verknüpfte Funktion
    bg="#ffa500",  # Hintergrundfarbe
    fg="black",  # Schriftfarbe
    font=("Helvetica", 14, "bold")  # Schriftart und Größe
)
btn_bgf_berechnung.pack(pady=10)  # Abstand nach oben und unten

# Schaltfläche für die kubische Berechnung
btn_kubische_berechnung = tk.Button(
    root,
    text="Kubische Berechnung",  # Beschriftung der Schaltfläche
    state=tk.DISABLED,  # Initial deaktiviert
    command=kubische_berechnung,  # Verknüpfte Funktion
    bg="#ffa500",  # Hintergrundfarbe
    fg="black",  # Schriftfarbe
    font=("Helvetica", 14, "bold")  # Schriftart und Größe
)
btn_kubische_berechnung.pack(pady=10)  # Abstand nach oben und unten

# Start der Tkinter-Hauptschleife
root.mainloop()