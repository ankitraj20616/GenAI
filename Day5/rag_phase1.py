from dotenv import load_dotenv
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()
# print(os.getenv("PIINECONE_API"))

def load_pdf():
    file_path = os.getenv("PDF_PATH")
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    return docs

def pdf_chunking(doc):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(doc)
    return chunks

def vector_embedding(chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model= "models/embedding-001")
    texts = [doc.page_content for doc in chunks]
    vector_embeddings = embeddings.embed_documents(texts)
    return vector_embeddings



docs = load_pdf()
print("PDF loaded")
chunks = pdf_chunking(docs)
print("Chunks created")
# vectors = vector_embedding(chunks)

pinecone_index = os.getenv("PINECONE_INDEX_NAME")
embeddings = GoogleGenerativeAIEmbeddings(model= "models/embedding-001")
print("Vector embedding model configured.")
vector_store = PineconeVectorStore.from_documents(
    documents= chunks,
    embedding= embeddings,
    index_name= pinecone_index,
    batch_size= 5
)
print(f"Successfully uploaded {len(chunks)} chunks to Pinecone.")