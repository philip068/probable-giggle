import click

def prompt_positive_int(prompt_text: str, default: int = 0) -> int:
    """
    Prompt the user for a positive integer. Continues to prompt until valid input is received.

    Parameters:
        prompt_text (str): The message displayed to the user.
        default (int): The default value if the user presses Enter without input.

    Returns:
        int: The validated positive integer input by the user.
    """
    while True:
        try:
            value = click.prompt(prompt_text, type=int, default=default)
            if value < 0:
                click.echo("⚠️ Value cannot be negative. Please enter a valid number.")
            else:
                return value
        except click.Abort:
            # Handle user abort (e.g., Ctrl+C)
            click.echo("\nOperation aborted by the user.")
            raise
        except Exception as e:
            click.echo(f"⚠️ Invalid input: {e}. Please enter a valid number.")
