import streamlit as st
import json
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Load knowledge base
with open("Farming_QA.json", "r", encoding="utf-8") as f:
    knowledge_base = json.load(f)

# Extract list of all Questions
Questions = [item["Question"] for item in knowledge_base]

# Chat history using session state
if "chat" not in st.session_state:
    st.session_state.chat = []

# Title
st.set_page_config(page_title="Farmer AI Chatbot", layout="wide")
st.markdown(
    """
    <style>
    body {
        background-color: #1e1e1e;
        color: white;
    }
    .block-container {
        padding-top: 2rem;
    }
    .chatbox {
        background-color: #262730;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
    }
    .user-msg {
        background-color: #2e2f3a;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 5px;
    }
    .bot-msg {
        background-color: #40414f;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🌾 Farmer AI Chatbot")
st.caption("Ask me anything related to rice diseases, fertilizers, weather, and more.")

# Sidebar for history
with st.sidebar:
    st.header("🕘 Chat History")
    for i, msg in enumerate(st.session_state.chat):
        st.write(f"**Q{i+1}:** {msg['Question']}")
    if st.button("Clear History"):
        st.session_state.chat = []
        st.experimental_rerun()

# Main input area
query = st.text_input("💬 Ask your Question about rice farming...")

if st.button("Ask"):
    if query.strip() == "":
        st.warning("Please type a Question.")
    else:
        # Fuzzy match the best Question from the database
        best_match, score = process.extractOne(query, Questions, scorer=fuzz.token_sort_ratio)

        # Threshold (e.g., 60) to ignore irrelevant Questions
        if score >= 60:
            for item in knowledge_base:
                if item["Question"] == best_match:
                    Answer = item["Answer"]
                    break
        else:
            Answer = "🤔 Sorry, I couldn't understand your Question. Please rephrase it."

        # Save chat
        st.session_state.chat.append({
            "Question": query,
            "Answer": Answer
        })

# Show chat history (like ChatGPT)
st.markdown("### 💬 Conversation")
for msg in reversed(st.session_state.chat):
    st.markdown(f'<div class="user-msg">👤 **You:** {msg["Question"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="bot-msg">🤖 **Bot:** {msg["Answer"]}</div>', unsafe_allow_html=True)
