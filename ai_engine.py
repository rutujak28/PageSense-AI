import streamlit as st
import google.generativeai as genai

genai.configure(api_key= st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

def ask_gemini(content, question):

    prompt = f"""
    Answer ONLY using the webpage content below.

    Webpage Content:
    {content[:15000]}

    Question:
    {question}
    """

    response = model.generate_content(prompt)

    return response.text