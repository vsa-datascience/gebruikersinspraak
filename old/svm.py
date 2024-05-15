import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# Sample DataFrame
data = {'Questions': ["What percentage of people prefer cats over dogs?",
                      "How many students scored above 90% in the exam?",
                      "What is the average height of adults in the population?",
                      "When was the last census conducted?",
                      "Do you like pizza?"]}
df = pd.DataFrame(data)

# Label the questions (1 for numerical, 0 for non-numerical)
df['IsNumerical'] = [1, 1, 1, 0, 0]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df['Questions'], df['IsNumerical'], test_size=0.2, random_state=42)

# Create a bag-of-words representation of the text data
vectorizer = CountVectorizer()
X_train_vectorized = vectorizer.fit_transform(X_train)
X_test_vectorized = vectorizer.transform(X_test)

# Train a Support Vector Machine (SVM) classifier
classifier = SVC(kernel='linear')
classifier.fit(X_train_vectorized, y_train)

# Make predictions on the test set
predictions = classifier.predict(X_test_vectorized)

# Evaluate the model
accuracy = accuracy_score(y_test, predictions)
print(f"Accuracy: {accuracy}")

# Example: Classify a new question
new_question = ["How many books are in the library?"]
new_question = ["What percentage of people are book readers?"]

new_question_vectorized = vectorizer.transform(new_question)
prediction_new = classifier.predict(new_question_vectorized)
print(f"Is the new question numerical? {bool(prediction_new[0])}")
