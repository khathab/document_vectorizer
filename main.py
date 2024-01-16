from documentizer import Documentizer

def main(path):
    knowledge_base = Documentizer()
    #vectorizer.add_document(path)

    while True:
        search_query = input('Question: ')
        result = knowledge_base.search_documents(search_query)
        print(f"Answer:: {result}")

if __name__ == "__main__":
    path = r'documents\1706.03762.pdf'
    main(path)

