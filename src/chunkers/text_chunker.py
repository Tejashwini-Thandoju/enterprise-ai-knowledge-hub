def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100):
    """
    Splits text into overlapping chunks.

    Parameters:
        text: Complete document text
        chunk_size: Maximum characters per chunk
        overlap: Number of overlapping characters

    Returns:
        List of text chunks
    """

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunks.append(text[start:end])

        start += chunk_size - overlap

    return chunks