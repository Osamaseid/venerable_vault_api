from . import models

def calculate_value(base_cost: float, age_category: str, documents_count: int) -> tuple:
    """
    Calculate the valuation based on base cost, age category, and documentation.
    Returns (calculated_value, multiplier_used)
    """
    multiplier = 1.0

    age_multipliers = {
        "antique": 1.5,
        "vintage": 1.2,
        "modern": 1.0,
        "contemporary": 0.9
    }
    
    age_multiplier = age_multipliers.get(age_category.lower(), 1.0)
    multiplier += age_multiplier
    
    if documents_count >= 5:
        multiplier += 0.5
    elif documents_count >= 3:
        multiplier += 0.3
    elif documents_count >= 1:
        multiplier += 0.1
    
    calculated_value = round(base_cost * multiplier, 2)
    return calculated_value, round(multiplier, 2)