# streamlit_app.py
import streamlit as st
from jobdescription import generate_job_description
from test_creation import create_test
from resumeSelector import add_to_db,evaluate_candidates,search_resumes_ans
from scheduleMeetings import interview_meet_link
from audio_to_text import feedBackAnalysis
from startup import  ans
from video_to_audio import video_analyse

global question
global options
global answers


def main():
    st.title("Smart Recruiter")

    # Create a multiselect widget for tabs
    selected_tabs = st.sidebar.radio("Navigation", ["Post Jobs","Resume Upload","Create Test","Schedule Interview Link","Interview Transcript","Chat"])

    # Display content based on selected tabs
    if "Post Jobs" in selected_tabs:
        render_tab_1()

    if "Create Test" in selected_tabs:
        render_tab_2()
    
    if"Resume Upload" in selected_tabs:
        render_tab_4()
    
    if "Schedule Interview Link" in selected_tabs:
        render_tab_5()
    
    if "Interview Transcript" in selected_tabs:
        render_tab_6()
        
    if "Chat" in selected_tabs:
        render_tab_7()
    

def render_tab_1():
   
     st.header("Post Jobs")
     st.title("JD Form")

     # Get user inputs
     with st.form('jd'):
      company_name = st.text_input("Enter your Company Name:")
      job_title = st.text_input("Enter your JobTitle:")
      skills = st.text_input("Enter Required skillsets")
      location = st.text_input("Enter Location")
      exp=st.number_input("Enter years of experience")
      submit = st.form_submit_button("Get JD")
    
     if submit:
    
        
        generated_description = generate_job_description(job_title, company_name, skills,location,exp)
        result=generated_description.choices[0].message.content
        st.write(f"{result}")
  
     

def render_tab_2():
     st.header("Test Creation") 
     with st.form('jd'):
      topics = st.text_input("Enter Required test topic")
      submit = st.form_submit_button("Get Questions")
    
     if submit:
        global question
        global options
        global answers
        question,options,answers = create_test(topics)
        render_tab_3()

def render_tab_3():
    global question
    global options
    global answers
    st.header("Test Zone")
    for i,q in enumerate(question):
         st.write(f"{i+1}.{q}")
         st.radio("select an option",options[i],index=None)
    st.button("Send Question")  

def render_tab_4():
    st.header("Resume Zone")
    with st.form('Resume'):
     link=st.text_input("Enter the url")
     submit=st.form_submit_button("Upload")
    if submit:
        add_to_db(link)
    st.header("Eligible Candidate")
    with st.form('Select Candidate'):
        skills=st.text_input('Enter the skills')
        k=st.text_input('Enter number of profiles')
        submit=st.form_submit_button("Get Candidate")
    if submit:
           final=search_resumes_ans(skills,k)
           result=evaluate_candidates(final,skills)
           st.write(f"{result}")

def render_tab_5():
    interview_meet_link()
    
def render_tab_6():
    st.title("Interview Transcript")
    video_analyse()
    

def render_tab_7():
    st.title("Chat")
    ans()
    
        
    
    
     
if __name__ == "__main__":
    main()
   