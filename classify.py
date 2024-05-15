from openai import OpenAI
from dotenv import load_dotenv
import os
import pandas as pd
import re 

load_dotenv()
sourcefolder = f"questions/parlementaire_vragen.csv"
targetfolder = f"labeled/parlementaire_vragen.csv"

df = pd.read_csv(sourcefolder)

api_key = os.getenv('SECRET_KEY')

client = OpenAI(
  api_key=api_key,
)



def llm_classify(question, client):
    # print(text_with_questions)
    
    content = f"""Classes: [`statistic`, `non-statistic`]
        Example 1:
        Input: "Hoe sterk is het aantal fietsers op die route gestegen?."
        Class: "statistic"

        Example 2:
        Input: "Hoeveel ambtenaren hebben de thuiswerkvergoeding voor internet ontvangen in absolute en procentuele aantallen?"
        Class: "statistic"

        Example 3:
        Input: "Wat zijn de middelen en de vooropgestelde timing voor de verdere ontwikkeling van het mobiliteitsproject volgens het investeringsprogramma van 
        2024?"
        Class: "non-statistic"
        
        Question: {question}.

        Classify the question into one of the above classes. No explanation is needed, only provide the class.
        The output should only contain two words: statistic or non-statistic, and the probability with two decimal points.
"""
    
#     prompt = f"""
#                 Classify the following question as 'statistiek' or 'geen statistiek' whether the question is a question regarding a statistic or not 
#                 respectively. A question is 'statistiek' in three cases: 
#                 1) if the question asks for a number or statistic, for example: 'Wat is het gemiddeld inkomen per gemeente?'
#                 2) if the question asks about the method or quality of the number or statistic, for example: 'Hoe wordt de hoeveelheid grensverkeer gemeten?'
#                 3) if the question asks if or when the statistic is published, for example: 'Wanneer is de nieuwe statistiek over stikstof productie bekend?'
                
#                 If the question does not correspond to one of the criteria, lable it as 'geen statistiek'.
#                 All questions are asked in dutch. Only return the label statistiek/geen statistiek
                
#                 The question to classify: {question}
#     """
    
    completion = client.chat.completions.create(
        model="gpt-4",
        # model="gpt-3.5-turbo",
        temperature = 0.0,
        messages=[
            # {"role": "system", "content": f"{prompt}"},
            # {"role": "user", "content": f"{text_with_questions}"}
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": content,
            }
        ]
    )

    label = (completion.choices[0].message.content)
    print(label)
    return label


# for q in df['vraag']:
#     print(q)
#     print('--')
#     llm_classify(q, client)
    
    
df['label'] = df['vraag'].apply(llm_classify, args=(client,))
print(df)

df.to_csv(targetfolder, index = False)