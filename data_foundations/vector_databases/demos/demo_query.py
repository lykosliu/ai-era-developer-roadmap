# demo_query.py: Simple Vector Search with ChromaDB

import chromadb
from chromadb.utils import embedding_functions

def run_demo():
    # 1. Initialize an in-memory ChromaDB client
    client = chromadb.Client()

    # 2. Define a simple embedding function (using a default local model)
    default_ef = embedding_functions.DefaultEmbeddingFunction()

    # 3. Create a collection (similar to a table)
    collection = client.create_collection(name="ai_knowledge", embedding_function=default_ef)

    # 4. Add documents with their IDs
    documents = [
        "LLMs (Large Language Models) are trained on massive amounts of text data.",
        "Prompt Engineering is the art of crafting inputs to get better outputs.",
        "Vector databases store numerical representations of semantic meaning.",
        "RAG (Retrieval-Augmented Generation) connects LLMs to external data.",
        "Agents are autonomous systems that use LLMs to perform complex tasks."
    ]
    ids = [f"doc_{i}" for i in range(len(documents))]

    print("Adding documents to the vector database...")
    collection.add(documents=documents, ids=ids)

    # 5. Perform a semantic query
    query = "How can I make AI remember more context?"
    print(f"\nSearching for query: '{query}'")

    results = collection.query(query_texts=[query], n_results=2)

    # 6. Display the top 2 results
    print("\nTop 2 most relevant results:")
    for i, doc in enumerate(results['documents'][0]):
        print(f"{i+1}. {doc}")

if __name__ == "__main__":
    run_demo()
