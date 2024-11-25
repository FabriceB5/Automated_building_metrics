import pandas as pd

def export_to_excel(data, file_name):
    """
    Exportiert die Daten in eine Excel-Datei.
    
    :param data: Liste von Dictionaries mit den Daten.
    :param file_name: Name der Excel-Datei.
    """
    df = pd.DataFrame(data)
    df.to_excel(file_name, index=False)
