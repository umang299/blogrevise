import os
import sys
import requests
import streamlit as st

cwd = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(cwd)


from backend.src.aws import AWSClient
from backend.src.utils import load_yaml_file, extract_text
from backend.src.BlogOutline import BlogOutline

config = load_yaml_file(file_path=os.path.join(cwd, 'backend', 'config.yaml'))

outline = BlogOutline()
aws_client = AWSClient(config=config)


def on_click_upload():
    st.session_state.upload_clicked = True


def app():
    ## HEADER
    st.header(
        body=':red[Blog Outline]',
        anchor=False
    )

    if 'upload_clicked' not in st.session_state:
        st.session_state.upload_clicked = False

    # DEFINING TABS
    my_outlines, generate, upload = st.tabs(tabs=['MyOutline', 'Generate', 'Upload'])

    # MY OUTLINES TAB
    with my_outlines:
        selected_outline = st.selectbox(
                label='Select a file',
                index=None,
                options=outline.get_outline_filenames_by_user_id(
                    user_id='abc123456'
                ),
                placeholder='Select a file'
            )

        if selected_outline is not None:
            st.write(f'Blog Outline: {selected_outline}')
            st.text_area(label='Blog Outline', height=300)
        else:
            pass

    # GENERATE OUTLINE TAB
    with generate:
        topic = st.text_input(label='Enter a singular topic with specific \
                               contents like relevant examples, statistics')
        if topic is not None:
            st.write(f'Topic: {topic}')
        else:
            st.error('Enter a topic ')

        instructions = st.text_input(label='Preference Instructions')
        if instructions is not None:
            st.write(f'Instructions: {instructions}')
        else:
            pass

        col1, col2, col3 = st.columns(3)
        with col1:
            from_my_outlines = st.toggle(label='Import from my outlines')
        with col2:
            generate_button = st.button(
                                    label='Generate',
                                    key=125,
                                    type='primary')
        with col3:
            upload_button = st.button(
                                label='Upload',
                                key=127,
                                on_click=on_click_upload,
                                type='primary')

        if generate_button:
            params = {
                'topic': topic,
                'instructions': instructions
            }
            response = requests.get(
                            url=f"{config['url']}/generate_blog",
                            params=params
                        )
            if response.status_code == 200:
                st.text_area(
                        label='Blog Outline',
                        value=response.json()['outline'],
                        height=200
                    )

        if upload_button:
            st.write(f"{response}")

        elif from_my_outlines:
            selected_outline = st.selectbox(
                label='Select a file',
                index=None,
                key=126,
                options=outline.get_outline_filenames_by_user_id(
                    user_id='abc123456'
                ),
                placeholder='Select a file'
            )

    # UPLOAD OUTLINE TAB
    with upload:
        text = ''
        st.session_state['filename_popup'] = True
        uploaded_files = st.file_uploader(
                            label='Choose a text file',
                            accept_multiple_files=False
                        )

        if uploaded_files is not None:
            text = extract_text(uploaded_file=uploaded_files)
            st.text_area(label='Blog Outline', value=text, height=200)

            filename = st.text_input(label='Enter filename')
            upload_button = st.button(label='Upload file', key=126)

            if upload_button and text != '':
                if filename is not None:
                    st.write(f'filename : {filename}.txt')
                    upload_status, saved_filename = aws_client.upload_file(
                                        text=text,
                                        filename=f'{filename}.txt'
                                    )

                    if upload_status:
                        st.success(f'{saved_filename} uploaded')
                    else:
                        st.success(f'Failed to upload {saved_filename}')
        else:
            pass
