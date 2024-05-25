ALPHA_LEVEL = 128

def convert_byte(byte):
    if byte < 1024:
        return f"{byte}B"
    elif byte < 1024**2:
        return f"{byte/1024:.2f}KB"
    elif byte < 1024**3:
        return f"{byte/(1024**2):.2f}MB"
    else:
        return f"{byte/(1024**3):.2f}GB"