import ijson
from pymongo import MongoClient
from decimal import Decimal

# Sostituisci con le tue credenziali effettive
client = MongoClient("mongodb://root:password@localhost:27017/")
db = client["real-estate"]  # Sostituisci con il nome del tuo database
collection = db["comuni2"]  # Sostituisci con il nome della tua collezione

def convert_decimal_to_float(obj):
    """
    Converte ricorsivamente i valori Decimal in float.
    """
    if isinstance(obj, list):
        return [convert_decimal_to_float(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimal_to_float(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        return obj

def process_geojson(filename):
    """
    Legge un file GeoJSON come un array di oggetti e inserisce ciascun oggetto JSON in MongoDB.
    """
    with open(filename, 'r', encoding='utf-8') as f:  # Specifica la codifica UTF-8
        # Utilizza ijson per analizzare il file in modo incrementale
        objects = ijson.items(f, 'item')
        for obj in objects:
            try:
                # Converte tutti i Decimal in float
                obj = convert_decimal_to_float(obj)
                # Inserisce l'oggetto JSON nella collezione MongoDB
                collection.insert_one(obj)
            except Exception as e:
                print(f"Errore durante l'inserimento: {e}")

if __name__ == "__main__":
    geojson_file = "output3_utf8.geojson"  # Sostituisci con il percorso del tuo file
    process_geojson(geojson_file)
    print("Feature inserite con successo!")
