def split_text(text: str, chunk_size: int = 500) -> list[str]:
    words = text.split()

    chunks = []
    current_chunk = ""

    for word in words:

        # Si añadir esta palabra supera el tamaño máximo
        if len(current_chunk) + len(word) + 1 > chunk_size:

            if current_chunk:
                chunks.append(current_chunk)

            current_chunk = word

        else:
            if current_chunk:
                current_chunk += " " + word
            else:
                current_chunk = word

    # Añadir el último fragmento
    if current_chunk:
        chunks.append(current_chunk)

    return chunks