from features.dataset_processing import *
from argument_parser import argument_parser
from model.model_creation import *
from features.pcap_classifier import *

MODEL_PATH = 'model/model.h5'
THRESHOLD = 0.5


def main():
    files = argument_parser()[0]
    normal_traffic = read_pcap(files.normal_pcap)

    # Issue
    print(normal_traffic)
    
    anomaly_traffic = read_pcap(files.anomaly_pcap)
    input_traffic = read_pcap(files.input_pcap)

    # Create normal traffic based labels and tensors
    normal_labels = set_labels(normal_traffic)
    n_features_tensors, n_labels_tensors = create_tensors(normal_traffic, normal_labels)
    print(n_features_tensors)
    print(n_labels_tensors)

    # Create input traffic based labels and tensors
    input_labels = set_labels(input_traffic)
    i_features_tensors, i_labels_tensors = create_tensors(input_traffic, input_labels)

    # Split dataset
    x_train, y_train, x_test, y_test = split_dataset(n_features_tensors, n_labels_tensors)

    # Create model
    untrained_model = create_model()

    # Train model
    trained_moedel = train(untrained_model, x_train, y_train, x_test, y_test)

    # Evaluate model
    evaluate_model(trained_moedel, x_test, y_test)

    # Save model
    save_model(trained_moedel, MODEL_PATH)

    # Load model
    loaded_model = load_model(MODEL_PATH)

    # Make predictions
    predictions = make_predictions(loaded_model, i_features_tensors)

    # Classify
    print(classify(predictions, THRESHOLD))


if __name__ == "__main__":
    main()