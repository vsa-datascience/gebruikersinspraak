from openai import OpenAI
from dotenv import load_dotenv
import os
import pandas as pd
import re 

load_dotenv()
sourcefolder = f"documents/"
txt_files = os.listdir(sourcefolder)
txt_files.remove(".ipynb_checkpoints")
txt_files = txt_files
# print(txt_files)

def retrieve_questions_for_file(f):
    file_path = "documents/" + f
    with open(file_path, 'r') as file:
        file_content = file.read()
        file_content = file_content.replace('\n', ' ')
    
    return file_content



def find_questions(text_with_questions):
        # pattern = r'\b.*\?'
        # questions = re.findall(pattern, text_with_questions)
        
        sentences = re.split(r'(?<=[.!?])\s+', text_with_questions)
        pattern = r'\b.*\?'
        questions = []
        for sentence in sentences:
            match = re.match(pattern, sentence)
            if match:
                questions.append(match.group())
                
        return questions
    
    
def llm_call(text_with_questions, client):
    # print(text_with_questions)
    
    prompt = f"""
                Retrieve all the questions that are asked in the sources below. If the quesion itself does not contain enough information to be able the answer 
                by only reading the question, use the information in the sources and only the infomation present in that sources to rewrite the question such 
                that question contains all the necessary information by itself to be able to answer it fully. 
                The answers should be in  the language the text is written in.
                Respond by returning the following format: Q1: question 1, Q2: question 2, Q3: question 3, Q4: question 4, ...
                sources: {text_with_questions}
                your answer:
    """
    
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        # temperature = 0.0,
        messages=[
            # {"role": "system", "content": f"{prompt}"},
            # {"role": "user", "content": f"{text_with_questions}"}
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": prompt,
            }
        ]
    )

    questions_out = (completion.choices[0].message.content)
    # print(completion.choices[0].message.content)
    return (completion.choices[0].message.content)


api_key = os.getenv('SECRET_KEY')

client = OpenAI(
  api_key=api_key,
)

# prompt = f""""You are question retriever from texts. Retrieve the questions asked in this text, and if the question themselves don't contain much information, rewrite the question such that they contain the information from the text, make sure you only take information from the provided text. The output should be a python list of only the questions."""

# prompt = f""""You are question retriever from texts. Retrieve all the sentences that end with a question mark '?'. No sentences without question marks can be slected. The output should be a python list of only the questions."""



quesions_list = []
for f in txt_files[0:20]:
    text_with_questions = retrieve_questions_for_file(f)
    questions_out_llm = llm_call(text_with_questions, client)
    # print(questions_out_llm)
    questions_list = questions_out_llm.split("\n")
    # questions_out = find_questions(text_with_questions)
    # print(questions_out)
    df = pd.DataFrame()
    df['vraag'] = questions_list
    quesions_list.append(df)


all_questions =  pd.concat(quesions_list, axis=0)

print(all_questions)
all_questions.to_csv('questions/parlementaire_vragen.csv', index =False)


