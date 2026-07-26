import streamlit as st
from backend.core import validate_user, add_user

st.set_page_config(
    page_title="Login - LangGraph Chatbot with Memory",
    page_icon="🔑",
    layout="centered",
)

st.title("🔑 Login - LangGraph Chatbot")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if "username" not in st.session_state:
    st.session_state["username"] = ""

tab1, tab2 = st.tabs(["Login", "Register"])


with tab1:
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", type="primary"):
        if username and password:
            try:
                if validate_user(username, password):
                    st.session_state["authenticated"] = True
                    st.session_state["username"] = username
                    st.success("✅ Login successful! Redirecting...")
                    st.switch_page("pages/frontend.py")
                else:
                    st.error("❌ Invalid username or password")
            except Exception as e:
                st.error(f"❌ Login failed: {str(e)}")
        else:
            st.warning("⚠️ Please enter both username and password")

# ---------------- Register ----------------
with tab2:
    new_user = st.text_input("New Username", key="reg_username")
    new_pass = st.text_input("New Password", type="password", key="reg_password")
    confirm_pass = st.text_input(
        "Confirm Password", type="password", key="confirm_password"
    )

    if st.button("Register", type="primary"):
        if new_user and new_pass and confirm_pass:
            if new_pass != confirm_pass:
                st.error("❌ Passwords don't match")
            elif len(new_pass) < 6:
                st.error("❌ Password must be at least 6 characters")
            else:
                try:
                    add_user(new_user, new_pass)
                    st.success("🎉 User registered successfully! Please login.")
                except Exception as e:
                    if "duplicate key" in str(e).lower():
                        st.error("❌ Username already exists")
                    else:
                        st.error(f"❌ Registration failed: {str(e)}")
        else:
            st.warning("⚠️ Please fill all fields")
