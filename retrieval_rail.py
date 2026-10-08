import os
import re
from chunking import cortar_en_chunks, CARPETA

# --- Palabras clave que indican una posible instruccion oculta / prompt injection ---
PALABRAS_SOSPECHOSAS = [
    "ignora todas las reglas",
    "ignora las instrucciones",
    "instruccion oculta",
    "a partir de ahora",
]

# --- Patrones que indican datos sensibles (version simple con expresiones regulares) ---
PATRON_DNI = re.compile(r"DNI:\s*\d{7,8}")
PATRON_SUELDO = re.compile(r"sueldo:\s*\$?\d+(\.\d+)?", re.IGNORECASE)


def detectar_instruccion_oculta(texto):
    texto_lower = texto.lower()
    for palabra in PALABRAS_SOSPECHOSAS:
        if palabra in texto_lower:
            return True
    return False


def enmascarar_datos_sensibles(texto):
    texto_limpio = PATRON_DNI.sub("DNI: [DATO OCULTO]", texto)
    texto_limpio = PATRON_SUELDO.sub("sueldo: [DATO OCULTO]", texto_limpio)
    return texto_limpio


def retrieval_rail(chunk_texto):
    """
    Revisa un chunk y devuelve una decision:
    - 'bloqueado': el chunk completo se descarta (riesgo de instruccion oculta)
    - 'enmascarado': el chunk se deja pasar pero con los datos sensibles tapados
    - 'permitido': el chunk pasa sin cambios
    """
    if detectar_instruccion_oculta(chunk_texto):
        return "bloqueado", None

    if PATRON_DNI.search(chunk_texto) or PATRON_SUELDO.search(chunk_texto):
        texto_seguro = enmascarar_datos_sensibles(chunk_texto)
        return "enmascarado", texto_seguro

    return "permitido", chunk_texto


def main():
    for nombre_archivo in sorted(os.listdir(CARPETA)):
        ruta = os.path.join(CARPETA, nombre_archivo)
        with open(ruta, "r", encoding="utf-8") as f:
            texto = f.read()

        chunks = cortar_en_chunks(texto)
        print(f"\n=== {nombre_archivo} ===")

        for i, chunk in enumerate(chunks):
            decision, resultado = retrieval_rail(chunk)
            print(f"\n[chunk {i}] -> DECISION: {decision.upper()}")
            if decision == "bloqueado":
                print("   (este chunk NO llega al modelo)")
            else:
                print(f"   texto final: {resultado}")


if __name__ == "__main__":
    main()
