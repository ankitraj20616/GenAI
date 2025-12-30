# Chat with LLM by saving context

from google import genai
from google.genai import types

GEMINI_API_KEY = "YOUR_API_KEY"


if __name__ == "__main__":
    client = genai.Client(api_key= GEMINI_API_KEY)
    sys_instuction = """*   **Health and Food:** The conversation starts with Ankit asking what his partner ate, to which she replies she hasn't eaten since yesterday afternoon and feels very bad. Ankit expresses strong concern, urging her to eat for energy, and she eventually manages to eat a little khichdi.
*   **Rest and Sleep:** They discuss resting to feel better, but she's worried about sleeping during the day and disturbing her night sleep schedule. Ankit prioritizes her health over sleep routine for now.
*   **Study Plans:** Both have plans to study. She mentions she'll rest and then study, and Ankit advises her to study only if she feels up to it.
*   **Playful Banter:** They share some lighthearted moments, discussing the khichdi with ghee and Ankit wishing he could have some, leading to playful talk about marriage and her making him press her feet (which she refuses).
*   **Annoying Calls:** She complains about receiving many persistent calls from unknown numbers, even after blocking them, and mentions her uncle wanted her to go to the market in the fog.
*   **Gaming Session:** They play a game (carrom/ludo), and Ankit hilariously complains about her repeatedly winning ("Kutti sb jagah hara dii"). They plan to play again later when his game limit resets.
*   **Study Preparations:** They both decide to start studying. She needs to recharge her phone data, and they discuss using a laptop for 
code and phone for documents.
*   **Affectionate Closing:** The chat ends with affectionate messages, "Love you"s, and emojis, with Ankit reminding her not to sleep now so she can sleep at night. There's also a brief mention of a reel sent in a group chat."""

    chat = client.chats.create(
        model = "gemini-2.5-flash",
        config= types.GenerateContentConfig(
            system_instruction= sys_instuction
        )
    )
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