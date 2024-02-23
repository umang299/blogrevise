import yaml
import streamlit as st
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu

from src import Blog_Outline, Content_Brief, Write_Blog

st.set_page_config(page_title='MarketingSidekick')


with open('config.yaml') as file:
    config = yaml.load(file, Loader=yaml.loader.SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login(
                                                    location='main',
                                                    fields={
                                                        'Form name': 'Login',
                                                        'Username': 'Username',
                                                        'Password': 'Password',
                                                        'Login': 'Login'}
                                                    )

if authentication_status:
    authenticator.logout('Logout', 'main')
    st.header(f" {name}'s Marketing SideKick")
    with st.sidebar:
        app = option_menu(
                    menu_title='Tasks',
                    options=['Blog Outline', 'Content Brief', 'Write a Blog'],
                    menu_icon='chat-text-fill',
                    default_index=1,
                    styles={
                        "container": {
                                    "padding": "5!important",
                                    "background-color": 'black'
                                    },
                        "icon": {
                                "color": "white",
                                "font-size": "23px"
                                },
                        "nav-link": {
                                "color": "white",
                                "font-size": "20px",
                                "text-align": "left",
                                "margin": "0px",
                                "--hover-color": "blue"
                                },
                        "nav-link-selected": {"background-color": "#02ab21"}
                        }
                    )

    if app == "Blog Outline":
        Blog_Outline.app()
    if app == "Content Brief":
        Content_Brief.app()
    if app == "Write a Blog":
        Write_Blog.app()

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')