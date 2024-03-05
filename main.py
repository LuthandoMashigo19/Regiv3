import streamlit as st
import google.generativeai as gen_ai
import os
import PyPDF2

GOOGLE_API_KEY = ("AIzaSyAzvYjga2f7OBF-_F3lOa8FekGtZb3Wo9U")
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

chat = model.start_chat()
extractedtext = ""


def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ''
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text()
    return text


st.title("Regi v2")

uploaded_file = st.file_uploader("Upload your doucment")

# if uploaded_file:
#     extractedtext = extract_text_from_pdf(uploaded_file)
#     st.write(extractedtext)

if "messages" not in st.session_state:
    st.session_state["messages"] = [{
        "role":
        "assistant",
        "content":
        "Hello! How can I help you today?"
    }]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if uploaded_file:
        newprompt = prompt + " : " + extractedtext
        genAIRes = chat.send_message(newprompt)

    else:
        genAIRes = chat.send_message(prompt)

    response = genAIRes.text
    # msg = response.choices[0].message.content
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })
    st.chat_message("assistant").write(response)
