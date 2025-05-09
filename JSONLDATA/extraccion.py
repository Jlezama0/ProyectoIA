import json

# Archivo de entrada y salida
archivo_jsonl = 'prueba.jsonl'
archivo_salida = 'respuestas_extraidas.txt'

with open(archivo_jsonl, 'r', encoding='utf-8') as entrada, open(archivo_salida, 'w', encoding='utf-8') as salida:
    for linea in entrada:
        try:
            datos = json.loads(linea)
            # Buscar contenido con rol "user"
            for contenido in datos.get("contents", []):
                if contenido.get("role") == "model":
                    for parte in contenido.get("parts", []):
                        if "text" in parte:
                            pregunta = parte["text"].strip()
                            salida.write(pregunta + '\n')
        except json.JSONDecodeError:
            print("Línea con formato inválido, se omite.")
