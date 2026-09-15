import pdfplumber

def extract_text_from_pdf(pdf_path):
    text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


if __name__ == "__main__":
    text = extract_text_from_pdf("sample.pdf")

    if text.strip():
        print("PDF TEXT FOUND:")
        print(text[:2000])
    else:
        print("NO TEXT FOUND IN PDF")