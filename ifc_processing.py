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

def process_bgf_berechnung_detailliert(ifc_file_path):
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
    model = ifcopenshell.open(ifc_file_path)

    raum_liste = []
    geschoss_volumen = {}

    print("Beginne die Verarbeitung der IfcBuildingStoreys für Kubische Berechnung...")

    for storey in model.by_type("IfcBuildingStorey"):
        storey_name = storey.Name if hasattr(storey, "Name") else "Unbekannt"

        geschoss_volumen[storey_name] = 0

        spaces = storey.IsDecomposedBy[0].RelatedObjects if storey.IsDecomposedBy else []

        for space in spaces:
            room_name = space.Name if hasattr(space, "Name") else "Unbenannter Raum"
            volume = getattr(space, "Volume", 0)

            print(f"Raum: {room_name}, Geschoss: {storey_name}, Volumen: {volume}")
            raum_liste.append({
                "Bezeichnung": f"{storey_name} - {room_name}",
                "Volumen": volume
            })
            geschoss_volumen[storey_name] += float(volume) if isinstance(volume, (int, float)) else 0

    geschoss_auflistung = [{"Bezeichnung": f"{storey_name}", "Volumen": total_volume}
                           for storey_name, total_volume in geschoss_volumen.items()]

    return raum_liste, geschoss_auflistung