import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Constants
AVAILABLE_MODELS = [
    "gemini-3.1-flash-lite",        # 500/day
    "gemini-3.5-flash",             # 20/day
    "gemini-2.5-flash",             # 20/day
    "gemini-2.5-flash-lite",        # 20/day
]

def show_help_menu():
    print("\n---------- Help Menu ----------")
    print("    /help                : Shows this help menu")
    print("    /status              : Shows the current active configuration")
    print("    /temp <0.0 - 2.0>    : Sets the temperature value>")
    print("    /max <int>           : Set the maximum output tokens value")
    print("    /model <int>         : Sets the model (and shows list)")
    print("    /exit or /quit       : Ends the session")
    print("    /clear               : Clears the conversation history")
    print("-------------------------------\n")

def show_models_menu():
    print("\n---------- Models Menu ----------")
    for idx, model in enumerate(AVAILABLE_MODELS, start=1):
        print(f"   {idx}   {model}")
    print("---------------------------------\n")

def show_status_menu(current_model, temperature, max_output_tokens, history_length):
    print("\n---------- Status Menu ----------")
    print(f"    Model               : {current_model}")
    print(f"    Temperature         : {temperature}")
    print(f"    Max Output Tokens   : {max_output_tokens}")
    print(f"    Conversation Length : {history_length} messages")
    ## what other things to add??
    print("---------------------------------\n")

def initialize_client():
    load_dotenv()
    if not os.getenv("GEMINI_API_KEY"):
        print("System Error: GEMINI_API_KEY not found. Please check your .env file.")
        exit(1)
    return genai.Client()

def main():
    client = initialize_client()

    print("\nGemini Chatbot Initialized! Type /exit or /quit to end the conversation.\n")

    current_model = "gemini-3.1-flash-lite"
    temperature = 0.0
    max_output_tokens = 1024
    
    history=[]

    while True:
        user_input = input("You: ")
        clean_user_input = user_input.strip()
        if not clean_user_input:
            continue
        if clean_user_input.startswith("/"):
            parts = clean_user_input.split()
            command = parts[0].lower()
            args = parts[1:]
            if command in ["/quit", "/exit"]:
                print(f"\nGemini: Goodbye!")
                break

            elif command == "/status":
                show_status_menu(current_model, temperature, max_output_tokens, len(history))
                continue

            elif command == "/model":
                if len(args)==0:
                    print(f"\nPlease input a valid number to select a model between 1 and {len(AVAILABLE_MODELS)}.")
                    show_models_menu()
                    continue
                elif len(args) == 1:
                    try:
                        model_nb = int(args[0]) -1
                        if model_nb < 0 or model_nb >= len(AVAILABLE_MODELS):
                            print(f"\nPlease input a valid number to select a model between 1 and {len(AVAILABLE_MODELS)}.\n")
                            continue

                        current_model = AVAILABLE_MODELS[model_nb]
                        print(f"\nSystem Success: Model set to {current_model}.\n")
                        continue
            
                    except ValueError:
                        print(f"\nPlease input a valid number to select a model between 1 and {len(AVAILABLE_MODELS)}.\n")
                        continue

            elif command == "/temp":
                if len(args) == 0:
                    print("\nPlease input a temperature value between 0.0 and 2.0 (low = factual, high = creative).\n")
                    continue
                elif len(args) == 1:
                    try:
                        temp_val = float(args[0])
                        if temp_val < 0 or temp_val > 2.0:
                            print("\nPlease input a temperature value between 0.0 and 2.0 (low = factual, high = creative).\n")
                            continue
                        temperature = temp_val
                        print(f"\nSystem Success: Temperature value set to {temperature}.\n")
                        continue
                    except ValueError:
                        print("\nPlease input a temperature value between 0.0 and 2.0 (low = factual, high = creative).\n")
                        continue

            elif command == "/max":
                if len(args) == 0: 
                    print("\nPlease input a positive integer value for maximum output tokens.\n")
                    continue
                elif len(args) == 1:
                    try:
                        max_val = int(args[0])
                        if max_val <=0:
                            print("\nPlease input a positive integer value for maximum output tokens.\n")
                            continue  
                        max_output_tokens = max_val
                        print(f"\nSystem Success: Maximum Output Tokens set to {max_output_tokens}.\n")
                        continue
                    except ValueError:
                        print("\nPlease input a positive integer value for maximum output tokens.\n")
                        continue

            elif command == "/clear":
                history = []
                print("\nConversation History Completely Cleared!\n")
                continue

            elif command == "/help":
                show_help_menu()
                continue

        else:
            history.append({
                "role":"user",
                "parts":[{"text": clean_user_input}]
            })

            try:
                config = types.GenerateContentConfig(
                    temperature = temperature,
                    max_output_tokens = max_output_tokens,
                )

                response_stream = client.models.generate_content_stream(
                    model = current_model,
                    contents = history,
                    config = config
                )
                print("\nGemini: ", end="", flush=True)
                full_response=""

                for chunk in response_stream:
                    if chunk.text: #skip empty chunks
                        print(chunk.text, end="", flush=True)
                        full_response+=chunk.text
                print("\n") #print an empty line when done outputting

                if full_response:
                    history.append({
                        "role":"model",
                        "parts": [{"text": full_response}]
                    })
                
                else:
                    print("System: Model returned no text.")

            except Exception as e:
                print(f"API Error: {e}")
                history.pop() #remove user message that caused the error
                continue


if __name__ == "__main__":
    main()
