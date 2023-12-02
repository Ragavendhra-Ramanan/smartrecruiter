# streamlit_app.py
import streamlit as st
from jobdescription import generate_job_description

def main():
    st.title("User Input Form")

    # Get user inputs
    company_name = st.text_input("Enter your Company Name:")
    job_title = st.text_input("Enter your JobTitle:")
    skills = st.text_input("Enter Required skillsets")
    
    try:
        generated_description = generate_job_description(job_title, company_name, skills)
        print(generated_description)
        st.write(f"JOB DESCRIPTION: {generated_description}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
