from documentizer import Documentizer

def main(documents):
    knowledge_base = Documentizer()
    for document in documents:
        knowledge_base.add_document(document)

    while True:
        search_query = input('Question: ')
        result = knowledge_base.search_documents(search_query)
        print(f"Answer:: {result}")

if __name__ == "__main__":
    documents = [r'documents\1706.03762.pdf', r'documents\Q123_Shareholders_Report-EN.pdf', r'documents\M14-3048 E.pdf']
    main(documents)

