import unittest
from ..documentizer.chunking import Chunker
from unittest import TestCase

class TestChunks(TestCase):

    def test_chunk():
        try:
            path = r'document_vectorizer\test\Kids_Story.pdf'
            chunker = Chunker(300)
            chunks = chunker.chunk_evenly(path)
            print(chunks)
        except Exception as e:
            print(f"{e}")

if __name__ == "__main__":
    unittest.main()