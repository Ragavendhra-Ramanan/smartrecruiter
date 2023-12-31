import openai
from dotenv import load_dotenv

load_dotenv()
def generate_job_description(job_title, company_name, skills_required,location,exp):
    conversation = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Create a job description for the position of {job_title} at {company_name} in location {location}. The ideal candidate should have the following skills: {skills_required} with 6 responsibilities also with preivous experience of {exp} years"}
    ]

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # You may need to adjust the model based on availability
        messages=conversation,
        max_tokens=200
    )
    return response

