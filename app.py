from rag import create_vector_store
import streamlit as st
from scraper import get_page_text
from ai_engine import ask_gemini
import time

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="PageSense AI",
    page_icon="🚀",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

/* Background */
.main {
    background-color: #F8FAFC;
}

/* Page spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Buttons */
.stButton > button {
    width: 100%;
    background-color: #7C3AED;
    color: white;
    border-radius: 12px;
    border: none;
    padding: 0.7rem;
    font-weight: 600;
    transition: 0.3s;
}

.stButton > button:hover {
    background-color: #6D28D9;
}

/* Inputs */
.stTextInput input {
    border-radius: 12px;
}

/* Selectbox */
div[data-baseweb="select"] {
    border-radius: 12px;
}
footer {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}

header {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

with st.sidebar:

    st.markdown("#  PageSense AI")

    st.markdown("---")

    st.markdown("""
    ###  About

    Transform any webpage into:

    - Notes
    - Viva Answers
    - Exam Solutions
    - Assignments

    ### ⚙️ Tech Stack

    - Gemini
    - FAISS
    - Sentence Transformers
    - Streamlit
    """)

    st.markdown("---")

    st.success("Ready to Learn ")

# --------------------------------------------------
# HERO SECTION
# --------------------------------------------------

st.markdown("""
<div style='text-align:center;padding:30px;'>

<h1 style='font-size:48px;margin-bottom:0px;'>
  PageSense AI
</h1>

<h3 style='color:#64748B;margin-top:10px;'>
Transform Any Webpage Into Study Material
</h3>

<p style='color:#64748B;font-size:18px;'>
Learn, summarize and study any webpage using AI
</p>

</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "index" not in st.session_state:
    st.session_state.index = None

if "chunks" not in st.session_state:
    st.session_state.chunks = None

if "processed_url" not in st.session_state:
    st.session_state.processed_url = None

# --------------------------------------------------
# URL INPUT
# --------------------------------------------------

st.markdown("###  Webpage URL")

url = st.text_input(
    "",
    placeholder="Paste any webpage URL here..."
)

# --------------------------------------------------
# PROCESS WEBPAGE
# --------------------------------------------------

if st.button(" Analyze Webpage"):

    if not url:
        st.error("Please enter a URL first.")

    else:
        try:
            with st.spinner("Creating knowledge base..."):

                content = get_page_text(url)
                
                index, chunks = create_vector_store(content)
                
                st.session_state.index = index
                st.session_state.chunks = chunks
                st.session_state.processed_url = url


        except Exception as e:
               st.error(f"Error: {e}")

if st.session_state.index is not None:
# --------------------------------------------------
# QUESTION + MODE
# --------------------------------------------------

        st.markdown("---")

        left, right = st.columns([3, 1])

        with left:

            st.markdown("###  Ask a Question")

            question = st.text_input(
                "",
                placeholder="Ask anything about the webpage..."
            )

        with right:


            mode = st.radio(
                " Study Mode",
            [
                "Normal",
                "Viva",
                "Exam",
                "Assignment",
                "Notes"
            ],
            horizontal=True
            )

        # --------------------------------------------------
        # WORD LIMIT
        # --------------------------------------------------

        word_limit = None

        if mode == "Assignment":

            word_limit = st.number_input(
                "Word Limit",
                min_value=50,
                max_value=2000,
                value=400
            )

        # --------------------------------------------------
        # QUICK ACTIONS
        # --------------------------------------------------

        st.markdown("###  Quick Actions")

        col1, col2, col3 = st.columns(3)

        with col1:
            summarize = st.button(" Summary")

        with col2:
            keypoints = st.button(" Key Points")

        with col3:
            exam_topics = st.button(" Exam Topics")
        if exam_topics:

            if st.session_state.index is None:
                st.error("Please click Analyze Webpage first.")

            else:
                try:

                    with st.spinner("Generating exam topics..."):

                        answer = ask_gemini(
                            "Generate important exam topics from this webpage.",
                            st.session_state.index,
                            st.session_state.chunks,
                            mode,
                            word_limit
                        )

                    st.markdown("##  Important Exam Topics")
                    st.write(answer)

                except Exception as e:
                    st.error(f"Error: {e}")

        # --------------------------------------------------
        # SUMMARIZE
        # --------------------------------------------------

        if summarize:

            if st.session_state.index is None:
                st.error("Please click Analyze Webpage first.")

            else:
                try:

                    with st.spinner("Generating summary..."):

                        answer = ask_gemini(
                            "Summarize this webpage.",
                            st.session_state.index,
                            st.session_state.chunks,
                            mode,
                            word_limit
                        )

                    st.markdown("##  Summary")
                    st.write(answer)

                except Exception as e:

                    if "429" in str(e):
                        st.error(
                            " Gemini API limit reached. Please try again later."
                        )
                    else:
                        st.error(f"Error: {e}")

        # --------------------------------------------------
        # KEY POINTS
        # --------------------------------------------------

        if keypoints:

            if st.session_state.index is None:
                st.error("Please click Analyze Webpage first.")

            else:
                try:

                    with st.spinner("Finding key points..."):

                        answer = ask_gemini(
                            "Give the 5 most important points from this webpage.",
                            st.session_state.index,
                            st.session_state.chunks,
                            mode,
                            word_limit
                        )

                    st.markdown("## Key Points")
                    st.write(answer)

                except Exception as e:

                    if "429" in str(e):
                        st.error(
                            "Gemini API limit reached. Please try again later."
                        )
                    else:
                        st.error(f"Error: {e}")

        # --------------------------------------------------
        # ASK AI
        # --------------------------------------------------

        if st.button(" Ask PageSense AI"):

            if not url:
                st.error("Please enter a URL first.")

            elif not question:
                st.error("Please enter a question.")

            elif st.session_state.index is None:
                st.error("Please click Analyze Webpage first.")

            else:
                try:

                    with st.spinner("Thinking..."):

                        answer = ask_gemini(
                            question,
                            st.session_state.index,
                            st.session_state.chunks,
                            mode,
                            word_limit
                        )

                    st.markdown("## Answer")
                    st.write(answer)

                except Exception as e:

                    if "429" in str(e):
                        st.error(
                            " Gemini API limit reached. Please try again later."
                        )
                    else:
                        st.error(f"Error: {e}")