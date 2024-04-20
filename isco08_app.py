import pandas as pd
import streamlit as st
from langchain_openai import OpenAI, ChatOpenAI
import os
from dotenv import load_dotenv

llm = OpenAI(temperature=0)

# Add title, image and header
st.title('ISCO-08 Code Generator')
st.image("assets/ess.png", width=150)
st.header('Enter your job details:')

# Questions for the user
job_title = st.text_input('1. What is the name or title of your main job?')
job_work = st.text_input('2. In your main job, what kind of work do you do most of the time?')
job_qualifications = st.text_input('3. What training or qualifications are needed for the job?')

button_clicked = st.button('Generate ISCO-08 code')

if button_clicked:
    if job_title and job_work and job_qualifications:
        # Improved prompt
        prompt = f"Could you please generate an ISCO-08 code for a job with the title '{job_title}', where the primary work responsibility is '{job_work}', and the necessary qualifications for the job are '{job_qualifications}'?"
        
        result = llm.invoke(prompt)
        st.write("LLM Response:")
        st.write(result)
    else:
        st.warning("Please answer all the questions to generate the output.")

# Footer with second image
st.markdown('---')
st.markdown(
    """
    This application was developed by Benjamin Beuster for AI testing at Sikt.
    """
)
st.image("assets/sikt.jpg", width=200)

# the app is published here: https://isco08-code-generator.streamlit.app/