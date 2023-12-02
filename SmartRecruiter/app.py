# streamlit_app.py
import streamlit as st
from jobdescription import generate_job_description

def main():
    st.title("User Input Form")

    # Get user inputs
    company_name = st.text_input("Enter your Company Name:")
    job_title = st.text_input("Enter your JobTitle:")
    skills = st.text_input("Enter Required skillsets")
    submit = st.form_submit_button("Get JD")
    
    if submit:
    
      try:
        generated_description = generate_job_description(job_title, company_name, skills)
        result=generated_description.choices[0].message.contentgenerated_description
        st.write(f"JOB DESCRIPTION: {result}")
      except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
