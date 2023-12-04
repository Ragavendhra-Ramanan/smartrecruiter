import os
import re
from pdfminer.high_level import extract_text
import requests
import openai
import pandas as pd
import numpy as np
import faiss
global result
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

result=pd.DataFrame([{'name':'Ramanan','email':"ramananrohit4@gmail.com","phone_no":"9566797727","skills":"SQL,Angular,C#","profile":"software developer","summary":"Software developer with skills in Angular,c#,SQL"},
                     {'name':'Lakshmi','email':"lakshmi.yaseen@gmail.com","phone_no":"9566797711","skills":"Python,Data and AI","profile":"Data Scientist","summary":"Data Scientist with skills in Python,Data and AI"},
                     {'name':'Balaji','email':"balaji.prathap@gmail.com","phone_no":"9566711727","skills":"C#,Angular,Python","profile":"Data engineer","summary":"Data Engineer with skills in Angular,c#,Python"}])

def print_pdf_text(url=None, file_path=None):
    # Determine the source of the PDF (URL or local file)
    if url:
        response = requests.get(url)
        response.raise_for_status()  # Ensure the request was successful
        temp_file_path = "temp_pdf_file.pdf"
        with open(temp_file_path, 'wb') as temp_file:
            temp_file.write(response.content)  # Save the PDF to a temporary file
        pdf_source = temp_file_path
    elif file_path:
        pdf_source = file_path  # Set the source to the provided local file path
    else:
        raise ValueError("Either url or file_path must be provided.")

    # Extract text using pdfminer
    text = extract_text(pdf_source)

    # Remove special characters except "@", "+", ".", and "/"
    cleaned_text = re.sub(r"[^a-zA-Z0-9\s@+./:,]", "", text)

    # Format the text for better readability
    cleaned_text = cleaned_text.replace("\n\n", " ").replace("\n", " ")
    # If a temporary file was used, delete it
    if url and os.path.exists(temp_file_path):
        os.remove(temp_file_path)

    return cleaned_text


def pinfo_extractor(resume_text):
    context = f"Resume text: {resume_text}"
    question = """ From above candidate's resume text, extract the only following details:
                Name: (Find the candidate's full name. If not available, specify "not available.")
                Email: (Locate the candidate's email address. If not available, specify "not available.")
                Phone Number: (Identify the candidate's phone number. If not found, specify "not available.")
                Years of Experience: (If not explicitly mentioned, calculate the years of experience by analyzing the time durations at each company or position listed. Sum up the total durations to estimate the years of experience. If not determinable, write "not available.")
                Skills Set: Extract the skills which are purely technical and represent them as: [skill1, skill2,... <other skills from resume>]. If no skills are provided, state "not available."
                Profile: (Identify the candidate's job profile or designation. If not mentioned, specify "not available.")
                Summary: provide a brief summary of the candidate's profile without using more than one newline to segregate sections.
                """

    prompt = f"""
        Based on the below given candidate information, only answer asked question:
        {context}
        Question: {question}
    """
    # print(prompt)
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful HR recruiter."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=700,
        temperature=0.5,
        n=1  # assuming you want one generation per document
    )
    # Extract the generated response
    response_text = response.choices[0].message.content 
    print(response_text)
    # Split the response_text into lines
    lines = response_text.strip().split('\n')

    name = lines[0].split(': ')[1]
    email = lines[1].split(': ')[1]
    phone_no = lines[2].split(': ')[1]
    years_of_expiernce = lines[3].split(': ')[1]
    skills = lines[4].split(': ')[1]
    profile = lines[5].split(': ')[1]
    summary = lines[6].split(': ')[1]
    data_dict = {
        'name': name,
        'email': email,
        'phone_no': phone_no,
        'years_of_expiernce': years_of_expiernce,
        'skills': skills,
        'profile': profile,
        'summary': summary
    }
    print(data_dict, "\n")
    return data_dict;
def get_embedding(text, model="text-embedding-ada-002"):
    text = text.split("\n")
    response = openai.embeddings.create(input=text, model=model)
    return response.data[0].embedding

def add_to_db(url):
    resume_text = print_pdf_text(url=url).replace('\n',' ')
    print("Resume Text extracted\n")
    ip_data_dict = pinfo_extractor(resume_text)
    print("Information extracted\n")
    global result
    df_to_append = pd.DataFrame(ip_data_dict,index=[len(result)])
    # Append the new data to the original DataFrame
   
    result = pd.concat([result,df_to_append],axis=0, ignore_index=True)
    st.write(result)
    getSummary=result.summary.tolist()
    res=[]
    for summary in getSummary:
       res.append(get_embedding(summary))
    dim=len(res[0])
    global index
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(res).reshape(-1,dim))
    
def search_resumes_ans(query,k):
    query_embed = get_embedding(query)
    global index
    svec = np.array(query_embed).reshape(1,-1)
    distances, I = index.search(svec,k=int(k))
    row_indices = I.tolist()[0]
    print(row_indices)
    global result
    final= result.iloc[row_indices] 
    return final[['name','summary']].values.tolist() 

def evaluate_candidates(final,query):
    result=final
    responses = []  # List to store responses for each candidate
    for resume_str in result:
        name = resume_str[0]
        context = f"Resume text: {resume_str[1]}"
        question = f"What percentage of the job requirements does the candidate meet for the following job description? answer in 3 lines only and be effcient while answering: {query}."
        prompt = f"""
            Read below candidate information about the candidate:
            {context}
            Question: {question}
        """
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a expert HR analyst and recuriter."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.2,
            n=1  # assuming you want one generation per document
        )
        # Extract the generated response
        response_text = response.choices[0].message.content # response['choices'][0]['message']['content']
        responses.append((name, response_text))  # Append the name and response_text to the responses list
    return responses
