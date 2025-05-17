import streamlit as st
from supabase_client import signup_user, login_user
from candidate_data import load_candidates 


st.set_page_config(page_title="AI Hiring Copilot", layout="centered")

# ─── Session-state defaults ───────────────────────────────────────────────────
defaults = {
    "logged_in": False,
    "show_signup": False,
    "user_email": "",
    "login_error": "",
    "signup_error": "",
    "signup_success": "",
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ─── Navigation helpers ───────────────────────────────────────────────────────
def do_logout():
    st.session_state.logged_in = False
    st.session_state.user_email = ""

# ─── UI Sections ──────────────────────────────────────────────────────────────
def show_login():
    # Blue button CSS for login and signup
    st.markdown("""
    <style>
    div[data-testid='stButton'] > button, 
    div[data-testid='stFormSubmitButton'] > button {
        background-color: #007bff !important;
        color: white !important;
        border: none !important;
    }
    div[data-testid='stButton'] > button:hover, 
    div[data-testid='stFormSubmitButton'] > button:hover {
        background-color: #0056b3 !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🚀 AI Hiring Copilot")

    if not st.session_state.show_signup:
        st.header("Login")
        with st.form("login_form"):
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            submitted = st.form_submit_button("Login", type="primary")
            if submitted:
                success, msg = login_user(email.strip(), password.strip())
                if success:
                    st.session_state.logged_in = True
                    st.session_state.user_email = email
                    st.session_state.login_error = ""
                else:
                    if 'Invalid login credentials' in msg:
                        st.session_state.login_error = "Incorrect email or password"
                    elif 'You must provide either an email or phone number and a password' in msg:
                        st.session_state.login_error = "Please enter both email and password"
                    else:
                        st.session_state.login_error = msg

        if st.session_state.login_error:
            st.error(st.session_state.login_error)

        st.write("Don't have an account?")
        st.markdown("*⚠️ Double-click Login button to proceed*")
        if st.button("Go to Sign Up", type="primary"):
            st.session_state.show_signup = True
            st.session_state.login_error = ""

    else:
        st.header("Sign Up")
        st.markdown("""
        <style>
        div[data-testid='stButton'] > button, 
        div[data-testid='stFormSubmitButton'] > button {
            background-color: #007bff !important;
            color: white !important;
            border: none !important;
        }
        div[data-testid='stButton'] > button:hover, 
        div[data-testid='stFormSubmitButton'] > button:hover {
            background-color: #0056b3 !important;
            color: white !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        with st.form("signup_form"):
            email = st.text_input("Email", key="signup_email")
            password = st.text_input("Password", type="password", key="signup_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm")
            submitted = st.form_submit_button("Sign Up", type="primary")
            if submitted:
                if password != confirm_password:
                    st.session_state.signup_error = "Passwords do not match"
                else:
                    success, msg = signup_user(email.strip(), password.strip())
                    if success:
                        st.session_state.signup_success = msg
                        st.session_state.signup_error = ""
                        st.session_state.logged_in = True
                        st.session_state.user_email = email
                        st.session_state.show_signup = False
                    else:
                        st.session_state.signup_error = msg

        if st.session_state.signup_error:
            st.error(st.session_state.signup_error)
        elif st.session_state.signup_success:
            st.success(st.session_state.signup_success)

        st.write("Already have an account?")
        if st.button("Go to Login", type="primary"):
            st.session_state.show_signup = False
            st.session_state.signup_error = ""
            st.session_state.signup_success = ""

def show_dashboard():
    # Custom blue button CSS for all buttons
    st.markdown("""
    <style>
    div[data-testid='stButton'] > button, 
    div[data-testid='stFormSubmitButton'] > button {
        background-color: #007bff !important;
        color: white !important;
        border: none !important;
    }
    div[data-testid='stButton'] > button:hover, 
    div[data-testid='stFormSubmitButton'] > button:hover {
        background-color: #0056b3 !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🚀 AI Hiring Copilot Dashboard")
    st.success(f"Welcome, {st.session_state.user_email}!")
    
    # Job Fit Analysis Section
    st.markdown("### 📄 Already Have a Resume?")
    st.markdown("""
    **Check Job Fitment Instantly!**
    - Analyze how well a candidate matches your job requirements
    - Get detailed insights into skills and potential
    - Make data-driven hiring decisions
    """)
    if st.button("📊 Analyze Resume Fitment", key="resume_fit", use_container_width=True, type="primary"):
        js = "window.open('https://reviewresume.streamlit.app/')"  # open in new tab
        st.components.v1.html(f"<script>{js}</script>", height=0)

    
    # Candidate Search Section
    st.markdown("### 🔍 Find Top Candidates")
    st.markdown("""
    **Smart Candidate Search**
    - Reduce hiring time by 70%
    - Cut recruitment costs significantly
    - Find the perfect match for your team
    - AI-powered candidate screening
    """)
    if st.button("🌟 Search Best Candidates", key="candidate_search", use_container_width=True, type="primary"):
        st.switch_page("pages/chat_page.py")
    
    # Logout Section
    st.markdown("---")
    st.markdown("*⚠️ Double-click Logout button to proceed*")
    if st.button("🚪 Logout", key="dashboard_logout", use_container_width=True, type="primary"):
        do_logout()

# ─── Main App Logic ───────────────────────────────────────────────────────────
if st.session_state.logged_in:
    show_dashboard()
else:
    show_login()
