from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

def chunk_text(text, chunk_size=500):

    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])

    return chunks


def create_vector_store(text):

    chunks = chunk_text(text)

    embeddings = embedding_model.encode(chunks)

    embeddings = np.array(
        embeddings,
        dtype=np.float32
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    return index, chunks


def retrieve_context(
        question,
        index,
        chunks,
        k=3
):

    query_embedding = embedding_model.encode(
        [question]
    )

    query_embedding = np.array(
        query_embedding,
        dtype=np.float32
    )

    distances, indices = index.search(
        query_embedding,
        k
    )

    context = "\n".join(
        chunks[i]
        for i in indices[0]
    )

    return context