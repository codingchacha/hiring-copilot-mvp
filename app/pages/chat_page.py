import streamlit as st
from llm_client import prompt_to_candidate_query
from candidate_data import load_candidates, rank_candidates, format_candidates_for_ui

st.set_page_config(page_title="Candidate Search", layout="centered")

# --- Simple user "database" for demo ---
USERS = {
    "user@example.com": "password123",
    "admin@example.com": "adminpass"
}

# --- Login Functionality ---
def login():
    st.title("🔐 Please log in")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if email in USERS and USERS[email] == password:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.experimental_rerun()
        else:
            st.error("❌ Invalid email or password")

def logout():
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_email = None
        st.session_state.chat_history = []
        st.experimental_rerun()

# --- Main app ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_email = None

if not st.session_state.logged_in:
    login()
else:
    st.title("🧠 AI-Powered Candidate Search")
    st.write(f"Welcome, **{st.session_state.user_email}**!")
    logout()

    # Load candidates once
    candidates = load_candidates("mock_candidates.json")

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Clear chat button
    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []

    # Display previous chat messages
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User prompt input
    prompt = st.chat_input("Describe the ideal candidate, role, or ask a question...")

    if prompt:
        # Save user prompt in history
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        # Call LLM to convert prompt into query
        query = prompt_to_candidate_query(prompt)

        # Rank candidates based on query
        top_candidates = rank_candidates(candidates, query, top_n=5)

        # Format top candidates for UI display
        formatted_candidates = format_candidates_for_ui(top_candidates)

        # Display results
        with st.chat_message("assistant"):
            if formatted_candidates:
                st.markdown("### Top Matching Candidates:")
                for i, c in enumerate(formatted_candidates, 1):
                    with st.container():
                        st.markdown(f"**{i}. {c['Name']}**")
                        st.markdown(f"- Email: {c['Email']}")
                        st.markdown(f"- Skills: {', '.join(c['Skills'])}")
                        st.markdown(f"- Experience: {c['Experience']} years")
                        st.markdown(f"- Location: {c['Location']}")
                        if "Certifications" in c:
                            st.markdown(f"- Certifications: {', '.join(c['Certifications'])}")
                        if "GitHub Repos" in c:
                            repos = ", ".join(f"{r['name']} ({r['stars']}⭐)" for r in c["GitHub Repos"])
                            st.markdown(f"- GitHub Repos: {repos}")

                        # Buttons container (side by side)
                        col1, col2 = st.columns([1,1])

                        with col1:
                            mail_btn_key = f"mail_{i}"
                            if st.button("📧 Send Email", key=mail_btn_key):
                                st.session_state[f"mail_sent_{i}"] = True
                        with col2:
                            bg_check_key = f"bg_check_{i}"
                            if st.button("🔍 Background Check", key=bg_check_key):
                                st.session_state[f"bg_check_initiated_{i}"] = True

                        # Show success messages if buttons were clicked
                        if st.session_state.get(f"mail_sent_{i}", False):
                            st.success("📨 Mail has been sent successfully with your interest. Candidate has been communicated to reply back if interested in job change.")
                        if st.session_state.get(f"bg_check_initiated_{i}", True):
                            st.info("🕵️ Background verification initiated. Reports will be shared within 7 working days.")
            else:
                st.markdown("No matching candidates found for your query.")

        # Save reply in chat history (optional, summarized)
        st.session_state.chat_history.append({"role": "assistant", "content": "Displayed top matching candidates."})
