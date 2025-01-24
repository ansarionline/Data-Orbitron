# Import libraries
import random
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import Sequential
from keras.layers import Dense, Dropout
import pickle

# Download NLTK data
nltk.download("punkt")
nltk.download("wordnet")

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Training data
training_data = [
    {"patterns": ["Hi", "Hello", "How are you?"], "responses": ["Hello!", "Hi there!"]},
    {"patterns": ["What is your name?", "Who are you?"], "responses": ["I'm a chatbot.", "I am your assistant."]},
    {"patterns": ["Bye", "Goodbye"], "responses": ["Goodbye!", "See you later!"]},
]

# Preprocess data
words = []
classes = []
documents = []
ignore_words = ["?", "!"]

# Process each pattern in the dataset
for data in training_data:
    for pattern in data["patterns"]:
        word_list = nltk.word_tokenize(pattern)  # Tokenize pattern
        words.extend(word_list)
        documents.append((word_list, data["responses"]))
        if data["responses"] not in classes:
            classes.extend(data["responses"])

# Lemmatize, lower, and remove duplicates
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(set(words))

# Sort classes
classes = sorted(set(classes))

# Prepare training data
training = []
output_empty = [0] * len(classes)

for doc in documents:
    bag = []
    word_patterns = doc[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(doc[1][0])] = 1  # One response per pattern
    training.append([bag, output_row])

# Shuffle and convert to array
import random
random.shuffle(training)
training = np.array(training, dtype=object)

# Split into features (X) and labels (y)
X_train = np.array(list(training[:, 0]))
y_train = np.array(list(training[:, 1]))

# Build the chatbot model
model = Sequential()
model.add(Dense(128, input_shape=(len(X_train[0]),), activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(64, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(len(y_train[0]), activation="softmax"))

# Compile the model
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

# Train the model
model.fit(X_train, y_train, epochs=200, batch_size=5, verbose=1)

# Save the model and metadata
model.save("chatbot_model.h5")
with open("words.pkl", "wb") as f:
    pickle.dump(words, f)
with open("classes.pkl", "wb") as f:
    pickle.dump(classes, f)

print("Model training complete and saved!")

# Chatbot functions
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence, words):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence, model):
    bow = bag_of_words(sentence, words)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return [{"intent": classes[r[0]], "probability": str(r[1])} for r in results]

def get_response(intents, intents_json):
    tag = intents[0]["intent"]
    for data in intents_json:
        if tag in data["responses"]:
            return random.choice(data["responses"])

# Chat loop
while True:
    message = input("You: ")
    if message.lower() in ["quit", "exit", "bye"]:
        print("Bot: Goodbye!")
        break
    intents = predict_class(message, model)
    response = get_response(intents, training_data)
    print(f"Bot: {response}")
