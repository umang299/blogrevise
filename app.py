import os
import streamlit as st
from main import (PromptGenerator, extract_text,
                  get_response)


def save_and_download_text(text, filename="download.txt"):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)
    # Provide a download button
    with open(filename, "r", encoding='utf-8') as f:
        st.download_button(
            label="Download Text File",
            data=f,
            file_name=filename,
            mime="text/plain"
        )

    os.remove(path=filename)


keywords = st.text_input(
            label="Enter Keywords",
            placeholder='Ai, Generative AI, .....'
            )

instruction = st.text_input(
            label="Enter Instructions",
            placeholder='Write it under 150 words'
            )

with st.sidebar:
    st.title('Upload File')
    uploaded_files = st.file_uploader(
                label='Choose a text file',
                accept_multiple_files=False
            )
    generate = st.button(label='Generate')

    if uploaded_files is not None:
        input_text = extract_text(uploaded_file=uploaded_files)

        prompt_gen = PromptGenerator(
                    blog=input_text,
                    keyword=keywords,
                    instructions=instruction)

        messages = prompt_gen.generate()

    else:
        pass

if generate:
    with st.spinner(text='Thinking....'):
        response = get_response(message=messages)
        st.text_area(label='Generated Article', value=response, height=400)
        save_and_download_text(text=response, filename='Generated_Article.txt')
