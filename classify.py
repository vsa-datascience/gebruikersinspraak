from openai import OpenAI
from dotenv import load_dotenv
import os
import pandas as pd
import re 

load_dotenv()
sourcefolder = f"questions/parlementaire_vragen.csv"
targetfolder = f"labeled/parlementaire_vragen.csv"

api_key = os.getenv('SECRET_KEY')
client = OpenAI(
  api_key=api_key,
)


def llm_classify(question, client):
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
    
    completion = client.chat.completions.create(
        model="gpt-4",
        # model="gpt-3.5-turbo",
        temperature = 0.0,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": content,
            }
        ]
    )

    label = (completion.choices[0].message.content)
    return label



# read file with questions
df = pd.read_csv(sourcefolder)
# classify each question  
df['label'] = df['vraag'].apply(llm_classify, args=(client,))
# file to csv
df.to_csv(targetfolder, index = False)