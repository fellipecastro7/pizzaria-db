from datetime import datetime

def formatar_data_hora():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")