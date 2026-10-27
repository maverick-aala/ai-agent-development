from pathlib import Path
from similarity import cosine_similarity
from test_embedding import get_embedding_vector

# Preparing knwoledge base from all .txt files
def load_documents():
    documents = {}
    folder = Path("day06/knowledge")
    for  file in folder.glob("*.txt"):
        documents[file.name] = file.read_text(
            encoding="utf-8"
        )
    return documents


# Keyword based retriever
def retrieve(question):
    documents = load_documents()
    question = question.lower()
    for filename, content in documents.items():
        if question in content.lower():
            return filename, content
    return None, None

# Embedding based retriever
def retrieve_based_on_embedding(question):
    documents = load_documents()
    question = question.lower()
    max_similarity_score = {"filename": "", "content": "", "score": 0}
    for filename, content in documents.items():
        question_embedding, content_embedding = get_embedding_vector(question, content)
        similarity = cosine_similarity(question_embedding, content_embedding)
        print(similarity)
        if (similarity > max_similarity_score["score"]):
            max_similarity_score = {"filename": filename, "content": content, "score": similarity}
    return max_similarity_score
