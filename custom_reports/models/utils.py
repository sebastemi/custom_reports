import re

def extract_data(text: str, return_ot: bool) -> str:
    """
    Extrae la OT o el nombre del cliente de una cadena de texto.
    """
    # Regex: Captura "OT-algo", luego ignora espacios y el guion, y captura el resto.
    patron = r'^(OT-[\w]+)\s*-\s*(.*)$'
    match = re.match(patron, text, re.IGNORECASE)
    
    if not match:
        return "Formato inválido"
        
    if return_ot:
        return match.group(1) # Devuelve la OT
    else:
        return match.group(2) # Devuelve el nombre del cliente