import streamlit as st

def bg_main():
    st.markdown("""
    <style>
    .stMain {
        background-image: url('https://w0.peakpx.com/wallpaper/314/578/HD-wallpaper-dark-bg-bg-wp-abstract-dark.jpg'); /* Local background image */
        background-size: cover;
    }
    </style>
    """,unsafe_allow_html=True)

def local_bg_image():
    css='''
    <style>
    .stMain{
        background-image: url('leo.jpg');
        background-size: cover;
    }
    </style>
    '''
    st.markdown(css,unsafe_allow_html=True)

