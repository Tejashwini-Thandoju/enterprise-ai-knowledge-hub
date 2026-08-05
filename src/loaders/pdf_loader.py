from pypdf import PdfReader


def load_pdf(file_path: str) -> str:
    """
    Reads a PDF file and returns all extracted text.
    """

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        extracted_text = page.extract_text()

        if extracted_text:
            text += extracted_text + "\n"

    return text


if __name__ == "__main__":
    pdf_text = load_pdf("data/raw/HR_Policy.pdf")
    print(pdf_text)