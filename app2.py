import streamlit as st
import pandas as pd
from fuzzywuzzy import process, fuzz

# --- Streamlit Setup ---
st.set_page_config(page_title="🌾 Agro QA Chatbot", layout="wide")
st.title("🌱 Agro QA Chatbot")
st.caption("Ask anything related to farming: crops, pests, fertilizers, weather, etc.")

# --- Load and Prepare Data ---
@st.cache_data
def load_data():
    df = pd.read_parquet("0001.parquet")
    df.columns = [col.strip().lower() for col in df.columns]

    q_col = next((col for col in df.columns if "question" in col), None)
    a_col = next((col for col in df.columns if "answer" in col), None)

    if not q_col or not a_col:
        st.error("❌ Could not find 'question' and 'answer' columns in the dataset.")
        return pd.DataFrame(columns=["question", "answer"])

    df = df[[q_col, a_col]].dropna()
    df.rename(columns={q_col: "question", a_col: "answer"}, inplace=True)
    return df

df = load_data()

# --- Fuzzy Match Base ---
questions = df["question"].astype(str).tolist()
answers = df["answer"].astype(str).tolist()

# --- Initialize Chat History ---
if "chat" not in st.session_state:
    st.session_state.chat = []

# --- Input Box ---
user_input = st.text_input("💬 Ask your farming question:")

if st.button("Ask"):
    if user_input.strip():
        best_match, score = process.extractOne(user_input, questions, scorer=fuzz.token_sort_ratio)

        if score >= 70:
            matched_question = best_match
            matched_answer = answers[questions.index(matched_question)]
        else:
            matched_question = ""
            matched_answer = "🤔 Sorry, I couldn't find a relevant answer. Please rephrase."

        st.session_state.chat.append({
            "user_input": user_input,
            "matched_question": matched_question,
            "matched_answer": matched_answer
        })
    else:
        st.warning("⚠️ Please enter a question before clicking 'Ask'.")

# --- Display Chat History ---
st.markdown("### 🗨️ Chat History")
for chat in reversed(st.session_state.chat):
    st.markdown(f"**👨‍🌾 You:** {chat.get('user_input', '')}")
    if chat.get("matched_question"):
        st.markdown(f"📌 **Matched Question:** {chat.get('matched_question')}")
    st.markdown(f"🤖 **Bot:** {chat.get('matched_answer')}")

# --- Sidebar Options ---
with st.sidebar:
    st.header("⚙️ Options")
    if st.button("🧹 Clear Chat"):
        st.session_state.chat = []
        st.experimental_rerun()
