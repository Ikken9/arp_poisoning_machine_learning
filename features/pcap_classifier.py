from argument_parser import OUTPUT_VERBOSITY_LEVEL_DEBUG


def make_predictions(model, features):
    predictions = model.predict(features)

    if OUTPUT_VERBOSITY_LEVEL_DEBUG:
        print(f"\nPredictions:\n{predictions}")

    return predictions


def classify(predictions, threshold):
    # Classify the data based on a threshold
    classified_predictions = [1 if pred > threshold else 0 for pred in predictions]

    return classified_predictions
