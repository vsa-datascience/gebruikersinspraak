import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from transformers import BertTokenizer, TFBertForSequenceClassification
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.data import Dataset

# Sample DataFrame
data = {'Questions': ["What percentage of people prefer cats over dogs?",
                      "How many students scored above 90% in the exam?",
                      "What is the average height of adults in the population?",
                      "When was the last census conducted?",
                      "Do you like pizza?"]}
df = pd.DataFrame(data)
print(df)
# Label the questions (1 for numerical, 0 for non-numerical)
df['IsNumerical'] = [1, 1, 1, 0, 0]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df['Questions'], df['IsNumerical'], test_size=0.2, random_state=42)

# Load pre-trained BERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = TFBertForSequenceClassification.from_pretrained('bert-base-uncased')

# Tokenize and encode sequences
X_train_tokens = tokenizer(list(X_train), padding=True, truncation=True, return_tensors='tf', max_length=64)
X_test_tokens = tokenizer(list(X_test), padding=True, truncation=True, return_tensors='tf', max_length=64)

# Convert to TensorFlow Dataset
train_dataset = Dataset.from_tensor_slices((dict(X_train_tokens), np.array(y_train)))
test_dataset = Dataset.from_tensor_slices((dict(X_test_tokens), np.array(y_test)))

# Fine-tune the BERT model for sequence classification
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(train_dataset.batch(2), epochs=3, validation_data=test_dataset.batch(2))

# Evaluate the model
results = model.evaluate(test_dataset.batch(2), verbose=0)
print(f"Accuracy: {results[1]}")

# Example: Classify a new question
new_question = ["How many books are in the library?"]
new_question_tokens = tokenizer(new_question, padding=True, truncation=True, return_tensors='tf', max_length=64)
prediction_new = model.predict(dict(new_question_tokens))['logits'][0][0]
print(f"Is the new question numerical? {prediction_new > 0.5}")
