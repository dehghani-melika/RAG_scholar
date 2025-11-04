from openai import OpenAI
import requests
import fitz 
from fastapi import FastAPI
from pydantic import BaseModel
import json
import uvicorn

# url = "https://arxiv.org/pdf/1706.03762.pdf"

def extract_pdf_url(url):
    res = requests.get(url, stream=True)

    if res.status_code == 200:
        # Save PDF temporarily or process directly from bytes
        pdf_document = fitz.open(stream=res.content, filetype="pdf")
        # Extract text from all pages
        full_text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            full_text += page.get_text()
        
        # print(full_text[:1000])  # Print first 1000 characters
        pdf_document.close()
    else:
        print("❌ Failed to download PDF")

    return full_text


# -------------------------------------   create api

app = FastAPI()

from dotenv import load_dotenv
import os 

load_dotenv()
API_KEY = os.environ['OPENAI_API_KEY']

# class PromptRequest(BaseModel):
#     prompt: str

def call_llm(prompt: str) -> str:

    client = OpenAI(api_key=API_KEY)
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a professor"},
        {"role": "user", "content": prompt}
    ]
    )
    response = completion.choices[0].message.content
    return response


@app.post("/getPdfContent/")
async def generate_response(data: dict):
    url_flag = data.get("url_flag", False)
    user_input = data.get("user_input", "")
    summary_request = data.get("summary_request", False)

    if url_flag:
        pdf_text = extract_pdf_url(user_input)
    else:
        pdf_text = user_input

    if summary_request:
        prompt = "give a summary of this paper: \n" + pdf_text
    else:
        prompt = "give a main idea of this paper: \n" + pdf_text
        
    response = call_llm(prompt)
    print(f"User Prompt: {response}")
    
    return {"response": response}

#  uvicorn extract-info-paper:app --host localhost --port 80
# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000) 
