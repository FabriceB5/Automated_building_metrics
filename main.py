import tkinter as tk
from tkinter import filedialog, messagebox
from ifc_processing import process_bgf_berechnung, process_kubische_berechnung
from excel_export import export_to_excel
from tkinter import ttk

# Globale Variable für den IFC-Dateipfad
ifc_file_path = None

def upload_file():
    """
    Öffnet einen Datei-Dialog zum Auswählen einer IFC-Datei.
    Wenn eine Datei erfolgreich ausgewählt wurde, wird der Pfad global gespeichert 
    und die Berechnungsschaltflächen aktiviert.
    """
    global ifc_file_path
    ifc_file_path = filedialog.askopenfilename(filetypes=[("IFC files", "*.ifc")])
    if ifc_file_path:
        messagebox.showinfo("Erfolg", f"Datei erfolgreich hochgeladen: {ifc_file_path}")
        btn_bgf_berechnung.config(state=tk.NORMAL)
        btn_kubische_berechnung.config(state=tk.NORMAL)

def bgf_berechnung():
    """
    Führt die BGF-Berechnung durch und zeigt die Ergebnisse an.
    """
    if not ifc_file_path:
        messagebox.showerror("Fehler", "Bitte laden Sie zuerst eine IFC-Datei hoch.")
        return

    try:
        # BGF-Berechnung durchführen
        raum_liste, geschoss_auflistung = process_bgf_berechnung(ifc_file_path)
        export_to_excel(raum_liste, geschoss_auflistung, "BGF_Berechnung.xlsx")

        # Ergebnisse in der Tabelle anzeigen
        update_results_table(raum_liste)

        # Gesamtfläche der BGF berechnen
        total_bgf = sum(item["Fläche"] for item in geschoss_auflistung)

        # Grundstücksfläche und Ausnützungsziffer abrufen
        try:
            grundstuecksflaeche = float(entry_gf.get())
            ausnuetzungsziffer = float(entry_az.get())
        except ValueError:
            messagebox.showerror("Fehler", "Bitte geben Sie gültige Zahlenwerte für GF und AZ ein.")
            return

        # Maximale zulässige BGF berechnen
        max_bgf = grundstuecksflaeche * ausnuetzungsziffer

        # Ergebnis anzeigen
        messagebox.showinfo(
            "BGF-Auswertung",
            f"BGF ist: {total_bgf:.2f} m²\n"
            f"BGF soll: {max_bgf:.2f} m²\n"
            f"{'Ausnutzung überschritten!' if total_bgf > max_bgf else 'Ausnutzung in Ordnung.'}"
        )

    except Exception as e:
        messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {str(e)}")

def kubische_berechnung():
    """
    Führt die Kubische Berechnung durch und zeigt die Ergebnisse an.
    """
    if not ifc_file_path:
        messagebox.showerror("Fehler", "Bitte laden Sie zuerst eine IFC-Datei hoch.")
        return

    try:
        # Kubische Berechnung durchführen
        raum_liste, geschoss_auflistung = process_kubische_berechnung(ifc_file_path)
        export_to_excel(raum_liste, geschoss_auflistung, "Kubische_Berechnung.xlsx")

        # Ergebnisse in der Tabelle anzeigen
        update_results_table(raum_liste)

        messagebox.showinfo("Erfolg", "Kubische Berechnung abgeschlossen und Excel exportiert.")
    except Exception as e:
        messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {str(e)}")

def update_results_table(data):
    """
    Aktualisiert die Ergebnis-Tabelle und passt die Spaltenüberschrift basierend auf den Daten an.
    :param data: Liste von Dictionaries mit "Bezeichnung" und entweder "Fläche" oder "Volumen".
    """
    # Tabelle leeren
    for row in results_table.get_children():
        results_table.delete(row)

    # Prüfen, ob die Daten "Fläche" oder "Volumen" enthalten
    if data and "Fläche" in data[0]:
        results_table.heading("Wert", text="Fläche (m²)")
    elif data and "Volumen" in data[0]:
        results_table.heading("Wert", text="Volumen (m³)")
    else:
        results_table.heading("Wert", text="Wert")

    # Daten einfügen
    for row in data:
        results_table.insert("", tk.END, values=(row["Bezeichnung"], row.get("Fläche", row.get("Volumen", "N/A"))))

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
    fg="white"
)
title_label.pack(pady=10)

# Hauptbereich
main_frame = tk.Frame(root, bg="#2c2c2c")
main_frame.pack(fill=tk.BOTH, expand=True)

# Linker Bereich für Eingabe und Buttons
left_frame = tk.Frame(main_frame, bg="#2c2c2c", width=200)
left_frame.pack(side=tk.LEFT, fill=tk.Y)

# Trennlinie
separator = tk.Frame(main_frame, bg="#666666", width=2)
separator.pack(side=tk.LEFT, fill=tk.Y)

# Rechter Bereich für Informationen und Ergebnisse
right_frame = tk.Frame(main_frame, bg="#333333")
right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

info_label = tk.Label(
    right_frame,
    text="Bitte laden Sie eine IFC-Datei hoch und geben Sie die Grundstücksfläche (GF) und die Ausnützungsziffer (AZ) ein.",
    bg="#333333",
    fg="white",
    font=("Helvetica", 14),
    wraplength=400,
    justify="center"
)
info_label.pack(pady=20)

# Ergebnis-Tabelle
results_table = ttk.Treeview(right_frame, columns=("Bezeichnung", "Wert"), show="headings")
results_table.heading("Bezeichnung", text="Bezeichnung")
results_table.heading("Wert", text="Wert")  # Initialwert
results_table.pack(fill=tk.BOTH, expand=True)

# Eingabefelder
label_gf = tk.Label(
    left_frame,
    text="GF (Grundstücksfläche):",
    bg="#2c2c2c",
    fg="white",
    font=("Helvetica", 12)
)
label_gf.pack(pady=5, padx=10, anchor="w")
entry_gf = tk.Entry(left_frame, bg="white", fg="black", font=("Helvetica", 12))
entry_gf.pack(pady=5, padx=10, fill=tk.X)

label_az = tk.Label(
    left_frame,
    text="AZ (Ausnützungsziffer):",
    bg="#2c2c2c",
    fg="white",
    font=("Helvetica", 12)
)
label_az.pack(pady=5, padx=10, anchor="w")
entry_az = tk.Entry(left_frame, bg="white", fg="black", font=("Helvetica", 12))
entry_az.pack(pady=5, padx=10, fill=tk.X)

# Buttons
btn_upload = tk.Button(
    left_frame,
    text="IFC-Datei hochladen",
    command=upload_file,
    bg="#2c2c2c",
    fg="white",
    font=("Helvetica", 14, "bold"),
    highlightbackground="white",
    highlightthickness=2,
    bd=0
)
btn_upload.pack(pady=20, padx=10, fill=tk.X)

btn_bgf_berechnung = tk.Button(
    left_frame,
    text="BGF-Berechnung",
    state=tk.DISABLED,
    command=bgf_berechnung,
    bg="#2c2c2c",
    fg="white",
    font=("Helvetica", 14, "bold"),
    highlightbackground="white",
    highlightthickness=2,
    bd=0
)
btn_bgf_berechnung.pack(pady=10, padx=10, fill=tk.X)

btn_kubische_berechnung = tk.Button(
    left_frame,
    text="Kubische Berechnung",
    state=tk.DISABLED,
    command=kubische_berechnung,
    bg="#2c2c2c",
    fg="white",
    font=("Helvetica", 14, "bold"),
    highlightbackground="white",
    highlightthickness=2,
    bd=0
)
btn_kubische_berechnung.pack(pady=10, padx=10, fill=tk.X)

root.mainloop()