import argparse
import time

from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.text import Text

from bots import bots
from utils import (generate_final_piece, generate_message, initialize_logging,
                   initialize_openai, read_file, save_conversation_history,
                   save_final_piece)

console = Console()

def print_message(bot_name, message, color):
    # Print the bot's name in its designated color
    console.print(f"{bot_name}:", style=f"bold {color}")
    # Print the bot's message in the same color and inside a panel for better visibility
    console.print(Panel.fit(Text(message, style=color, justify="left")))

# Main function
def main():
    parser = argparse.ArgumentParser(description="Run a conversation between WriterBot and EditorBot.")
    parser.add_argument("-k", "--key", help="The path to the text file containing the OpenAI API key.")
    parser.add_argument("-s", "--subject", help="The subject for the security awareness piece.")
    parser.add_argument("-t", "--timeout", type=int, default=20, help="The timeout in seconds for the OpenAI API.")
    parser.add_argument("-l", "--log", help="The path to the log file.")
    args = parser.parse_args()

    # Read the API key from a text file
    api_key = read_file(args.key)

    # Initialize the OpenAI API
    initialize_openai(api_key)

    # Initialize logging
    if args.log:
        initialize_logging(args.log)

    # Initialize the conversation with a system message
    messages = [{"role": "system", "content": f"WriterBot, your role is {bots[0]['name']}. EditorBot, your role is {bots[1]['name']}. The subject is {args.subject}."}]

    # Define the conversation stages
    conversation_stages = ["writing_initial", "review_1", "writing_revision_1", "review_2", "writing_revision_2", "confirmation", "final_generation"]
    stage_index = 0

    # Start a progress bar
    with Progress(TextColumn("[bold cyan]{task.description}"), BarColumn(), SpinnerColumn(), TextColumn("[bold green]{task.completed}/{task.total}"), console=console, transient=True) as progress:
        num_turns = 7  # Initial writing, two rounds of review and revision, confirmation, and final generation
        task = progress.add_task("[yellow]Running conversation...", total=num_turns)

        # Loop through a fixed number of turns, iterating through the bots
        for i in range(num_turns):
            # Select the current bot based on the conversation stage
            if conversation_stages[stage_index] in ["writing_initial", "writing_revision_1", "writing_revision_2"]:
                current_bot = bots[0]  # WriterBot
                bot_color = "cyan"
                if conversation_stages[stage_index] == "writing_initial":
                    bot_content = current_bot["initial_message"]
                else:
                    bot_content = current_bot["prompt"]
            elif conversation_stages[stage_index] in ["review_1", "review_2"]:
                current_bot = bots[1]  # EditorBot
                bot_color = "green"
                if conversation_stages[stage_index] == "review_1":
                    bot_content = current_bot["initial_message"]
                else:
                    bot_content = current_bot["prompt"]
            elif conversation_stages[stage_index] == "confirmation":
                # Stop the progress bar before asking for user confirmation
                progress.stop()
                # Ask for user confirmation to finish the process
                confirmation = input("Do you want to finish the process and generate the final piece? (y/n) ")
                # Restart the progress bar after getting user confirmation
                progress.start()
                if confirmation.lower() == 'y':
                    stage_index += 1
                    console.print("Finishing process...")
                    continue
                else:
                    console.print("Exiting process...")
                    break
            elif conversation_stages[stage_index] == "final_generation":
                # Generate the final piece and save it to a file
                console.print("Generating final piece...")
                final_piece = generate_final_piece(messages, args.timeout)
                try:
                    save_final_piece(final_piece, "final_piece.html")
                    console.print("Final piece saved to final_piece.html")
                except Exception as e:
                    console.print(Panel.fit(Text(f"An error occurred while saving the final piece: {e}", style="bold red")))
                break


            # Generate a message from the current bot and add it to the conversation
            message = generate_message(messages, current_bot["name"], bot_content, args.timeout)
            messages.append({"role": current_bot["name"], "content": message})
            print_message(current_bot["name"], message, bot_color)


           # Increment and print the turn count after every iteration
            stage_index += 1
            time.sleep(1)
            progress.update(task, advance=1)
            console.print("\n")  # Add newline character

    # Save the conversation history to a file
    conversation_history = [f"{msg['role']}: {msg['content']}" for msg in messages]
    save_conversation_history(conversation_history, "conversation_history.txt")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        console.print(Panel.fit(Text(f"An error occurred: {e}", style="bold red")))
