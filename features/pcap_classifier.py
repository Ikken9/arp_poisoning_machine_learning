def make_predictions(model, features):
    return model.predict(features)


def classify(predictions, threshold):
    # Classify the data based on a threshold
    classified_predictions = [1 if pred > threshold else 0 for pred in predictions]

    # Identify the indices of ARP poisoning packets
    arp_poisoning_indices = [i for i, pred in enumerate(classified_predictions) if pred == 1]

    return arp_poisoning_indices





