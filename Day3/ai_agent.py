from google import genai
from google.genai import types
import requests
import math

def sum_tool(num1: int, num2: int):
    return num1 + num2

def prime_tool(num: int):
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def get_crypto_price_tool(coin: str):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "ids": coin
    }
    return requests.get(url, params= params).json()

available_tools = {
    "sum": sum_tool,
    "prime": prime_tool,
    "get_crypto_price": get_crypto_price_tool,
}

tools=[{ 
    "functionDeclarations": [
                        {
                            "name": "sum",
                            "description": "Sum of two numbers",
                            "parameters": {
                                "type": "OBJECT",
                                "properties": {
                                    "num1": {"type": "number"},
                                    "num2": {"type": "number"}
                                },
                                "required": ["num1", "num2"]
                            }
                        },
                        {
                            "name": "prime",
                            "description": "Check if number is prime",
                            "parameters": {
                                "type": "OBJECT",
                                "properties": {
                                    "num": {"type": "number"}
                                },
                                "required": ["num"]
                            }
                        },
                        {
                            "name": "get_crypto_price",
                            "description": "Get crypto price",
                            "parameters": {
                                "type": "OBJECT",
                                "properties": {
                                    "coin": {"type": "string"}
                                },
                                "required": ["coin"]
                            }
                        }
                    ]
                }]

if __name__ == "__main__":
    client = genai.Client(api_key= "YOUR_API_KEY")
    
    chat = client.chats.create(
        model = "gemini-2.5-flash",
        config= types.GenerateContentConfig(
            system_instruction= """
                You are AI agent.
                You have access of 3 tools:
                1. sum(num1, num2)
                2. prime(num)
                3. get_crypto_price(coin)
                Use tools only when required.
                Otherwise answer normally as an AI agent.
            """,
            tools= tools
        )
    )

    print("--- Chat Started (Type 'exit' or 'quit' to stop) ---")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Tata!")
            break
        try:
            response = chat.send_message(
                user_input
            )

            if response.function_calls:
                fc = response.function_calls[0]
                tool_name = fc.name
                args = fc.args
                print(f"Tool Called → {tool_name}({args})")
                result = available_tools[tool_name](**args)
                tool_response = chat.send_message(
                    genai.types.Part.from_function_response(
                        name = tool_name,
                        response= {"result": result}
                    )
                )
                print(f"Gemini: {tool_response.text}")
            else:
                print(f"Gemini: {response.text}")
        except Exception as e:
            print(f"Error: {e}")