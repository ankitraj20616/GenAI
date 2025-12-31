from google import genai
from google.genai import types
import subprocess
import os
import shlex


CURRENT_DIR = os.getcwd()


def execute_command(cmd: str):
    global CURRENT_DIR

    print(f"Executing: {cmd}")

    # Handle `cd` manually
    if cmd.startswith("cd "):
        path = cmd.replace("cd ", "").strip()
        new_path = os.path.join(CURRENT_DIR, path)

        if os.path.isdir(new_path):
            CURRENT_DIR = new_path
            print(f"Changed directory to: {CURRENT_DIR}")
            return f"Changed directory to {path}"
        else:
            return f"Directory not found: {path}"

    try:
        subprocess.run(
            cmd,
            shell=True,        
            cwd=CURRENT_DIR,   
            check=True
        )
        return "Command executed successfully"

    except subprocess.CalledProcessError as e:
        return f"Command failed: {e}"
    
def write_file(path: str, content: str):
    global CURRENT_DIR
    file_path = os.path.join(CURRENT_DIR, path)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Written file: {file_path}")
    return f"{path} written successfully"
    
available_tools = {
    "command_executer": execute_command,
    "write_file": write_file
}
tools = [
    types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="command_executer",
                description="Run shell commands like mkdir, cd",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "cmd": types.Schema(type=types.Type.STRING)
                    },
                    required=["cmd"]
                )
            ),
            types.FunctionDeclaration(
                name="write_file",
                description="Write content to a file",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "path": types.Schema(type=types.Type.STRING),
                        "content": types.Schema(type=types.Type.STRING),
                    },
                    required=["path", "content"]
                )
            )
        ]
    )
]


def handle_response(chat, response):
    while response.function_calls:
        fc = response.function_calls[0]
        tool_name = fc.name
        args = fc.args

        print(f"Tool Called → {tool_name}({args})")
        result = available_tools[tool_name](**args)
        response = chat.send_message(
            types.Part.from_function_response(
                name=tool_name,
                response={"result": result}
            )
        )
    if response.text:
        print(f"\nGemini:\n{response.text}\n")
    else:
        print("\nGemini finished execution.\n")

if __name__ == "__main__":
    client = genai.Client(api_key= "AIzaSyAP61ITIsHj0N3E104D1XfJ-jAMv3qtO7Y")
    
    chat = client.chats.create(
        model = "gemini-2.5-flash",
        config= types.GenerateContentConfig(
            system_instruction= """
                You are website builder expert. You have to create the frontend of the website in htmk=l, css and js only by analysing the user input.
                You have access of tools, command_executer which can run and execute any shell or terminal command and write_file which can write into files.
                I am using call function of subprocess module of python provide command that it can execute.
                
                What is your jobs:
                1.Analyse the user query to see what type of website they want to build.
                2.Give them command one by one or step by step.
                3.Use available tool command_executer.
                # Now you can give them command in following below, like:
                Rules:
                1. Use command_executer ONLY for mkdir and cd.
                2. Use write_file to write HTML, CSS, JS files.
                3. Never use echo or cat.
                4. Always write complete, bug-free code.
                5. Create folder → cd → write index.html → write style.css → write script.js.


                provide command in form of string to the tool , and use tool to execute all commands.
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

            handle_response(chat, response)
        except Exception as e:
            print(f"Error: {e}")