def split_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 100
) -> list[str]:

    words = text.split()

    if not words:
        return []

    if overlap >= chunk_size:
        raise ValueError(
            "overlap debe ser menor que chunk_size"
        )

    chunks = []

    start = 0

    while start < len(words):

        current_chunk = []
        current_length = 0

        for i in range(start, len(words)):

            word = words[i]

            new_length = (
                current_length
                + len(word)
                + (1 if current_chunk else 0)
            )

            if new_length > chunk_size:
                break

            current_chunk.append(word)
            current_length = new_length

        if not current_chunk:
            current_chunk.append(words[start])

        chunk = " ".join(current_chunk)
        chunks.append(chunk)

        consumed_words = len(current_chunk)

        if start + consumed_words >= len(words):
            break

        overlap_length = 0
        overlap_words = 0

        for word in reversed(current_chunk):

            additional_length = (
                len(word)
                + (1 if overlap_words else 0)
            )

            if overlap_length + additional_length > overlap:
                break

            overlap_length += additional_length
            overlap_words += 1

        start = start + consumed_words - overlap_words

    return chunks

