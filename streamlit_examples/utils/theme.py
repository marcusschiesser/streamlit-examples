import os

import streamlit as st
from PIL import Image


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)


def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)


def initPage(page_title):
    dir_root = os.path.dirname(os.path.abspath(__file__))
    favicon = Image.open(dir_root + "/../assets/favicon.png")
    st.set_page_config(page_title=page_title, page_icon=favicon)
    local_css("style.css")
    # insert header brand with logo and link to website
    st.components.v1.html(
        """
        <style>
            .header-brand {
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            .header-divider {
                height: 1px;
                margin-top: 5px;
                background-color: rgba(49, 51, 63, 0.2);
            }
        </style>

        <div class="header-brand">
            <a href="https://schiesser-it.com/" target="_blank">
                <img src="https://schiesser-it.com/images/logo/schiesser.svg" width="200" />
            </a>
            <a href="https://www.linkedin.com/in/marcusschiesser" target="_blank">
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    fill="#0a66c2"
                    class="mercado-match"
                    width="32"
                    height="32"
                    focusable="false"
                >
                    <path
                        d="M20.5 2h-17A1.5 1.5 0 002 3.5v17A1.5 1.5 0 003.5 22h17a1.5 1.5 0 001.5-1.5v-17A1.5 1.5 0 0020.5 2zM8 19H5v-9h3zM6.5 8.25A1.75 1.75 0 118.3 6.5a1.78 1.78 0 01-1.8 1.75zM19 19h-3v-4.74c0-1.42-.6-1.93-1.38-1.93A1.74 1.74 0 0013 14.19a.66.66 0 000 .14V19h-3v-9h2.9v1.3a3.11 3.11 0 012.7-1.4c1.55 0 3.36.86 3.36 3.66z"
                    ></path>
                </svg>
            </a>
        </div>
        <div class="header-divider" />
        """,
        height=80,
    )
    st.markdown(f"## {page_title}")
