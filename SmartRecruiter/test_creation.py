from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

def create_test(subject):
  # your OpenAI key saved in the “OPENAI_API_KEY” environment variable.
 chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
 template="You are an interviewer who asks 3 question from each topic  using  multiple choice based and also display answers for each at last."
 #template = "You are an interviewer who asks 3 questions from each topic and with multiple choice question and display the option in newline seperately with  the answers at the last "
 system_message_prompt = SystemMessagePromptTemplate.from_template(template)
 human_template = "Ask question about the  {subject}."
 human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

 chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

 response = chat(chat_prompt.format_prompt(subject=subject).to_messages())

 ans= response.content
 # Split the text into questions, options, and answers
 question_blocks = ans.split('\n\n')

 questions = []
 options = []
 answers = []

 for block in question_blocks[:-1]:
    lines = block.strip().split('\n')
    questions.append(lines[0].strip())
    options.append([option.strip() for option in lines[1:]])

 answers.append(question_blocks[-1].strip().split('\n')[1:])

 f_ques=[ques[2:] for ques in questions]
 f_option=[[opt[2:].strip() for opt in opts] for opts in options]
 f_answers=[[ans[5:].strip() for ans in answer] for answer in answers][0]
 return f_ques,f_option,f_answers