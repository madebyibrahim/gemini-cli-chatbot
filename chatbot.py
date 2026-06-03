import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from datetime import datetime
import json

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
    print("    /save-human [file]   : Export entire conversation to human-readable .txt file")
    print("    /save-json [file]    : Export entire conversation to .json file")
    print("    /load [file]         : Load a previously exported .json conversation")
    print("-------------------------------\n")

def show_models_menu():
    print("\n---------- Models Menu ----------")
    for idx, model in enumerate(AVAILABLE_MODELS, start=1):
        print(f"   {idx}   {model}")
    print("---------------------------------\n")

def export_chat(filename, history, export_mode):
    export_dir = "chat_export"
    os.makedirs(export_dir, exist_ok=True)
    full_path = os.path.join(export_dir, filename)
    if export_mode == "human":
        with open(full_path, "w", encoding="utf-8") as f:
            for msg in history:
                role = msg["role"]
                text = msg["parts"][0]["text"]
                if role == "user":
                    f.write(f"You: {text}\n")
                else:
                    f.write(f"Gemini: {text}\n")
                f.write("\n") # empty line separator
        print(f"System Success: Conversation history saved to {full_path}")

    elif export_mode == "json":
        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)
        print(f"System Success: Conversation history saved to {full_path}")

def show_status_menu(current_model, temperature, max_output_tokens, history_length):
    print("\n---------- Status Menu ----------")
    print(f"    Model               : {current_model}")
    print(f"    Temperature         : {temperature}")
    print(f"    Max Output Tokens   : {max_output_tokens}")
    print(f"    Conversation Length : {history_length} messages")
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

            elif command == "/save-human":
                try:
                    if not history:
                        print("\nNothing is saved; conversation is empty.\n")
                        continue

                    export_mode = "human"
                    if len(args) == 0:
                        filename = "chat_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
                        export_chat(filename, history, export_mode)
                        continue
                    
                    else:
                        filename = args[0]
                        if not filename.endswith(".txt"):
                            filename += ".txt"
                        export_chat(filename, history, export_mode)
                        continue


                except (OSError, IOError) as e:
                    print(f"Error Exporting Chat: {e}")
                    continue

            elif command == "/save-json":
                try:
                    if not history:
                        print("\nNothing is saved; conversation is empty.\n")
                        continue

                    export_mode = "json"
                    if len(args) == 0:
                        filename = "chat_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".json"
                        export_chat(filename, history, export_mode)
                        continue
                    else:
                        filename = args[0]
                        if not filename.endswith(".json"):
                            filename+= ".json"
                        export_chat(filename, history, export_mode)
                        continue

                except (OSError, IOError) as e:
                    print(f"Error Exporting Chat: {e}")
                    continue

            elif command == "/load":
                if len(args) == 0:
                    print("\nPlease provide the complete file name to load into memory (e.g. /load test1.json)\n")
                    continue
                else:
                    filename = args[0]
                    full_path = os.path.join("chat_export", filename)

                    try:
                        with open(full_path, "r", encoding="utf-8") as f:
                            loaded = json.load(f)
                        if not isinstance(loaded, list):
                            print("\nInvalid file format. Conversation must be a list of messages.\n")
                            continue
                        
                        history = loaded # replace history with loaded conversation
                        print(f"\nSystem Success: Loaded conversation from {full_path} ({len(history)} messages).\n")
                        continue

                    except FileNotFoundError:
                        print(f"\nFile not found: {full_path}\n") 
                        continue
                    
                    except json.JSONDecodeError:
                        print(f"\nSystem Error: {full_path} is not valid JSON.\n")
                        continue

                    except (OSError, IOError) as e:
                        print(f"Error reading file: {e}")
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
