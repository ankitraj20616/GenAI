from google import genai

GEMINI_API_KEY = "GEMINI_API_KEY"

if __name__ == "__main__":
    client = genai.Client(api_key= GEMINI_API_KEY)

    response = client.models.generate_content(
        model= "gemini-2.5-flash", contents = "What is array, explain inshort",
    )

    print(response.text)