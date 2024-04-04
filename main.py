import streamlit as st
import google.generativeai as gen_ai
import os
import PyPDF2

GOOGLE_API_KEY = ("AIzaSyAzvYjga2f7OBF-_F3lOa8FekGtZb3Wo9U")
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

chat = model.start_chat()
extractedtext = ""

#Set background image
background_img = """
<style>
        /*  Animation */
        .bg {
          animation:slide 3s ease-in-out infinite alternate;
          background-image: linear-gradient(-60deg, #050708 50%, #09f 50%); /* Balck and blue blend*/
          bottom:0;
          left:-50%;
          opacity:.5;
          position:fixed;
          right:-50%;
          top:0;
          z-index:-1;
        }

        .bg2 {
          animation-direction:alternate-reverse;
          animation-duration:4s;
        }

        .bg3 {
          animation-duration:5s;
        }

        @keyframes slide {
          0% {
            transform:translateX(-25%);
          }
          100% {
            transform:translateX(25%);
          }
        }
        
        body {
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: #f5f5f5; /* Light grey background */
            position: relative; /* Added to position the navbar */
        }
        
</style>
<html>
    <body>
        <div class="bg"></div>
        <div class="bg bg2"></div>
        <div class="bg bg3"></div>
    </body>
</html>
"""

st.markdown(background_img,unsafe_allow_html=True)


def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ''
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text()
    return text


st.title("Sales Proposal Generator")

uploaded_file = st.file_uploader("Upload your doucment")

if uploaded_file:
    extractedtext = extract_text_from_pdf(uploaded_file)
    # st.write(extractedtext)

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

    if extractedtext:
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
