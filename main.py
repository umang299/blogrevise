import os
import io
import docx
import PyPDF2
from openai import OpenAI

api_key = os.environ['OPENAI_API_KEY']
client = OpenAI(api_key=api_key)


class PromptGenerator:
    def __init__(
                self,
                blog: str = None,
                keyword: list[str] = None,
                instructions: str = None):

        self.blog = blog if blog is not None else ''

        if keyword is not None:
            assert type(keyword) is str
            self.keyword = keyword
        else:
            self.keyword = ''

        self.instruction = instructions
        self.sys_prompt = self._read_from_file(file_path='prompt.txt')
        self.sys_prompt = self._append_keywords()
        self.sys_prompt = self._append_instructions()

    def _read_from_file(self, file_path):
        with open(file_path, 'r') as f:
            text = f.read()
        return text

    def _append_keywords(self):
        if self.keyword == '':
            return self.sys_prompt
        else:
            self.sys_prompt = self.sys_prompt.replace(
                "<<KEYWORDS>>", self.keyword
            )
            return self.sys_prompt

    def _append_instructions(self):
        if self.instruction is not None:
            self.sys_prompt = self.sys_prompt.replace(
                "<<INSTRUCTIONS>>", self.instruction
            )
            return self.sys_prompt
        else:
            self.sys_prompt = self.sys_prompt.replace(
                "<<INSTRUCTIONS>>", ''
            )
            return self.sys_prompt

    def generate(self):
        messages = [
            {'role': 'system', 'content': self.sys_prompt},
            {'role': 'user', 'content': self.blog}
            ]
        return messages


def get_response(model: str = None, message: str = None):
    if message is None:
        return 'Input message not found'
    else:
        if model is None:
            model = "gpt-4-1106-preview"
            response = client.chat.completions.create(
                            model="gpt-4-1106-preview",
                            messages=message,
                            frequency_penalty=1,
                            temperature=0.2
                            )
            return response.choices[0].message.content
        else:
            response = client.chat.completions.create(
                            model=model,
                            messages=message
                            )
            return response.choices[0].message.content


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
