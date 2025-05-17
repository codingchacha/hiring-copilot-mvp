import os
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables from the parent directory's .env file
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase URL and KEY must be set in .env file")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def signup_user(email: str, password: str):
    try:
        response = supabase.auth.sign_up({"email": email, "password": password})
        if response.user is not None:
            return True, "Signup successful. Please verify your email."
        else:
            return False, f"Signup failed: {response.error}"
    except Exception as e:
        return False, f"Signup error: {str(e)}"

def login_user(email: str, password: str):
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if response.user is not None:
            return True, "Login successful"
        else:
            return False, f"Login failed: {response.error}"
    except Exception as e:
        return False, f"Login error: {str(e)}"
