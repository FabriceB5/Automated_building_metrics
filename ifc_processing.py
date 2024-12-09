import ifcopenshell

# Liste möglicher Namen für Flächenattribute
FLAECHE_NAMEN = ["Fläche", "Area", "Superficie", "Surface"]

def debug_ifc_structure(ifc_file_path):
    """
    Analysiert die IfcBuildingStoreys und ihre Beziehungen zu Räumen.
    Diese Funktion dient zur Strukturprüfung einer IFC-Datei. Sie untersucht, ob und wie die Geschosse
    (`IfcBuildingStoreys`) mit Räumen (`IfcSpace`) über spezifische Beziehungen verknüpft sind.

    :param ifc_file_path: Pfad zur IFC-Datei, die analysiert werden soll.
    """
    # Öffne die IFC-Datei
    model = ifcopenshell.open(ifc_file_path)

    print("Prüfe IfcBuildingStoreys und deren Beziehungen...")
    # Iteriere über alle IfcBuildingStoreys (Geschosse) in der IFC-Datei
    for storey in model.by_type("IfcBuildingStorey"):
        # Lese den Namen des Geschosses (falls vorhanden), sonst "Unbekannt"
        storey_name = storey.Name if hasattr(storey, "Name") else "Unbekannt"
        print(f"\nGeschoss: {storey_name}")

        # Prüfe, ob das Geschoss eine IsDecomposedBy-Beziehung hat (zeigt verknüpfte Objekte)
        if storey.IsDecomposedBy:
            print(f"  IsDecomposedBy vorhanden: {len(storey.IsDecomposedBy)} Einträge")
            # Iteriere über die IsDecomposedBy-Beziehungen
            for rel in storey.IsDecomposedBy:
                # Zeige den Beziehungstyp (z. B. IfcRelAggregates oder IfcRelContainedInSpatialStructure)
                print(f"    Beziehungstyp: {rel.is_a()}")
                # Falls die Beziehung IfcRelContainedInSpatialStructure ist, zeige die Anzahl der verknüpften Objekte
                if rel.is_a("IfcRelContainedInSpatialStructure"):
                    print(f"    Anzahl RelatedObjects: {len(rel.RelatedObjects)}")
        else:
            # Keine IsDecomposedBy-Beziehungen gefunden
            print("  Keine IsDecomposedBy-Beziehungen gefunden.")


def process_bgf_berechnung(ifc_file_path):
    """
    Berechnet die BGF (Bruttogrundfläche) pro Raum und summiert die Flächen pro Geschoss.

    :param ifc_file_path: Pfad zur IFC-Datei.
    :return: Tuple (raum_liste, geschoss_auflistung)
        - raum_liste: Liste mit Raumdetails (Geschoss, Raumname, Fläche)
        - geschoss_auflistung: Liste mit summierten Flächen pro Geschoss
    """

    model = ifcopenshell.open(ifc_file_path)

    raum_liste = []
    geschoss_flaechen = {}

    print("Beginne die Verarbeitung der IfcBuildingStoreys...")

    # Iteriere über alle Geschosse in der IFC-Datei
    for storey in model.by_type("IfcBuildingStorey"):
        storey_name = storey.Name if hasattr(storey, "Name") else "Unbekannt"

        # Initialisiere die Fläche des Geschosses, falls noch nicht vorhanden
        if storey_name not in geschoss_flaechen:
            geschoss_flaechen[storey_name] = 0

        # Suche nach Räumen, die mit dem Geschoss verknüpft sind
        spaces = []  # Liste der Räume im Geschoss
        if storey.IsDecomposedBy:  # Prüfen, ob das Geschoss Räume enthält
            for rel in storey.IsDecomposedBy:
                if rel.is_a("IfcRelAggregates"):  # Räume sind über IfcRelAggregates verknüpft
                    spaces.extend(rel.RelatedObjects)

        print(f"DEBUG: Geschoss {storey_name} hat {len(spaces)} Räume.")

        # Iteriere über die Räume (IfcSpace) im Geschoss
        for space in spaces:
            if space.is_a("IfcSpace"):  # Prüfen, ob es sich um einen Raum handelt
                # Lese den Namen des Raumes (falls vorhanden), sonst "Unbenannter Raum"
                room_name = space.Name if hasattr(space, "Name") else "Unbenannter Raum"
                area = 0

                # Extrahiere die Fläche aus den Property-Sets des Raumes
                for property_set in space.IsDefinedBy:  # Durchlaufe alle verknüpften PropertySets
                    if property_set.is_a("IfcRelDefinesByProperties"):
                        props = property_set.RelatingPropertyDefinition
                        if props.is_a("IfcPropertySet"):  # Prüfe, ob es ein PropertySet ist, enthält Eigenschaften des Raumes
                            for prop in props.HasProperties:  # Iteriere über die Eigenschaften
                                # Prüfen, ob der Name der Eigenschaft in den definierten Flächenbezeichnungen ist
                                if prop.Name in FLAECHE_NAMEN:
                                    area_value = getattr(prop.NominalValue, 'wrappedValue', 0)
                                    if isinstance(area_value, str):  # Entferne "m²", falls vorhanden
                                        area_value = area_value.replace("m²", "").strip()
                                    try:
                                        area = float(area_value)  # Konvertiere die Fläche zu Float
                                    except ValueError:
                                        area = 0  # Setze die Fläche auf 0, falls ungültig
                                    break  # Verlasse die Schleife nach Finden der Fläche

                print(f"DEBUG: Raum {room_name} im Geschoss {storey_name} hat Fläche: {area}")

                # Füge die Raumdetails zur Liste hinzu
                raum_liste.append({
                    "Bezeichnung": f"{storey_name} - {room_name}",
                    "Fläche": area
                })

                # Addiere die Fläche des Raumes zur Gesamtfläche des Geschosses
                geschoss_flaechen[storey_name] += area
                print(f"DEBUG: Aktuelle Gesamtfläche für Geschoss {storey_name}: {geschoss_flaechen[storey_name]}")

    # Konvertiere die summierten Geschossflächen in eine Liste
    geschoss_auflistung = [
        {"Bezeichnung": storey_name, "Fläche": total_area}
        for storey_name, total_area in geschoss_flaechen.items()
    ]

    # Gib die Raumliste und die summierten Geschossflächen zurück
    return raum_liste, geschoss_auflistung

def process_kubische_berechnung(ifc_file_path):
    """
    Berechnet die Kubatur (Volumen) pro Raum und summiert die Volumen pro Geschoss.

    :param ifc_file_path: Pfad zur IFC-Datei.
    :return: Tuple (raum_liste, geschoss_auflistung)
        - raum_liste: Liste mit Raumdetails (Geschoss, Raumname, Volumen)
        - geschoss_auflistung: Liste mit summierten Volumen pro Geschoss
    """

    # IFC-Modell öffnen
    model = ifcopenshell.open(ifc_file_path)

    raum_liste = []  # Liste für Raumdetails (Raumname, Volumen)
    geschoss_volumen = {}  # Dictionary für summierte Volumen pro Geschoss

    print("Beginne die Verarbeitung der IfcBuildingStoreys für Kubatur...")

    # Iteriere über alle Geschosse
    for storey in model.by_type("IfcBuildingStorey"):
        # Name des Geschosses lesen (oder "Unbekannt" setzen, wenn Name fehlt)
        storey_name = storey.Name if hasattr(storey, "Name") else "Unbekannt"

        # Initialisiere Volumen für das Geschoss
        if storey_name not in geschoss_volumen:
            geschoss_volumen[storey_name] = 0

        # Suche alle Räume, die mit dem Geschoss verknüpft sind
        spaces = []
        if storey.IsDecomposedBy:  # Prüfe, ob das Geschoss Räume enthält
            for rel in storey.IsDecomposedBy:
                if rel.is_a("IfcRelAggregates"):  # Räume sind oft über Aggregates verknüpft
                    spaces.extend(rel.RelatedObjects)

        print(f"DEBUG: Geschoss {storey_name} hat {len(spaces)} Räume.")

        # Iteriere über die Räume im Geschoss
        for space in spaces:
            if space.is_a("IfcSpace"):  # Prüfe, ob es sich um einen Raum handelt
                room_name = space.Name if hasattr(space, "Name") else "Unbenannter Raum"
                volume = 0  # Initialisiere das Volumen des Raumes

                # Zugriff auf Mengen (Quantities)
                if hasattr(space, "IsDefinedBy"):  # Prüfen, ob Mengen definiert sind
                    for property_set in space.IsDefinedBy:  # Alle PropertySets des Raumes durchlaufen
                        if property_set.is_a("IfcRelDefinesByProperties"):
                            props = property_set.RelatingPropertyDefinition
                            if props.is_a("IfcElementQuantity"):  # Suche nach Mengen (ElementQuantity)
                                print(f"DEBUG: Mengen gefunden für Raum {room_name}:")
                                for quantity in props.Quantities:
                                    print(f"  Menge: {quantity.Name}, Wert: {getattr(quantity, 'VolumeValue', None)}")
                                    if quantity.Name.lower() in ["volumen", "volume", "grossvolume"]:  # Alternative Namen prüfen
                                        volume_value = getattr(quantity, 'VolumeValue', 0)
                                        try:
                                            volume = float(volume_value)  # Konvertiere zu Float
                                            break
                                        except ValueError:
                                            volume = 0  # Setze Volumen auf 0 bei ungültigem Wert

                # Debugging-Ausgabe: Volumen des Raumes
                print(f"DEBUG: Raum {room_name} im Geschoss {storey_name} hat Volumen: {volume}")

                # Füge Raumdetails zur Liste hinzu
                raum_liste.append({
                    "Bezeichnung": f"{storey_name} - {room_name}",
                    "Volumen": volume
                })

                # Addiere Volumen des Raumes zum Gesamtvolumen des Geschosses
                geschoss_volumen[storey_name] += volume
                print(f"DEBUG: Aktuelles Gesamtvolumen für Geschoss {storey_name}: {geschoss_volumen[storey_name]}")

    # Summiere die Geschossdaten und wandle sie in eine Liste um
    geschoss_auflistung = [
        {"Bezeichnung": storey_name, "Volumen": total_volume}
        for storey_name, total_volume in geschoss_volumen.items()
    ]

    # Gib die Ergebnisse zurück: Raumliste und Geschossauflistung
    return raum_liste, geschoss_auflistung