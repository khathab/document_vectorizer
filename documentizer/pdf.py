import pypdf

def get_text(path):
    pdf = pypdf.PdfReader(path)
    text = ''
    for page in pdf.pages:
        text += page.extract_text()
    return text

def extract_chunks(path):
    pdf = pypdf.PdfReader(path)
    processed_paragraphs = []
    for page in pdf.pages:
        for image in page.images:
            with open(f'{image.name}', 'wb') as file:
                file.write(image.data)
        text = page.extract_text()
        paragraphs = text.split('\n')
        current_paragraph = ""
        for paragraph in paragraphs:
            # add paragraph to list
            if len(paragraph) > 500:
                processed_paragraphs.append(paragraph)
            else:
                current_paragraph += '\n'+ paragraph
                if len(current_paragraph) > 500:
                    processed_paragraphs.append(current_paragraph)
                    current_paragraph = ''
    return processed_paragraphs
