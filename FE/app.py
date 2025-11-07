# frontend/app.py
import streamlit as st
import requests
from pathlib import Path
from streamlit.components.v1 import html as components_html

# -------------------------------------------
# PAGE CONFIG
# -------------------------------------------
st.set_page_config(page_title="Codebase Genius", layout="wide")

# -------------------------------------------
# CSS STYLING
# -------------------------------------------
st.markdown("""
<style>
.main > div {
    max-width: 1000px;
    padding-left: 50px;
    padding-right: 50px;
}
.block-container {
    display: flex;
    flex-direction: column;
    height: 100vh;
    padding-top: 1rem;
    padding-bottom: 0;
}
.stTabs {
    position: sticky;
    top: 0;
    z-index: 100;
    background-color: white;
    padding-bottom: 1rem;
}
.chat-scroll {
    flex: 1;
    overflow-y: auto;
    padding: 1rem 0;
    margin-bottom: 1rem;
    max-height: calc(100vh - 300px);
}
.chat-input {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    background-color: white;
    padding: 1rem 0;
    border-top: 1px solid #e0e0e0;
    z-index: 50;
}
.stChatMessage {
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------
# BACKEND ENDPOINTS
# -------------------------------------------
BASE_URL = "http://127.0.0.1:8000"
CODEGENIUS_ENDPOINT = f"{BASE_URL}/walker/codebase_genius"
GET_DOCS_ENDPOINT = f"{BASE_URL}/walker/get_all_docs"
GET_DIAGRAMS_ENDPOINT = f"{BASE_URL}/walker/get_all_diagrams"

# -------------------------------------------
# SESSION STATE INIT
# -------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------------------------------
# SIDEBAR
# -------------------------------------------
with st.sidebar:
    st.title("Session")
    repo_url = st.text_input("GitHub repository URL", "")
    if st.button("Start Analysis"):
        if repo_url.strip() != "":
            st.session_state.chat_history = []
            st.session_state.chat_history.append({"role": "system", "content": f"Starting analysis for {repo_url}"})
            with st.spinner("Triggering Codebase Genius..."):
                try:
                    res = requests.post(CODEGENIUS_ENDPOINT, json={"repo_url": repo_url})
                    if res.status_code == 200:
                        st.success("Repository analysis started!")
                    else:
                        st.error(f"Error: {res.status_code} - {res.text}")
                except Exception as e:
                    st.error(f"Failed to connect to backend: {e}")
        else:
            st.warning("Please enter a valid GitHub URL")

# -------------------------------------------
# TITLE & TABS
# -------------------------------------------
st.title("🧠 Codebase Genius")
tab1, tab2, tab3 = st.tabs(["💬 Chat", "📘 Docs", "📊 Diagrams"])

# -------------------------------------------
# CHAT TAB
# -------------------------------------------
with tab1:
    chat_container = st.container()
    with chat_container:
        st.markdown('<div class="chat-scroll">', unsafe_allow_html=True)
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"], unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        if st.session_state.chat_history:
            components_html("""
                <script>
                  setTimeout(() => {
                    const el = window.parent.document.querySelector('.chat-scroll');
                    if (el) { el.scrollTop = el.scrollHeight; }
                  }, 100);
                </script>
            """, height=0)

# -------------------------------------------
# DOCS TAB
# -------------------------------------------
with tab2:
    st.header("📘 Repository Docs")
    if st.button("🔄 Refresh Docs"):
        with st.spinner("Fetching documentation..."):
            try:
                res = requests.post(GET_DOCS_ENDPOINT)
                if res.status_code == 200:
                    reports = res.json().get("reports", [])
                    docs = reports[0] if reports and isinstance(reports[0], list) else []
                    if docs:
                        for doc in docs:
                            st.markdown(f"### {doc.get('title', 'Untitled')}")
                            st.write(doc.get("content", ""))
                    else:
                        st.info("No docs found.")
                else:
                    st.error(f"Error fetching docs: {res.status_code}")
            except Exception as e:
                st.error(f"Error: {e}")

# -------------------------------------------
# DIAGRAMS TAB
# -------------------------------------------
with tab3:
    st.header("📊 Generated Diagrams")
    if st.button("🔄 Load Diagrams"):
        with st.spinner("Loading diagrams..."):
            try:
                res = requests.post(GET_DIAGRAMS_ENDPOINT)
                if res.status_code == 200:
                    reports = res.json().get("reports", [])
                    diagrams = reports[0] if reports and isinstance(reports[0], list) else []
                    if diagrams:
                        for d in diagrams:
                            st.markdown(f"#### {d.get('title', 'Diagram')}")
                            mermaid_code = d.get("content", "")
                            st.markdown(f"```mermaid\n{mermaid_code}\n```")
                    else:
                        st.info("No diagrams found.")
                else:
                    st.error(f"Error fetching diagrams: {res.status_code}")
            except Exception as e:
                st.error(f"Failed to load diagrams: {e}")
