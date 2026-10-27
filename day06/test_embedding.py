# will test actual embedding model nomic-embed-text
import os
from openai import OpenAI
from dotenv import load_dotenv
from similarity import cosine_similarity

# load configurations from the .env file
load_dotenv()

#create a cleint that communicates with ollama (AI Model)
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

def get_embedding_vector(question, content):
   question_embedding = client.embeddings.create(
      model=os.getenv("EMBEDDING_MODEL"),
      input=question
    ).data[0].embedding
   
   content_embedding = client.embeddings.create(
      model=os.getenv("EMBEDDING_MODEL"),
      input=content
    ).data[0].embedding

   return question_embedding, content_embedding
 


response1 = client.embeddings.create(
    model=os.getenv("EMBEDDING_MODEL"),
    input="Python"
 
)

response2 = client.embeddings.create(
    model=os.getenv("EMBEDDING_MODEL"),
 
     input="Language"
)

embedding1 = response1.data[0].embedding
embedding2 = response2.data[0].embedding




