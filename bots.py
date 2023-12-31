
# This script defines the WriterBot and EditorBot, their roles, and their configurations.

# Define the bots and their configurations
bots = [
    {
        "name": "WriterBot",
        "color": "blue",
        "initial_message": "Please generate a brief piece on the given subject, making sure it is informative, engaging, and accessible to a general audience.",
        "prompt":   """
                    Carefully review the feedback from EditorBot. Incorporate the suggested changes and generate a revised version of the piece. Afterward, provide a detailed response to EditorBot explaining how you have addressed each point of feedback. Your response should be structured as follows:

                    REVISED PIECE:

                    RESPONSE TO EDITORBOT:
                    """
    },
    {
        "name": "EditorBot",
        "color": "green",
        "initial_message":  """
                            Review the piece generated by WriterBot. Provide detailed feedback and suggestions for improvement focusing on clarity, correctness, relevance, and engagement. Do not rewrite the piece. Instead, guide WriterBot to make the necessary changes. Your response should be structured as follows:

                            REVIEW COMMENTS:
                            """,
        "prompt":   """
                    Review the revised piece from WriterBot. Provide a succinct critique focusing on clarity, correctness, and effectiveness. Suggest improvements without rewriting the piece. Your response should be structured as follows:

                    REVIEW COMMENTS:
                    """
    }
]

