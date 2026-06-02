import os
import sys
from dotenv import load_dotenv
from google import genai

# Constants
AVAILABLE_MODELS = [
    "gemini-3.1-flash-lite",        # 500/day
    "gemini-3.5-flash",             # 20/day
    "gemini-2.5-flash",             # 20/day
    "gemini-2.5-flash-lite",        # 20/day
]

def show_help_menu():
    print("\n---------- Help Menu ----------")

    print("-------------------------------\n")

def show_models_menu():
    print("\n---------- Models Menu ----------")
    for idx, model in enumerate(AVAILABLE_MODELS, start=1):
        print(f"   {idx}   {model}")
    print("---------------------------------\n")

def show_status_menu():
    print("\n---------- Status Menu ----------")

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
                show_status_menu()
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
                            print(f"\nPlease input a valid number to select a model between 1 and {len(AVAILABLE_MODELS)}.")
                            continue

                        current_model = AVAILABLE_MODELS[model_nb]
                        print(f"\nSystem Success: Model set to {current_model}.")
                        continue
            
                    except ValueError:
                        print(f"\nPlease input a valid number to select a model between 1 and {len(AVAILABLE_MODELS)}.")
                        continue

            elif command == "/temp":
                if len(args) == 0:
                    print("Please input a temperature value between 0.0 and 2.0 (low = factual, high = creative).")
                    continue
                elif len(args) == 1:
                    try:
                        temp_val = float(args[0])
                        if temp_val < 0 or temp_val > 2.0:
                            print("Please input a temperature value between 0.0 and 2.0 (low = factual, high = creative).")
                            continue
                        temperature = temp_val
                        print(f"System Success: Temperature value set to {temperature}.")
                        continue
                    except ValueError:
                        print("Please input a temperature value between 0.0 and 2.0 (low = factual, high = creative).")
                        continue
            elif command == "/max":
                if len(args) == 0: 
                    print("Please input a positive integer value for maximum output tokens.")
                    continue
                elif len(args) == 1:
                    try:
                        max_val = int(args[0])
                        if max_val <=0:
                            print("Please input a positive integer value for maximum output tokens.")
                            continue  
                        max_output_tokens = max_val
                        print(f"System Success: Maximum Output Tokens set to {max_output_tokens}.")
                        continue
                    except ValueError:
                        print("Please input a positive integer value for maximum output tokens.")
                        continue

        else:
            history.append({
                "role":"user",
                "parts":[{"text": clean_user_input}]
            })



if __name__ == "__main__":
    main()
