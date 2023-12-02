import openai

openai.api_key = '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'

def generate_job_description(job_title, company_name, skills_required):
    conversation = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Create a job description for the position of {job_title} at {company_name}. The ideal candidate should have the following skills: {skills_required}."}
    ]

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # You may need to adjust the model based on availability
        messages=conversation,
        max_tokens=200
    )
    return response
    job_description = response['choices'][0]['message']['content']
    return job_description

# Example usage
job_title = "Software Engineer"
company_name = "TechCo"
skills_required = "Python, Java, SQL, problem-solving"
