import streamlit as st
from scraper import get_page_text
from ai_engine import ask_gemini

st.set_page_config(page_title="PageSense AI")

st.title("🔎 PageSense AI")
st.write("Chat with any webpage using AI")

url = st.text_input("Enter URL")

col1, col2 = st.columns(2)

with col1:
    summarize = st.button("Summarize")

with col2:
    keypoints = st.button("Key Points")

question = st.text_input("Ask a question")

if summarize:
    try:
        with st.spinner("Summarizing..."):
            content = get_page_text(url)

            answer = ask_gemini(
                content,
                "Summarize this webpage in bullet points."
            )

        st.write(answer)

    except Exception as e:
        st.error(f"Error: {e}")


if keypoints:
    try:
        with st.spinner("Finding key points..."):
            content = get_page_text(url)

            answer = ask_gemini(
                content,
                "Give the 5 most important points."
            )

        st.write(answer)

    except Exception as e:
        st.error(f"Error: {e}")


if st.button("Ask AI"):
    try:
        with st.spinner("Reading webpage and thinking..."):
            content = get_page_text(url)

            answer = ask_gemini(content, question)

        st.write("### Answer")
        st.write(answer)

    except Exception as e:
        st.error(f"Error: {e}")