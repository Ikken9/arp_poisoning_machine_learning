import numpy
import tensorflow as tf
from scapy.layers.l2 import ARP
from argument_parser import OUTPUT_VERBOSITY_LEVEL_DEBUG


def set_labels(data):
    n = len(data)
    arp_requests = {}
    labels = numpy.zeros(n)

    for packet in range(0, n - 1):
        if data[packet].haslayer(ARP):
            arp_packet = data[packet].getlayer(ARP)

            # Ignore gratuitous ARP packets
            if arp_packet.op == 1 and arp_packet.psrc == arp_packet.pdst:
                continue

            if arp_packet.psrc in arp_requests:
                if arp_requests[arp_packet.psrc] != arp_packet.hwsrc:
                    labels[packet] = 1
                    if OUTPUT_VERBOSITY_LEVEL_DEBUG:
                        print("\nARP poisoning detected!")
                        print("IP:", arp_packet.psrc)
                        print("Original MAC:", arp_requests[arp_packet.psrc])
                        print("Spoofed MAC:", arp_packet.hwsrc)
                        print("")
            else:
                arp_requests[arp_packet.psrc] = arp_packet.hwsrc
    return labels


def create_model():
    # Define the classifier model
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(16, activation='relu', input_shape=(4,)),
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    # Compile the model
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    return model


def train(model, x_train, x_test, y_train, y_test):
    # Train the model
    model.fit(x_train, y_train, batch_size=32, epochs=10, validation_data=(x_test, y_test))

    return model


def evaluate_model(model, x_test, y_test):
    loss, accuracy = model.evaluate(x_test, y_test)
    print('Test Loss:', loss)
    print('Test Accuracy:', accuracy)


def save_model(model, path):
    model.save(path)


def load_model(path):
    loaded_model = tf.keras.models.load_model(path)
    return loaded_model
