import re


def chunk_text(
    text: str,
    chunk_size: int = 700,
    overlap: int = 100
):
    """
    Splits document text into meaningful overlapping chunks.

    The chunker tries to preserve paragraphs and sentences
    instead of cutting text in the middle of a word.
    """

    # ----------------------------------------------
    # Clean the text
    # ----------------------------------------------

    text = re.sub(r"\s+", " ", text).strip()

    if not text:
        return []


    # ----------------------------------------------
    # Split into sentences
    # ----------------------------------------------

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text
    )


    chunks = []
    current_chunk = ""


    # ----------------------------------------------
    # Build chunks from complete sentences
    # ----------------------------------------------

    for sentence in sentences:

        sentence = sentence.strip()

        if not sentence:
            continue


        # If adding this sentence stays within the
        # target size, keep building the chunk.

        if (
            len(current_chunk) + len(sentence) + 1
            <= chunk_size
        ):

            if current_chunk:

                current_chunk += " " + sentence

            else:

                current_chunk = sentence


        else:

            # Save the current chunk

            if current_chunk:

                chunks.append(
                    current_chunk.strip()
                )


            # --------------------------------------
            # Create overlap from the previous chunk
            # --------------------------------------

            if overlap > 0 and current_chunk:

                overlap_text = current_chunk[
                    -overlap:
                ]

                current_chunk = (
                    overlap_text + " " + sentence
                )

            else:

                current_chunk = sentence


    # ----------------------------------------------
    # Add final chunk
    # ----------------------------------------------

    if current_chunk:

        chunks.append(
            current_chunk.strip()
        )


    return chunks