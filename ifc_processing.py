import ifcopenshell

# Liste möglicher Namen für Flächenattribute
FLAECHE_NAMEN = ["Fläche", "Area", "Superficie", "Surface"]

def debug_ifc_structure(ifc_file_path):
    """
    Analysiert die IfcBuildingStoreys und ihre Beziehungen zu Räumen.
    """
    model = ifcopenshell.open(ifc_file_path)

    print("Prüfe IfcBuildingStoreys und deren Beziehungen...")
    for storey in model.by_type("IfcBuildingStorey"):
        storey_name = storey.Name if hasattr(storey, "Name") else "Unbekannt"
        print(f"\nGeschoss: {storey_name}")

        if storey.IsDecomposedBy:
            print(f"  IsDecomposedBy vorhanden: {len(storey.IsDecomposedBy)} Einträge")
            for rel in storey.IsDecomposedBy:
                print(f"    Beziehungstyp: {rel.is_a()}")
                if rel.is_a("IfcRelContainedInSpatialStructure"):
                    print(f"    Anzahl RelatedObjects: {len(rel.RelatedObjects)}")
        else:
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

    for storey in model.by_type("IfcBuildingStorey"):
        storey_name = storey.Name if hasattr(storey, "Name") else "Unbekannt"

        # Initialisiere die Fläche für jedes Geschoss
        if storey_name not in geschoss_flaechen:
            geschoss_flaechen[storey_name] = 0

        # Räume über IfcRelAggregates finden
        spaces = []
        if storey.IsDecomposedBy:
            for rel in storey.IsDecomposedBy:
                if rel.is_a("IfcRelAggregates"):
                    spaces.extend(rel.RelatedObjects)

        print(f"DEBUG: Geschoss {storey_name} hat {len(spaces)} Räume.")

        for space in spaces:
            if space.is_a("IfcSpace"):
                room_name = space.Name if hasattr(space, "Name") else "Unbenannter Raum"
                area = 0

                # Fläche aus Property-Set extrahieren
                for property_set in space.IsDefinedBy:
                    if property_set.is_a("IfcRelDefinesByProperties"):
                        props = property_set.RelatingPropertyDefinition
                        if props.is_a("IfcPropertySet"):
                            for prop in props.HasProperties:
                                if prop.Name in FLAECHE_NAMEN:
                                    area_value = getattr(prop.NominalValue, 'wrappedValue', 0)
                                    if isinstance(area_value, str):
                                        area_value = area_value.replace("m²", "").strip()
                                    try:
                                        area = float(area_value)
                                    except ValueError:
                                        area = 0
                                    break

                print(f"DEBUG: Raum {room_name} im Geschoss {storey_name} hat Fläche: {area}")

                # Raumdetails zur Liste hinzufügen
                raum_liste.append({
                    "Bezeichnung": f"{storey_name} - {room_name}",
                    "Fläche": area
                })

                # Fläche zum Geschoss addieren
                geschoss_flaechen[storey_name] += area
                print(f"DEBUG: Aktuelle Gesamtfläche für Geschoss {storey_name}: {geschoss_flaechen[storey_name]}")

    # Summierte Flächen pro Geschoss in eine Liste umwandeln
    geschoss_auflistung = [{"Bezeichnung": storey_name, "Fläche": total_area}
                           for storey_name, total_area in geschoss_flaechen.items()]

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