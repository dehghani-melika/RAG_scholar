import streamlit as st
import json
import requests
from pypdf import PdfReader

st.title("ask your question")

with st.chat_message("user"):
    st.write("Hello 👋")

# prompt = st.chat_input("Say something")

option = st.selectbox('pick one', ["upload file","enter url"], index=None)
url_flag = False
user_input = None

if option == "upload file":
    pdf = st.file_uploader("enter yoour pdf file",type=["pdf"])
    if pdf is not None:
        # st.write("option is", pdf)
        reader = PdfReader(pdf)
        # st.write("option is", help(reader))
        full_text = ''
        for i in range (len(reader.pages)):
            full_text += reader.pages[i].extract_text()
        # if full_text.strip():
        #     st.subheader("📘 Full text extracted from PDF:")
        #     st.write(full_text)

        url_flag = False    
        user_input = full_text

elif option == "enter url"  :   
    pdf_url = st.text_input("Enter PDF URL:")
    if pdf_url is not None:
        url_flag = True
        user_input = pdf_url


def get_user_input():
        option = ''
        option = st.selectbox('pick one', ["upload file","enter url"], index=None)
        # st.write("option is", option)
        url_flag = False
    
        if option == "upload file":
            pdf = st.file_uploader("enter yoour pdf file",type=["pdf"])
            if pdf is not None:
                # st.write("option is", pdf)
                reader = PdfReader(pdf)
                # st.write("option is", help(reader))
                full_text = ''
                for i in range (len(reader.pages)):
                    full_text += reader.pages[i].extract_text()
                if full_text.strip():
                    st.subheader("📘 Full text extracted from PDF:")
                    st.write(full_text)
                return url_flag, full_text
            else:
                # print("pdf is None")
                pass

        elif option == "enter url"  :   
            pdf_url = st.text_input("url_file ", value="", placeholder="enter your url")
            if pdf_url is not None:
                print("pdf_url")
                url_flag = True
                return url_flag, pdf_url
            else:
                pass
            
        
# # get_user_input()
# st.write("get_user_input() is", get_user_input())

if st.button("🔍 Get Summary") and user_input:
    summary_request = True
    with st.spinner("Summarizing..."):
        res = requests.post(
            "http://backend:8000/getPdfContent/",
            json={"url_flag": url_flag, "user_input": user_input, "summary_request":summary_request},
        )
        if res.status_code == 200:
            st.subheader("🧠 Summary:")
            st.write(res.json()["response"])
        else:
            st.error("Failed to connect to the backend.")

if st.button("🔍 Get main idea") and user_input:
    summary_request = False
    with st.spinner("Geting main idea..."):
        res = requests.post(
            "http://backend:8000/getPdfContent/",
            json={"url_flag": url_flag, "user_input": user_input, "summary_request":summary_request},
        )
        if res.status_code == 200:
            st.subheader("🧠 Main idea:")
            st.write(res.json()["response"])
        else:
            st.error("Failed to connect to the backend.")

