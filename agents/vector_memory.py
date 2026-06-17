import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(
    path="vector_store/chromadb"
)

collection = client.get_or_create_collection(
    "articles"
)

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def remember_article(
        title,
        content
):

    embedding = model.encode(
        content
    ).tolist()

    collection.add(
        ids=[title],
        documents=[content],
        embeddings=[embedding]
    )


def retrieve_similar_articles(
        query,
        limit=3
):

    embedding = model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[embedding],
        n_results=limit
    )

    return results