import os
from dotenv import load_dotenv
from langchain_community.document_loaders import JSONLoader
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone, ServerlessSpec

load_dotenv()
WORKDIR = os.getenv("WORKDIR")
os.chdir(WORKDIR)

def extract_metadata(record: dict, metadata: dict) -> dict:
    metadata["question"] = record['question']
    return metadata

def import_to_pinecone():
    # Load FAQ data
    # /Users/yogeshgoel/agentic-customer-service-medical-clinic/data/syntetic_data
    loader = JSONLoader(
        file_path=f'{WORKDIR}/faq/data.json',
        jq_schema='.[]',
        text_content=False,
        metadata_func=extract_metadata
    )
    docs = loader.load()

    # Initialize Pinecone
    pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
    
    # Create Pinecone index
    index_name = 'ovidedentalclinic'
    if index_name not in pc.list_indexes():
        pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    ) 
)
    # Initialize OpenAI embeddings
    embedding = OpenAIEmbeddings(model="text-embedding-ada-002")

    # Create and populate Pinecone vector store
    vector_store = PineconeVectorStore.from_documents(
        documents=docs,
        embedding=embedding,
        index_name=index_name
    )

    print("FAQ data successfully imported to Pinecone!")

if __name__ == "__main__":
    import_to_pinecone()