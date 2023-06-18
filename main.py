from features.dataset_processing import *
from argument_parser import *
from model.model_creator import *
from features.pcap_classifier import *
import os.path

MODEL_PATH = 'model/model.h5'
THRESHOLD = 0.5


def main():
    if not os.path.exists(MODEL_PATH):
        normal_traffic = read_pcap(args.normal_pcap)
        anomaly_traffic = read_pcap(args.anomaly_pcap)

        parsed_normal_traffic = parse_pcap(process_arp_pcap(normal_traffic))
        parsed_anomaly_traffic = parse_pcap(process_arp_pcap(anomaly_traffic))

        # Create sample traffic features and labels tensors
        normal_labels = set_labels(normal_traffic)
        n_features_tensors, n_labels_tensors = create_tensors(parsed_normal_traffic, normal_labels)
        if OUTPUT_VERBOSITY_LEVEL_DEBUG:
            print("\nNormal Features Tensor:\n")
            print(n_features_tensors)
            print("\nNormal Labels Tensor:\n")
            print(n_labels_tensors)

        # Create anomaly traffic features and labels tensors
        anomaly_labels = set_labels(anomaly_traffic)
        a_features_tensors, a_labels_tensors = create_tensors(parsed_anomaly_traffic, anomaly_labels)
        if OUTPUT_VERBOSITY_LEVEL_DEBUG:
            print("\nAnomaly Features Tensor:\n")
            print(a_features_tensors)
            print("\nAnomaly Labels Tensor:\n")
            print(a_labels_tensors)

        # Split normal data related dataset into training data and test data
        normal_x_train, normal_x_test, normal_y_train, normal_y_test = split_dataset(
            n_features_tensors, n_labels_tensors)

        # Split anomaly data related dataset into training data and test data
        anomaly_x_train, anomaly_x_test, anomaly_y_train, anomaly_y_test = split_dataset(
            a_features_tensors, a_labels_tensors)

        # Create model
        model = create_model()

        # Train model
        train(model, normal_x_train, normal_x_test, normal_y_train, normal_y_test)
        train(model, anomaly_x_train, anomaly_x_test, anomaly_y_train, anomaly_y_test)

        # Evaluate model
        # print("\nEvaluate with normal data sample test: ")
        # evaluate_model(model, normal_x_test, normal_y_test)
        # print("\nEvaluate with anomaly data sample test: ")
        # evaluate_model(model, anomaly_x_test, anomaly_y_test)

        # Save model
        save_model(model, MODEL_PATH)

    input_traffic = read_pcap(args.input_pcap)
    parsed_input_traffic = parse_pcap(process_arp_pcap(input_traffic))

    # Create input traffic features and labels tensors
    input_labels = set_labels(input_traffic)
    i_features_tensors, i_labels_tensors = create_tensors(parsed_input_traffic, input_labels)

    if OUTPUT_VERBOSITY_LEVEL_DEBUG:
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
