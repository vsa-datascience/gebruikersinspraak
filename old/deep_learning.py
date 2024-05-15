import pandas as pd
from sklearn.model_selection import train_test_split
from gensim.models import Word2Vec
from keras.models import Sequential
from keras.layers import Dense, Embedding, Flatten
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import numpy as np

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

# Tokenize and pad sequences
tokenizer = Tokenizer()
tokenizer.fit_on_texts(X_train)
X_train_sequences = tokenizer.texts_to_sequences(X_train)
X_test_sequences = tokenizer.texts_to_sequences(X_test)
X_train_padded = pad_sequences(X_train_sequences)
X_test_padded = pad_sequences(X_test_sequences, maxlen=X_train_padded.shape[1])

# Build a Word2Vec model
word2vec_model = Word2Vec(sentences=X_train_sequences, vector_size=100, window=5, min_count=1, workers=4)

# Create an embedding matrix
embedding_matrix = np.zeros((len(tokenizer.word_index) + 1, word2vec_model.wv.vector_size))
for word, i in tokenizer.word_index.items():
    if word in word2vec_model.wv:
        embedding_matrix[i] = word2vec_model.wv[word]

# Build a simple neural network model
model = Sequential()
model.add(Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=embedding_matrix.shape[1],
                    input_length=X_train_padded.shape[1], weights=[embedding_matrix], trainable=False))
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train_padded, y_train, epochs=10, batch_size=2, verbose=1)

# Evaluate the model
accuracy = model.evaluate(X_test_padded, y_test, verbose=1)[1]
print(f"Accuracy: {accuracy}")

# Example: Classify a new question
new_question = ["How many books are in the library?"]
new_question_sequence = tokenizer.texts_to_sequences(new_question)
new_question_padded = pad_sequences(new_question_sequence, maxlen=X_train_padded.shape[1])
prediction_new = model.predict(new_question_padded)[0][0]
print(f"Is the new question numerical? {prediction_new > 0.5}")
