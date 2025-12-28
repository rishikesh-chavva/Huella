def calculate_footprint(material: str, weight_kg: float) -> float:
    """
    Calculates carbon footprint based on material type and weight.
    Factors are in kg CO2e per kg of material.
    """
    factors = {
        "cotton": 2.1,
        "organic cotton": 1.0,
        "polyester": 5.5,
        "recycled polyester": 2.3,
        "linen": 1.5,
        "wool": 13.0,
        "silk": 25.0,
        "nylon": 7.5,
        "denim": 4.5,
        "leather": 17.0
    }
    
    # Clean material string for better matching
    clean_material = material.lower().strip()
    
    # Try exact match or partial match
    factor = factors.get(clean_material)
    if not factor:
        for key, val in factors.items():
            if key in clean_material:
                factor = val
                break
    
    # Default to a medium-high factor if unknown (e.g., polyester/synthetic blend average)
    if factor is None:
        factor = 5.0
        
    return round(weight_kg * factor, 2)
