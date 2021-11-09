#añadir columnas identificativa de producto 
def modelo(a):
    if "winflo" in str(a).lower():
        return "az winflo"
    elif "in-season" in str(a).lower():
        return "in-season"
    elif "air zoom pegasus" in str(a).lower():
        return "pegasus"
    elif "air zoom structure " in str(a).lower():
        return "az structure"
    elif "air max" in str(a).lower():
        return "air max"
    elif "flex experience" in str(a).lower():
        return "flex experience"
    elif "lunar" in str(a).lower():
        return "lunar running"
    elif "sb " in str(a).lower():
        return "sb skate"
    elif "court" in str(a).lower():
        return "court tennis"
    elif "basket" in str(a).lower():
        return "basketball"
    elif "racer" in str(a).lower():
        return "racing"
    else:
        return "others"
# precio      
def limpiamos_precio(x):
    split = x.split("$")
    if len(split) >1:
        return split[1]
    else:
        return x