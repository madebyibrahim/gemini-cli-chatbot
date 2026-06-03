Here's a concise README.md for your `gemini-cli-chatbot` repository. You can copy and paste this directly into your project.

```markdown
# Gemini CLI Chatbot

A real-time command-line chatbot powered by Google's Gemini API. Supports dynamic configuration of model, temperature, and token limits, conversation history, and export/import capabilities.

## Prerequisites

- Python 3.9+
- A [Gemini API key](https://aistudio.google.com/apikey)
- Store your key in a `.env` file: `GEMINI_API_KEY=your_api_key_here`

## Installation

```bash
git clone https://github.com/madebyibrahim/gemini-cli-chatbot.git
cd gemini-cli-chatbot
pip install google-genai python-dotenv
```

Create a `.env` file with your API key.

## Usage

```bash
python chatbot.py
```

### Available Commands

```
/help                     Shows this help menu
/status                   Shows the current active configuration
/temp <0.0 - 2.0>         Sets the temperature value
/max <tokens>             Set the maximum output tokens value
/model <number>           Sets the model (and shows list)
/exit or /quit            Ends the session
/clear                    Clears the conversation history
/save-human [file]        Export entire conversation to human-readable .txt file
/save-json [file]         Export entire conversation to .json file
/load [file]              Load a previously exported .json conversation
```

> Exported conversations are saved to the `chat_export/` subfolder.

### Example Session

```
You: /temp 1.2
System Success: Temperature value set to 1.2.

You: /model
Please input a valid number to select a model between 1 and 4.
---------- Models Menu ----------
 1 gemini-3.1-flash-lite
 2 gemini-3.5-flash
 3 gemini-2.5-flash
 4 gemini-2.5-flash-lite
---------------------------------

You: 2
System Success: Model set to gemini-3.5-flash.

You: What's the capital of France?
Gemini: The capital of France is Paris.
```