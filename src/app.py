
import streamlit as st
from qa import GroundedQA

import streamlit as st

st.markdown(
    """
    <style>
    /* App background (BEIGE ONLY) */
    .stApp {
        background-color: #f6f1eb;
        color: #2b2b2b;
    }

    section.main > div {
        background-color: #f6f1eb;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #f6f1eb;
        border-right: 1px solid #e0d5cc;
    }

    /* Cards / content blocks (RUST ORANGE) */
    div[data-testid="stMarkdownContainer"] > div {
        background-color: #c65d3a;
        color: #ffffff;
        border-radius: 16px;
        padding: 18px;
        border: none;
    }

    /* Stats cards */
    div[data-testid="metric-container"] {
        background-color: #c65d3a;
        color: #ffffff;
        border-radius: 16px;
        padding: 16px;
        border: none;
    }

    /* Input boxes (light beige only here) */
    input {
        background-color: #fbf7f2 !important;
        border-radius: 10px !important;
        border: 1px solid #d7b3a6 !important;
        color: #2b2b2b !important;
    }

    /* Buttons (DARK RUST ORANGE) */
    button {
        background-color: #a4472c !important;
        color: #ffffff !important;
        border-radius: 12px;
        border: none;
        padding: 0.5rem 1.4rem;
        font-weight: 600;
    }

    button:hover {
        background-color: #8f3c24 !important;
    }

    /* Headings */
    h1, h2, h3 {
        color: #2b2b2b;
    }
    </style>
    """,
    unsafe_allow_html=True,
)





st.set_page_config(
    page_title="Advanced Local Search",
    layout="wide",
)

st.title("🔍 Advanced Local Knowledge Search")
st.caption("MMR • Reranking • Fully Local • Explainable")

qa = GroundedQA()

# Sidebar filters
st.sidebar.header("Filters")
file_type = st.sidebar.selectbox(
    "File type",
    options=["all", "md", "pdf", "csv", "docx"],
)

# Main input
question = st.text_input(
    "Ask a question about your documents:",
    placeholder="What is Retrieval-Augmented Generation?",
)

if st.button("Search"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Searching knowledge base..."):
            result = qa.answer(question)

        # ---------- Layout ----------
        col1, col2 = st.columns([3, 1])

        # ---------- Answer ----------
        with col1:
            st.subheader("✅ Answer")
            st.markdown(
                f"""
                <div style="padding:15px;border-radius:12px">

                {result["answer"]}
                </div>
                """,
                unsafe_allow_html=True,
            )

        # ---------- Confidence ----------
        def estimate_confidence(sources):
            unique_files = len(set(s["file"] for s in sources))
            if unique_files >= 3:
                return "🟢 High"
            elif unique_files == 2:
                return "🟡 Medium"
            else:
                return "🔴 Low"

        confidence = estimate_confidence(result["sources"])
        st.markdown(f"### 🔐 Confidence: **{confidence}**")

        # ---------- Stats ----------
        with col2:
            st.subheader("📊 Stats")
            st.metric("Retrieved", result["stats"]["retrieved_chunks"])
            st.metric("Used", result["stats"]["reranked_chunks"])
            st.metric("Total Time (s)", result["stats"]["total_time_sec"])

        # ---------- Sources ----------
        st.subheader("📚 Sources Used")

        grouped = {}
        for src in result["sources"]:
            grouped.setdefault(src["file"], []).append(src["chunk_id"])

        for file, chunks in grouped.items():
            st.markdown(
                f"- **{file}** → chunks: `{', '.join(chunks)}`"
            )
