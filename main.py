import streamlit as st
import sqlite3
from streamlit_option_menu import option_menu
import main1 as fac
import streamlit_custome_css as leo
import mail_reg as cu_mail
from PIL import Image
import io

st.markdown("""<center><h1 style="color:red;">Face Recognition Attendance</h1></center>""",unsafe_allow_html=True)




# Initialize session state for hiding menu and tracking login/signup state
if "hide_menu" not in st.session_state:
    st.session_state.hide_menu = False
if "page" not in st.session_state:
    st.session_state["page"] = "signup"
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = None

# Function to toggle menu visibility
def toggle_menu():
    st.session_state.hide_menu = not st.session_state.hide_menu

# Function to hide the option menu dynamically
def hide_option_menu():
    '''st.markdown(
        """
        <style>
        div[data-testid="stHorizontalBlock"] {
            display: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )'''

# Database setup
conn = sqlite3.connect('login_face.db', check_same_thread=False)
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS users (
    name TEXT NOT NULL,
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    email TEXT NOT NULL,
    image BLOB
)
''')
conn.commit()

# Function to register a new user
def register_user(name, username, password, email, image):
    try:
        c.execute('INSERT INTO users (name, username, password, email, image) VALUES (?, ?, ?, ?, ?)',(name, username, password, email, image))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Username already exists

# Function to validate user login
def validate_user(username, password):
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    return c.fetchone()

# Fetch user profile image
def fetch_user_image(username):
    c.execute("SELECT image FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    return row[0] if row and row[0] else None

# Show the menu only if not hidden
if not st.session_state.hide_menu:
    selected = option_menu(
        menu_title="",
        options=["login", "signup"],
        icons=["box-arrow-in-right", "person-plus"],
        orientation="horizontal",
    )
    
    if selected == "login":
        st.session_state["page"] = "login"
    else:
        st.session_state["page"] = "signup"

# Button to hide/show menu


# Login Page
def login_page():


    st.markdown("""
    <style>
    .stMain {
        background-image: url('https://th.bing.com/th/id/R.85983b9ac7d79c7c1152cba8a23ce5ff?rik=lRjjjbPyNSvmNw&riu=http%3a%2f%2f3.bp.blogspot.com%2f-mhK_tpzR53E%2fWZmYT0sk-GI%2fAAAAAAAAHfI%2fffaJPRth_F4OunrWGpyPXsA6GW_bMtrQwCHMYBhgL%2fs1600%2fplain-design-pattern-dark-background-image-hd-resolution-latest.jpg&ehk=KnM3VMz52RBfF0T9%2bRI2oA8qbSqbztYohceXM1vhwqk%3d&risl=&pid=ImgRaw&r=0'); /* Local background image */
        background-size: cover;
    }
    
    
    .login-form {
        background-color: rgba(0, 0, 0, 0.6);  /* Semi-transparent black */
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        width: 100%;
        max-width: 400px;
    }
    h2 {
        color: #fff;
    }
    </style>
    """, unsafe_allow_html=True)
    #st.markdown('''<center><h2 id="login" style="color: white;">Staff Login</h2></center>''', unsafe_allow_html=True)
    
    username1 = st.text_input("Username ")
    password1 = st.text_input("Password ", type="password")

    st.markdown("""
        <style>
        .stApp {
            background-image: url('');
            background-size: cover;
            background-position: center;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .login-form {
            background-color: rgba(0, 0, 0, 0.6);  /* Semi-transparent black */
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            width: 100%;
            max-width: 400px;
        }

        .stForm {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }

        

        h2 {
            color: white;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    
    if st.button("Login",on_click=toggle_menu):
        user = validate_user(username1, password1)
        if user:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username1
            st.session_state["profile_pic"] = fetch_user_image(username1)
            st.success("Login successful! Redirecting...")
            st.rerun()
        else:
            st.error("Invalid username or password.")

# Signup Page
def signup_page():


    leo.bg_image('https://i.pinimg.com/originals/ff/04/31/ff0431d11ff6b73e937280252f58f371.gif')
    
    st.markdown("""<center><h1>Signup</h1></center>""",unsafe_allow_html=True)
    name = st.text_input("Name",placeholder="Enter Name")
    username = st.text_input("Username",placeholder="Enter Username")
    email = st.text_input("Email",placeholder="Enter Email")
    password = st.text_input("Password", type="password",placeholder="Enter password")
    image_file = st.file_uploader("Upload Profile Picture", type=["png", "jpg", "jpeg"])

    if st.button("Signup"):
        if len(password) < 8:
            st.error("Password must be at least 8 characters.")
        else:
            if image_file:
                image_data = image_file.read() if image_file else None
            else:
                st.error("profile picture is must upload")
            try:
                if register_user(name, username, password, email, image_data):
                    cu_mail.mail_send(email, name, username, password)
                    st.success("Signup successful! Please login.")
                
                else:
                    st.error("Username already exists.")
            except:
                pass

# Sidebar with Logout
def sidebar():
    with st.sidebar:
        leo.sidebar_bg_image('https://t3.ftcdn.net/jpg/02/32/99/54/360_F_232995426_xAopAAEterBrZhcC1CXLVtCF6RhYF5Z3.jpg')
        
        if st.button("Logout"):
            st.session_state["logged_in"] = False
            st.session_state["page"] = "login"
            st.session_state["username"] = None
            st.session_state.hide_menu = False
            st.rerun()

# Main Page after login
def main_page():
    st.title(f"Welcome  {st.session_state['username']}!")
    
    # Display User Profile Picture
    if "profile_pic" in st.session_state:
        image_data = st.session_state["profile_pic"]
        image = Image.open(io.BytesIO(image_data))  # Convert bytes to image

        st.markdown("""
        <style>
        img[data-testid="stLogo"] {
            height: 4rem;
            border-radius:20px;
        })</style>""",unsafe_allow_html=True)
        st.logo(image,size="large")
    else:
        st.warning("No profile picture found.")
    

# Control flow for login/signup
if st.session_state["logged_in"]:
    main_page()
    fac.main()
    
    
    hide_option_menu()
    sidebar()
    
else:
    if st.session_state["page"] == "login":
        login_page()
    else:
        signup_page()






