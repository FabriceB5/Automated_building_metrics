import ifcopenshell

def process_kubische_berechnung(ifc_file_path):
    model = ifcopenshell.open(ifc_file_path)
    result = []
    
    for space in model.by_type("IfcSpace"):
        volume = space.Volume if hasattr(space, "Volume") else 0
        result.append({"Name": space.Name, "Volumen (m³)": volume})
    
    return result

def process_bgf_berechnung(ifc_file_path):
    model = ifcopenshell.open(ifc_file_path)
    result = []
    
    for space in model.by_type("IfcSpace"):
        area = space.Area if hasattr(space, "Area") else 0
        result.append({"Name": space.Name, "Fläche (m²)": area})
    
    return result
