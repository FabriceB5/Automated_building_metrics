import pandas as pd

def export_to_excel(raum_liste, geschoss_auflistung, file_name):
    """
    Exportiert die Raum- und Geschossdaten in eine Excel-Datei.

    :param raum_liste: Liste der Raumdetails (Bezeichnung, Fläche/Volumen).
    :param geschoss_auflistung: Liste der summierten Werte pro Geschoss.
    :param file_name: Name der Excel-Datei.
    """
    raum_df = pd.DataFrame(raum_liste)
    geschoss_df = pd.DataFrame(geschoss_auflistung)

    with pd.ExcelWriter(file_name, engine="openpyxl") as writer:
        raum_df.to_excel(writer, sheet_name="Räume", index=False)
        geschoss_df.to_excel(writer, sheet_name="Geschosse", index=False)