from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pinecone import Pinecone

load_dotenv()

client = genai.Client(api_key= os.getenv("GOOGLE_API_KEY"))

def transform_query(question, chat_history):
    if not chat_history:
        return question
    prompt = f"""Chat History:{
                chat_history}
                Follow up user Question: {question}
            """
    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents= prompt,
        config= types.GenerateContentConfig(
            system_instruction= f"""
                You are a query rewritter expert.Based on provided chat history, rephrase the "Follow up user Question" into a complete , standalone question that can understood without the chat history.
                Only output the rewritten question and nothing else.
            """
        )
    )
    return response.text

def chat(user_input, history_list):
    # Convert this user query into vector
    user_input = transform_query(user_input, history_list)
    embeddings = GoogleGenerativeAIEmbeddings(model= "models/embedding-001")
    query_vector = embeddings.embed_query(user_input)
    
    # Make connection with pinecone
    index = os.getenv("PINECONE_INDEX_NAME")
    pinecone = Pinecone()
    pinecone_index = pinecone.Index(index)
    search_result = pinecone_index.query(top_k=10, vector= query_vector, include_metadata= True)
    
    # Now we have top 10 related vextors now we will create context for LLM from this
    context_parts = []
    for match in search_result["matches"]:
        text_content = match.get("metadata", {}).get("text")
        if text_content:
            context_parts.append(text_content)
    context = "\n\n---\n\n".join(context_parts)


    # Give this to LLM
    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents= user_input,
        config= types.GenerateContentConfig(
            system_instruction= f"""
                You have to behave like a Data Structure and Algorithm Expert.
                You will give content of relevant information and user question.
                Your task is to answer user's question based ONLY on the provided context.
                If the answer is not in the context, you must say "I could not find the answer in the provided document".
                Keep your answer clear, consice and educaitonal.
                Context: {context}
            """
        )
    )
    return response.text

def main():
    print("-----------Start Chating with my RAG--------")
    history_list = []
    while True:
        user_input = input("You: ")
        if user_input.lower() in ("quit", "exit"):
            print("Bye!")
            break 
        
        response = chat(user_input, history_list)
        history_list.append(f"User: {user_input}")
        history_list.append(f"Gemini: {response}")
        
        print(f"Gemini:- {response}")

if __name__ == "__main__":
    main()
    