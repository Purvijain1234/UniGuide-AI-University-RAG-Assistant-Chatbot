import fitz

def load_pdf(uploaded_file):
    """
    Read PDF and keep page numbers.
    """
    document = fitz.open(
        stream=uploaded_file.read(),
        filetype="pdf"
    )
    pages = []
    for page_number, page in enumerate(document):
        text = page.get_text()
        # Clean text
        text = text.replace("-\n", "")
        text = text.replace("\n", " ")
        text = " ".join(text.split())
        
        if text.strip():
            pages.append(
                {
                    "page": page_number + 1,
                    "text": text
                }
            )
    return pages
