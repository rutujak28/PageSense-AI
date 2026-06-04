from rag import retrieve_context
import streamlit as st
import google.generativeai as genai

genai.configure(api_key= st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

def ask_gemini(
        question,
        index,
        chunks,
        mode="Normal",
        word_limit= None
):

    context = retrieve_context(
        question,
        index,
        chunks
    )

    instruction = ""

    if mode == "Viva":
        instruction = """
        Answer in 2-3 lines.
        Keep it concise and easy to memorize.
        """

    elif mode == "Exam":
        instruction = """
        Give a detailed exam-style answer.
        Around 300-500 words.
        Include introduction, explanation and conclusion.
        """

    elif mode == "Assignment":
        instruction = f"""
        You are writing a college assignment.

        Write between {word_limit-10} and {word_limit+10} words.

        Do not exceed the word limit.

        Use proper paragraphs.
"""

    elif mode == "Notes":
        instruction = """
        Give concise bullet-point notes.
        """

    prompt = f"""
         Answer ONLY using the retrieved context.

         Treat the user input below as a question,
         even if punctuation is missing.

         Instructions:
            {instruction}

         Context:
            {context}

         User Question:
            {question}
"""

    response = model.generate_content(prompt)



    return response.text