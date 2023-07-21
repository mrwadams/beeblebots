import openai
import logging
from exceptions import MissingFileError

# Function to read a file and return its content
def read_file(file_path):
    try:
        with open(file_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        raise MissingFileError(file_path)

# Function to initialize the OpenAI API
def initialize_openai(api_key):
    openai.api_key = api_key

# Function to initialize logging
def initialize_logging(log_file):
    logging.basicConfig(filename=log_file, level=logging.INFO)

# Function to generate a message using the OpenAI API and return the AI's response
def generate_message(messages, role, content, timeout):
    # Make a copy of the messages and change the 'role' to 'assistant' for WriterBot and EditorBot
    updated_messages = [{"role": "assistant" if msg["role"] in ["WriterBot", "EditorBot"] else msg["role"], "content": msg["content"]} for msg in messages]
    
    updated_messages.append({"role": "assistant" if role in ["WriterBot", "EditorBot"] else role, "content": content})
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k-0613",
            messages=updated_messages,
            max_tokens=1000,
            n=1,
            temperature=0.7,
            timeout=timeout,
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"An error occurred while generating a message: {e}")
        raise


# Function to save the conversation history to a file
def save_conversation_history(conversation_history, file_path):
    try:
        with open(file_path, "w") as file:
            file.write("\n".join(conversation_history))
    except Exception as e:
        logging.error(f"An error occurred while saving the conversation history: {e}")
        raise

# Function to generate the final piece using the OpenAI API and return the AI's response
def generate_final_piece(messages, timeout):
    # Make a copy of the messages and change the 'role' to 'assistant' for WriterBot and EditorBot
    updated_messages = [{"role": "assistant" if msg["role"] in ["WriterBot", "EditorBot"] else msg["role"], "content": msg["content"]} for msg in messages]
    
    updated_messages.append({"role": "assistant", "content": "Transform the final text into a professionally styled HTML template using Tailwind CSS. Use a light neutral background colour and choose bold bright colours for the headings."})
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k-0613",
            messages=updated_messages,
            max_tokens=2048,
            n=1,
            temperature=0.7,
            timeout=timeout,
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"An error occurred while generating the final piece: {e}")
        raise

# Function to save the final piece to a file
def save_final_piece(final_piece, file_path):
    try:
        with open(file_path, "w") as file:
            file.write(final_piece)
    except Exception as e:
        logging.error(f"An error occurred while saving the final piece: {e}")
        raise
