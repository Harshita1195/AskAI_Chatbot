# Import Libraries
import os
import streamlit as st

from dotenv import load_dotenv
load_dotenv() #load all environment variables from .env

import google.generativeai as genai

# configuring API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## function to load Gemini Pro model and get response
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

st.set_page_config(page_title="AskAi")

st.header("AskAi: Conversational AI chatbot with Gemini Pro")

# initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history']=[]

input = st.text_input("Input:", key="input")

submit = st.button("Submit")

# if submit button is clicked
if submit and input:
    response = get_gemini_response(input)

    # add user query and response to session chat history.
    st.session_state['chat_history'].append(("You", input))
    st.subheader("The response is:")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))

st.subheader("The chat history is:")

for role,text in st.session_state['chat_history']:
    st.write(f"{role}:{text}")