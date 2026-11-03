"""Day 06 — Load knowledge .txt files; keyword or embedding retrieval."""

from pathlib import Path
from similarity import cosine_similarity
from test_embedding import get_embedding_vector


def load_documents():
    """Read all *.txt under day06/knowledge into {filename: text}."""
    documents = {}
    folder = Path("day06/knowledge")
    for file in folder.glob("*.txt"):
        documents[file.name] = file.read_text(encoding="utf-8")
    return documents


def retrieve(question):
    """Keyword match: first document whose body contains the question substring."""
    documents = load_documents()
    question = question.lower()
    for filename, content in documents.items():
        if question in content.lower():
            return filename, content
    return None, None


def retrieve_based_on_embedding(question):
    """Pick document with highest cosine similarity between question and full document embeddings."""
    documents = load_documents()
    question = question.lower()
    max_similarity_score = {"filename": "", "content": "", "score": 0}
    for filename, content in documents.items():
        question_embedding, content_embedding = get_embedding_vector(question, content)
        similarity = cosine_similarity(question_embedding, content_embedding)
        print(similarity)
        if similarity > max_similarity_score["score"]:
            max_similarity_score = {
                "filename": filename,
                "content": content,
                "score": similarity,
            }
    return max_similarity_score
