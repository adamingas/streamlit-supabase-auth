"""
Demo app for streamlit-supabase-auth.

To run this example:
1. Set environment variables:
   export SUPABASE_URL="https://your-project.supabase.co"
   export SUPABASE_KEY="your-anon-key"

2. Run:
   uv run streamlit run examples/demo.py
   
   Or with regular streamlit:
   streamlit run examples/demo.py
"""

import os

import streamlit as st

# For development, import from parent directory
# In production, use: from streamlit_supabase_auth import SupabaseAuth
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from streamlit_supabase_auth import SupabaseAuth

# Page config
st.set_page_config(
    page_title="Streamlit Supabase Auth Demo",
    page_icon="🔐",
    layout="wide",
)

# Initialize auth
auth = SupabaseAuth(
    supabase_url=os.getenv("SUPABASE_URL", ""),
    supabase_key=os.getenv("SUPABASE_KEY", ""),
    redirect_uri=os.getenv("REDIRECT_URI", "http://localhost:8501"),
)

# Main UI
st.title("🔐 Streamlit Supabase Auth Demo")

if auth.is_authenticated():
    user = auth.get_user()

    st.success(f"✅ Authenticated as **{user.email}**")

    # User info
    with st.expander("👤 User Information", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            st.write("**User ID:**")
            st.code(user.id)

            st.write("**Email:**")
            st.code(user.email)

        with col2:
            st.write("**Provider:**")
            provider = user.app_metadata.get("provider", "unknown")
            st.code(provider)

            st.write("**Created At:**")
            st.code(user.created_at)

    # User metadata
    if user.user_metadata:
        with st.expander("📋 User Metadata"):
            st.json(user.user_metadata)

    # App metadata
    if user.app_metadata:
        with st.expander("⚙️ App Metadata"):
            st.json(user.app_metadata)

    # Logout section
    st.divider()
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("🚪 Logout", type="secondary", use_container_width=True):
            auth.logout()

else:
    st.info("👋 Welcome! Please login to continue.")

    # Check if credentials are configured
    if not os.getenv("SUPABASE_URL") or not os.getenv("SUPABASE_KEY"):
        st.warning(
            """
            ⚠️ **Environment variables not set!**
            
            Please set the following:
            ```bash
            export SUPABASE_URL="https://your-project.supabase.co"
            export SUPABASE_KEY="your-anon-key"
            ```
            """
        )
    else:
        st.write("Choose your login method:")

        col1, col2, col3 = st.columns(3)

        with col1:
            auth.login_button(
                provider="google",
                button_text="🔑 Google",
                use_container_width=True,
            )

        with col2:
            auth.login_button(
                provider="github",
                button_text="🐙 GitHub",
                use_container_width=True,
            )

        with col3:
            auth.login_button(
                provider="gitlab",
                button_text="🦊 GitLab",
                use_container_width=True,
            )

# Footer
st.divider()
st.caption(
    "Built with [Streamlit](https://streamlit.io) and [Supabase](https://supabase.com)"
)

