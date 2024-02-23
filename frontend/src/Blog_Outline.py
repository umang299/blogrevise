import streamlit as st


def app():
    st.header(
        body=':red[Blog Outline]',
        anchor=False
    )

    my_outlines, generate, upload = st.tabs(tabs=['MyOutline', 'Generate', 'Upload'])

    with my_outlines:
        selected_outline = st.selectbox(
                                label='Select a file',
                                index=None,
                                options=['file1.txt', 'file2.txt', 'file3.txt'],
                                placeholder='Select a file'
                            )

        if selected_outline is not None:
            st.write(f'Blog Outline: {selected_outline}')
            st.text_area(label='Blog Outline', height=300)
        else:
            pass