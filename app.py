import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import streamlit as st
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders
from langchain_groq import ChatGroq
load_dotenv()


def get_pdf_data(pdf_doc):
    text = ""
    # for pdf in pdf_docs:
    pdf_reader = PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text
# create chat prompt 
system_prompt = '''You are an expert resume parser. Parse the resume given and respond  in json format only.Also normalize the parsed data.
Output:
{{
  "name": "<FULL_NAME>",
  "contact_information": {{
    "mobile": ["<PHONE_NUMBER_1>", "<PHONE_NUMBER_2>"],
    "email": "<EMAIL_ADDRESS>",
    "address": "<ADDRESS>"
  }},
  "career_objective": "<CAREER_OBJECTIVE>",
  "work_experience": [
    {{
      "position": "<POSITION_TITLE>",
      "company": "<COMPANY_NAME>",
      "duration": "<DURATION>"
    }}
  ],
  "total_experience":"<TOTAL_EXPERIENCE_IN_YEARS>"
  "education": [
    {{
      "degree": "<DEGREE>",
      "institute": "<INSTITUTE>",
      "university_or_board": "<UNIVERSITY_OR_BOARD>",
      "year": "<YEAR>",
      "division": "<DIVISION>"
    }}
  ],
  "technical_skills": {{
    "languages": ["<LANGUAGE_1>", "<LANGUAGE_2>"],
    "methodologies": ["<METHODOLOGY_1>", "<METHODOLOGY_2>"],
    "web_technology": ["<WEB_TECH_1>", "<WEB_TECH_2>"],
    "databases": ["<DB_1>", "<DB_2>"]
  }},
  "projects": [
    {{
      "name": "<PROJECT_NAME>",
      "company": "<COMPANY_NAME>",
      "description": "<PROJECT_DESCRIPTION>",
      "technologies": ["<TECHNOLOGY_1>", "<TECHNOLOGY_2>"],
      "database": ["<DATABASE_1>", "<DATABASE_2>"]
    }}
  ],
  "strengths": [
    "<STRENGTH_1>",
    "<STRENGTH_2>"
  ],
  "hobbies": [
    "<HOBBY_1>",
    "<HOBBY_2>"
  ],
  "personal_details": {{
    "father_name": "<FATHER_NAME>",
    "date_of_birth": "<DATE_OF_BIRTH>",
    "gender": "<GENDER>",
    "nationality": "<NATIONALITY>",
    "marital_status": "<MARITAL_STATUS>",
    "languages": ["<LANGUAGE_1>", "<LANGUAGE_2>"]
  }}
}}


'''
prompt = ChatPromptTemplate.from_messages(
    [
    ('system',system_prompt),
    ('user','Resume : {resume}')
    ]
)
# call Ollama llama3 model
llm = ChatGroq(model="llama3-8b-8192",disable_streaming=True,api_key=st.secrets['GROQ_API_KEY'])

#output parser
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

## streamlt framework
st.set_page_config("ResumeParser")
st.header("Resume Parser Support💁")
st.title("Resume Parser App")
resume_file = st.file_uploader('Please upload your resume')

if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_data(resume_file)
                st.write(chain.invoke({'resume': raw_text}))
                st.success("Done")

