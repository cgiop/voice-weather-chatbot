import os
import json
import numpy as np
import tensorflow as tf

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout

from intent_data import INTENTS


# -----------------------------
# 1. Prepare dataset
# -----------------------------

texts = []
labels = []

for intent, examples in INTENTS.items():
    for example in examples:
        texts.append(example.lower())
        labels.append(intent)


# Create label mappings
intent_names = sorted(INTENTS.keys())

label_to_id = {
    intent: index
    for index, intent in enumerate(intent_names)
}

id_to_label = {
    index: intent
    for intent, index in label_to_id.items()
}

y = np.array([
    label_to_id[label]
    for label in labels
])


# -----------------------------
# 2. Tokenization
# -----------------------------

tokenizer = Tokenizer(
    num_words=2000,
    oov_token="<OOV>"
)

tokenizer.fit_on_texts(texts)

sequences = tokenizer.texts_to_sequences(texts)

max_length = 20

X = pad_sequences(
    sequences,
    maxlen=max_length,
    padding="post",
    truncating="post"
)


# -----------------------------
# 3. Build LSTM model
# -----------------------------

model = Sequential([
    Embedding(
        input_dim=len(tokenizer.word_index) + 1,
        output_dim=64
    ),

    LSTM(64),

    Dropout(0.3),

    Dense(
        32,
        activation="relu"
    ),

    Dense(
        len(intent_names),
        activation="softmax"
    )
])


# -----------------------------
# 4. Compile
# -----------------------------

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)


# -----------------------------
# 5. Train
# -----------------------------

print("\nTraining intent classifier...\n")

model.fit(
    X,
    y,
    epochs=100,
    batch_size=8,
    verbose=1
)


# -----------------------------
# 6. Save model
# -----------------------------

os.makedirs("models", exist_ok=True)

model.save("models/intent_classifier.keras")


# Save tokenizer
with open("models/tokenizer.json", "w") as file:
    file.write(tokenizer.to_json())


# Save labels
with open("models/labels.json", "w") as file:
    json.dump(id_to_label, file)


print("\n--------------------------------")
print("Intent classifier trained!")
print("--------------------------------")

print("\nIntents:")

for intent in intent_names:
    print("-", intent)

print("\nModel saved to:")
print("models/intent_classifier.keras")