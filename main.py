from documentizer import Documentizer

def main(path):
    vectorizer = Documentizer()
    #vectorizer.add_document(path)

    while True:
        search_query = input('Search Document: ')
        result = vectorizer.search_document(search_query)
        print(f"Result: {result.get('text',None)}")

if __name__ == "__main__":
    path = r'documents\1706.03762.pdf'
    main(path)

