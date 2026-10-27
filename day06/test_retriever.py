# from retriever import load_documents
from retriever import retrieve, retrieve_based_on_embedding

# documents = load_documents()

# for name, text in documents.items():
#     print(name)
#     print(text)
#     print("-"*40)


#here if we are something else like "status code" so it will return None because it is searching only for exact words not for meaning
# filename, content = retrieve("Codes") 
# print(filename)
# print()
# print(content)

retrieved_dict = retrieve_based_on_embedding("amazon") 
print(retrieved_dict["filename"])
print()
print(retrieved_dict["content"])
