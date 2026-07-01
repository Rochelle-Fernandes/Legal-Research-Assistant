import fitz #lib for pymuPDF for pdf to img 


def get_page_count(pdf_file):

    pdf_file.seek(0) # Moves back to the beginning of the file before reading

    doc = fitz.open(
        stream=pdf_file.read(),
        filetype="pdf"
    )

    return len(doc)


def get_first_page_text(pdf_file):

    pdf_file.seek(0)

    doc = fitz.open(
        stream=pdf_file.read(),
        filetype="pdf"
    )

    first_page = doc[0]

    return first_page.get_text()


def extract_all_pages(pdf_file):

    pdf_file.seek(0)

    doc = fitz.open(
        stream=pdf_file.read(),
        filetype="pdf"
    )

    pages = []

    for page_num in range(len(doc)):

        page = doc[page_num]

        pages.append(
            {
                "page": page_num + 1,
                "text": page.get_text()
            }
        )

    return pages


def is_scanned_pdf(pdf_file):

    pdf_file.seek(0)

    doc = fitz.open(
        stream=pdf_file.read(),
        filetype="pdf"
    )

    if len(doc) == 0:
        return True

    first_page_text = doc[0].get_text().strip()

    if len(first_page_text) < 50: # If no. of char extracted below 50 then it is scanned pdf 
        return True

    return False