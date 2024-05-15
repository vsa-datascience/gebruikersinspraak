import pandas as pd
import re

# Sample DataFrame
# data = {'Questions': ["What percentage of people prefer cats over dogs?",
#                       "How many students scored above 90% in the exam?",
#                       "What is the average height of adults in the population?",
#                       "When was the last census conducted?",
#                       "Do you like pizza?"]}

data = {'vragen': ["Wat is het percentage mensen dat katten boven honden verkiest?",
                      "Hoeveel studenten scoorden meer dan 90%?",
                      "Wat is de gemiddelde lengte in de Vlaamse bevolking?",
                      " Wanneer is de laatste census uitgevoerd?",
                      "Houd je van pizza?"]}

df = pd.DataFrame(data)

# Function to check if a question is related to numerical information using regex
def is_numerical_question(text):
    numerical_keywords = r'\b(?:gemiddeld|gemiddelde|mediaan|percent|percentage|aantal|hoeveel)\b'
    # numerical_keywords = r'\b(?:how (?:many|much)|average|median|percentage)\b'

    return bool(re.search(numerical_keywords, text, flags=re.IGNORECASE))

# Apply the function to the 'Questions' column and create a new column 'IsNumerical'
df['IsNumerical'] = df['vragen'].apply(is_numerical_question)

# Display the DataFrame
print(df)
