import json

import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import tokenizer_from_json


MODEL_PATH = "models/intent_classifier.keras"
TOKENIZER_PATH = "models/tokenizer.json"
LABELS_PATH = "models/labels.json"

MAX_LENGTH = 20


# Load trained model
model = tf.keras.models.load_model(MODEL_PATH)


# Load tokenizer
with open(TOKENIZER_PATH, "r") as file:
    tokenizer = tokenizer_from_json(file.read())


# Load intent labels
with open(LABELS_PATH, "r") as file:
    id_to_label = json.load(file)


def predict_intent(text):
    """
    Predict the user's intent from their text.
    """

    text = text.lower().strip()

    sequence = tokenizer.texts_to_sequences([text])

    padded_sequence = pad_sequences(
        sequence,
        maxlen=MAX_LENGTH,
        padding="post",
        truncating="post"
    )

    prediction = model.predict(
        padded_sequence,
        verbose=0
    )

    predicted_id = int(np.argmax(prediction))

    confidence = float(
        np.max(prediction)
    )

    intent = id_to_label[str(predicted_id)]

    return intent, confidence