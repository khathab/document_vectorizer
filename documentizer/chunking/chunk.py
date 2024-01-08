# how can we split the PDF into various pieces

# receive input stream or entire file
    # chunk equal size
    # chunk by disimiliarity
    # chunk

from datetime import datetime
import pypdf
from ..types import Document, Chunk
import logging

logger = logging.getLogger()
# chunking model should abstract chunking types
    # even-chunking
    # disimiliarity chunking
    # other chunking methods
# could also include post processing
class Chunker:

    def __init__(self, chunk_size) -> None:
        self.chunk_size = chunk_size

    def get_text(self, path):
        pdf = pypdf.PdfReader(path)
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
        return text

    def chunk_evenly(self, path):
        pdf = pypdf.PdfReader(path)
        date = pdf.metadata.get('/CreationDate', None)
        if date:
            # remove prefix D: and Z ex. D:20230803000729Z
            date = date[2:-1]
            date = datetime.strptime(date, '%Y%m%d%H%M%S')
        else:
            date = datetime.utcnow()
        document = Document(date_created=date)
        chunks = []
        chunks.append(Chunk(document_id=document.document_id,text='Document Start', page_number=1))
        for page_number, page in enumerate(pdf.pages, start=1):
            # for image in page.images:
            #     with open(f'{image.name}', 'wb') as file:
            #         file.write(image.data)

            page_text = page.extract_text()
            # doubly link previous and next chunks
            for i in range(0, len(page_text), self.chunk_size):
                text = page_text[i:i+self.chunk_size]
                current_chunk = Chunk(document_id=document.document_id,page_number=page_number,text=text,previous_chunk_id=chunks[-1].chunk_id)
                chunks[-1].next_chunk_id = current_chunk.chunk_id
                chunks.append(current_chunk)
                logger.debug(f'Created chunk: {current_chunk}')
        return document, chunks
