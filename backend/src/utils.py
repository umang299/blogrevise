import io
import docx
import yaml
import json
import PyPDF2


def load_yaml_file(file_path):
    """
    Load data from a YAML file.

    Parameters:
        file_path (str): The path to the YAML file.

    Returns:
        dict: The data loaded from the YAML file.
    """
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        return data
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error occurred while loading YAML file: {e}")
        return None


def read_text_file(file_path):
    """
    Read the contents of a text file.

    Parameters:
        file_path (str): The path to the text file.

    Returns:
        str: The contents of the text file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None


def extract_text(uploaded_file):
    # Determine the file type by its name
    if uploaded_file.name.endswith('.txt'):
        # Read text directly from the uploaded file object
        return uploaded_file.read().decode('utf-8')

    elif uploaded_file.name.endswith('.docx'):
        # Convert byte stream to a file-like object for docx
        file_stream = io.BytesIO(uploaded_file.getvalue())
        doc = docx.Document(file_stream)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])

    elif uploaded_file.name.endswith('.pdf'):
        # Convert byte stream to a file-like object for pdf
        file_stream = io.BytesIO(uploaded_file.getvalue())
        pdf_reader = PyPDF2.PdfReader(file_stream)
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()
        return text

    else:
        return "Unsupported file format"


def save_dict_to_json(data, file_path):
    """
    Save a dictionary to a JSON file.

    Args:
        data (dict): The dictionary to be saved.
        file_path (str): The file path where the JSON file will be saved.
    """
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
