# Chat with LLM by saving context

from google import genai
from LLM import GEMINI_API_KEY

if __name__ == "__main__":
    client = genai.Client(api_key= GEMINI_API_KEY)

    chat = client.chats.create(model = "gemini-2.5-flash")
    

    # response = chat.send_message("Hi, I am Ankit.")
    # print(response.text)

    # response = chat.send_message("How are you?")
    # print(response.text)

    # response = chat.send_message("What is my name?")
    # print(response.text)

    # for message in chat.get_history():
    #     print(f"role - {message.role}", end= " ")
    #     print(message.parts[0].text)

    print("--- Chat Started (Type 'exit' or 'quit' to stop) ---")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Tata!")
            break
        try:
            response = chat.send_message(user_input)
            print(f"Gemini: {response.text}")
        except Exception as e:
            print(f"An error occured: {e}!")