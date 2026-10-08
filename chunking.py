import os

CARPETA = "documentos"

def cortar_en_chunks(texto):
    """Corta el texto en chunks separando por parrafos (lineas en blanco)."""
    partes = texto.split("\n\n")
    # Limpiamos espacios extra y descartamos partes vacias
    chunks = [p.strip() for p in partes if p.strip()]
    return chunks

def main():
    todos_los_chunks = []

    for nombre_archivo in os.listdir(CARPETA):
        ruta = os.path.join(CARPETA, nombre_archivo)
        with open(ruta, "r", encoding="utf-8") as f:
            texto = f.read()

        chunks = cortar_en_chunks(texto)

        print(f"\n=== {nombre_archivo} -> {len(chunks)} chunks ===")
        for i, chunk in enumerate(chunks):
            print(f"\n[chunk {i}]")
            print(chunk)
            todos_los_chunks.append({
                "origen": nombre_archivo,
                "indice": i,
                "texto": chunk
            })

    return todos_los_chunks

if __name__ == "__main__":
    main()
