from features.dataset_processing import *
from argument_parser import *
from model.model_creator import *
from features.pcap_classifier import *
import os.path

MODEL_PATH = 'model/model.h5'
THRESHOLD = 0.5


def main():
    if not os.path.exists(MODEL_PATH):
        model = create_model()

        for i in range(len(args.files)):
            training_traffic = read_pcap(args.files[i])
            parsed_training_traffic = parse_pcap(process_arp_pcap(training_traffic))

            # Create training traffic features and labels tensors
            training_traffic_labels = set_labels(training_traffic)
            features_tensor, labels_tensor = create_tensors(parsed_training_traffic, training_traffic_labels)
            if OUTPUT_VERBOSITY_LEVEL:
                print(f"File at index: {i}")
                print("\nFeatures Tensor:\n")
                print(features_tensor)
                print("\nLabels Tensor:\n")
                print(labels_tensor)

            # Split dataset into training data and test data
            x_train, x_test, y_train, y_test = split_dataset(features_tensor, labels_tensor)

            # Train model
            train(model, x_train, x_test, y_train, y_test)

        # Evaluate model
        # print("\nEvaluate with normal data sample test: ")
        # evaluate_model(model, x_test, y_test)

        # Save model
        save_model(model, MODEL_PATH)

    input_traffic = read_pcap(args.input_pcap)
    parsed_input_traffic = parse_pcap(process_arp_pcap(input_traffic))

    # Create input traffic features and labels tensors
    input_labels = set_labels(input_traffic)
    i_features_tensors, i_labels_tensors = create_tensors(parsed_input_traffic, input_labels)

    if OUTPUT_VERBOSITY_LEVEL:
        print("\nInput Features Tensor:\n")
        print(i_features_tensors)
        print("\nInput Labels Tensor:\n")
        print(i_labels_tensors)

    # Load model
    loaded_model = load_model(MODEL_PATH)

    # Make predictions
    predictions = make_predictions(loaded_model, i_features_tensors)

    # Classify
    print(f"\nClassification: {classify(predictions, THRESHOLD)}")


if __name__ == "__main__":
    main()
