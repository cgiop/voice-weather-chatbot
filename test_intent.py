from intent_classifier import predict_intent


test_sentences = [
    "What's the weather in Chennai?",
    "How hot is Delhi?",
    "What is the humidity?",
    "How fast is the wind?",
    "Hello"
]


for sentence in test_sentences:

    intent, confidence = predict_intent(sentence)

    print("\nUser:", sentence)
    print("Intent:", intent)
    print("Confidence:", round(confidence, 4))