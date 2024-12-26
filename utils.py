from bs4 import BeautifulSoup

def read_keywords(file_path):
    """
    Reads keywords from a file and returns them as a list.

    Args:
        file_path (str): The path to the file containing keywords.

    Returns:
        list: A list of keywords, one per line, or an empty list if the file is empty.

    Raises:
        FileNotFoundError: If the file does not exist.
        IOError: If the file cannot be read.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = file.read().strip()
            # Split by newlines to handle multi-line files
            return data.splitlines() if data else []
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_path}") from e
    except IOError as e:
        raise IOError(f"Error reading file: {file_path}") from e


def extract_email_content(html_email_body, content_type, max_chars=None):
    """
    Extracts and prints the text content of an email based on its content type,
    while removing empty lines and optionally restricting the number of characters.

    Args:
        html_email_body (str): The email body, either as HTML or plain text.
        content_type (str): The type of content ('html' or 'text').
        subject (str): The subject of the email.
        max_chars (int, optional): The maximum number of characters to include in the extracted text. Defaults to None.

    Returns:
        str: The extracted text content from the email, limited by max_chars if specified.

    Raises:
        ValueError: If an unsupported content_type is provided.
    """
    try:
        if content_type.lower() == 'html':
            # Parse HTML content using BeautifulSoup
            soup = BeautifulSoup(html_email_body, 'html.parser')
            text = soup.get_text(separator='\n')  # Extract text with line separators
        elif content_type.lower() == 'text':
            # Treat the body as plain text
            text = html_email_body
        else:
            # Handle unsupported content types
            raise ValueError(f"Unsupported content type: {content_type}")

        # Clean and process extracted text
        clean_text = "\n".join(line.strip() for line in text.splitlines() if line.strip())

        # Restrict to max_chars if specified
        if max_chars is not None:
            clean_text = clean_text[:max_chars]

        return clean_text
    except Exception as e:
        print(f"An error occurred while extracting email content: {e}")
        raise