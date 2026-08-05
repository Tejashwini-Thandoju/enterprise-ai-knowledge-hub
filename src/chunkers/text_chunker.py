def chunk_text(text: str, chunk_size: int = 500):
    """
    Splits text into fixed-size chunks.

    Parameters:
        text: Complete document text
        chunk_size: Maximum number of characters per chunk

    Returns:
        List of text chunks
    """

    chunks = []

    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)

    return chunks